import gi
import asyncio
import uuid
import multiprocessing

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Inicializar o GStreamer
Gst.init(None)

# Dicionário para armazenar os processos e conexões
processes = {}

# Função que roda o pipeline dentro de um processo separado
def run_pipeline(pipeline_id, rtsp_url, conn):
    Gst.init(None)  # Cada processo precisa inicializar o GStreamer separadamente

    print(f"Iniciando pipeline {pipeline_id} para {rtsp_url}")

    pipeline = Gst.parse_launch(f"rtspsrc location={rtsp_url} ! decodebin ! autovideosink")

    pipeline.set_state(Gst.State.PLAYING)

    bus = pipeline.get_bus()
    while True:
        message = bus.timed_pop_filtered(100 * Gst.MSECOND, Gst.MessageType.EOS | Gst.MessageType.ERROR)

        if message:
            print(f"Pipeline {pipeline_id} finalizado ou erro detectado!")
            break

        # Verifica se há um comando de parada do processo principal
        if conn.poll():
            command = conn.recv()
            if command == "STOP":
                print(f"Recebido comando de parada para {pipeline_id}")
                break

    pipeline.set_state(Gst.State.NULL)
    conn.close()
    print(f"Pipeline {pipeline_id} parado corretamente.")

# Função assíncrona para iniciar um novo pipeline
async def start_pipeline(rtsp_url):
    pipeline_id = str(uuid.uuid4())  # Gera um ID único
    parent_conn, child_conn = multiprocessing.Pipe()

    process = multiprocessing.Process(target=run_pipeline, args=(pipeline_id, rtsp_url, child_conn))
    process.start()

    # Armazena o processo e a conexão
    processes[pipeline_id] = (process, parent_conn)

    return pipeline_id  # Retorna o ID do pipeline

# Função assíncrona para parar um pipeline específico
async def stop_pipeline(pipeline_id):
    if pipeline_id not in processes:
        return f"Pipeline {pipeline_id} não encontrado!"

    print(f"Parando pipeline {pipeline_id}...")

    process, conn = processes[pipeline_id]

    # Envia sinal para o processo parar
    conn.send("STOP")
    process.join(timeout=2)  # Espera 2 segundos para encerrar corretamente

    if process.is_alive():
        process.terminate()  # Força encerramento se necessário

    del processes[pipeline_id]
    return f"Pipeline {pipeline_id} parado com sucesso!"

# Função assíncrona para listar todos os pipelines em execução
async def list_pipelines():
    return list(processes.keys())

# Função assíncrona para parar todos os pipelines
async def stop_all_pipelines():
    pipeline_ids = list(processes.keys())
    for pipeline_id in pipeline_ids:
        await stop_pipeline(pipeline_id)
    return f"Todos os {len(pipeline_ids)} pipelines foram parados."

# Função assíncrona para iniciar um pipeline RTSP
async def start_test_gstreamer(rtsp_url: str):
    return await start_pipeline(rtsp_url)

# Função assíncrona para parar um pipeline RTSP
async def stop_test_gstreamer(request_id: str):
    return await stop_pipeline(request_id)
