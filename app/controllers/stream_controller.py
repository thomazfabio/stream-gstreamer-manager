import gi
import asyncio
import uuid
import multiprocessing
import time

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)
processes = {}

# Função que executa o pipeline
def run_pipeline(pipeline_id, rtsp_url, conn):
    Gst.init(None)
    print(f"Iniciando pipeline {pipeline_id} para {rtsp_url}")

    pipeline = Gst.parse_launch(f"rtspsrc location={rtsp_url} ! decodebin ! autovideosink")
    pipeline.set_state(Gst.State.PLAYING)

    bus = pipeline.get_bus()
    reconnection_attempts = 0

    while True:
        message = bus.timed_pop_filtered(500 * Gst.MSECOND, Gst.MessageType.ERROR | Gst.MessageType.EOS)

        if message:
            err, debug = message.parse_error()
            print(f"Erro no pipeline {pipeline_id}: {err.message}")
            
            if "403" in err.message or "401" in err.message:
                conn.send("AUTH_ERROR")
                break
            elif "Could not connect" in err.message or "No route to host" in err.message:
                reconnection_attempts += 1
                if reconnection_attempts > 5:
                    conn.send("CONNECTION_LOST")
                    break
                print(f"Tentando reconectar ({reconnection_attempts})...")
                time.sleep(2)
                pipeline.set_state(Gst.State.READY)
                pipeline.set_state(Gst.State.PLAYING)
                continue
            else:
                conn.send("UNKNOWN_ERROR")
                break
        
        if conn.poll():
            command = conn.recv()
            if command == "STOP":
                break
    
    pipeline.set_state(Gst.State.NULL)
    conn.close()
    print(f"Pipeline {pipeline_id} parado corretamente.")

# Função para iniciar um pipeline
async def start_stream(rtsp_url):
    pipeline_id = str(uuid.uuid4())
    parent_conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=run_pipeline, args=(pipeline_id, rtsp_url, child_conn))
    process.start()
    processes[pipeline_id] = (process, parent_conn)
    return pipeline_id

# Função para parar um pipeline específico
async def stop_stream(pipeline_id):
    if pipeline_id not in processes:
        return f"Pipeline {pipeline_id} não encontrado!"

    process, conn = processes[pipeline_id]
    if not process.is_alive():
        del processes[pipeline_id]
        return f"Pipeline {pipeline_id} já foi encerrado."
    
    conn.send("STOP")
    process.join(timeout=2)
    if process.is_alive():
        process.terminate()
    del processes[pipeline_id]
    return f"Pipeline {pipeline_id} parado com sucesso!"

# Função para listar todos os pipelines em execução
async def list_streams():
    return [pid for pid, (proc, _) in processes.items() if proc.is_alive()]

# Função para parar todos os pipelines
async def stop_all_streams():
    for pipeline_id in list(processes.keys()):
        await stop_stream(pipeline_id)
    return "Todos os pipelines foram parados."

#monitora os pipelines
async def monitor_pipelines():
    while True:
        for pipeline_id, (process, conn) in list(processes.items()):
            if not process.is_alive():
                print(f"Removendo pipeline morto: {pipeline_id}")
                del processes[pipeline_id]
            elif conn.poll():
                message = conn.recv()
                if message in ["AUTH_ERROR", "CONNECTION_LOST", "UNKNOWN_ERROR"]:
                    print(f"Erro detectado no pipeline {pipeline_id}: {message}")
                    await stop_stream(pipeline_id)
        await asyncio.sleep(15)