import gi
import asyncio
import uuid

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Inicializar o GStreamer
Gst.init(None)

# Dicionário para armazenar os pipelines
pipelines = {}

# Função que roda o pipeline (executada em segundo plano)
def run_pipeline(pipeline_id):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        print(f"Pipeline com ID {pipeline_id} não encontrado!")
        return

    pipeline.set_state(Gst.State.PLAYING)
    print(f"Pipeline {pipeline_id} rodando!")

    bus = pipeline.get_bus()
    while True:
        message = bus.timed_pop_filtered(100 * Gst.MSECOND, Gst.MessageType.EOS)
        if message:
            break

    print(f"Pipeline {pipeline_id} finalizado!")
    pipeline.set_state(Gst.State.NULL)
    del pipelines[pipeline_id]

# Função assíncrona para iniciar o pipeline
async def start_pipeline(pipeline_id):
    # Criar um novo pipeline para o ID fornecido
    pipeline = Gst.parse_launch("videotestsrc ! autovideosink")
    pipelines[pipeline_id] = pipeline

    # Executar a pipeline de forma assíncrona
    asyncio.create_task(asyncio.to_thread(run_pipeline, pipeline_id))

    return pipeline_id  # Retorna o ID do pipeline imediatamente

# Função assíncrona para parar o pipeline
async def stop_pipeline(pipeline_id):
    pipeline = pipelines.get(pipeline_id)
    if not pipeline:
        return f"Pipeline com ID {pipeline_id} não encontrado!"

    # Parar o pipeline
    pipeline.set_state(Gst.State.NULL)
    del pipelines[pipeline_id]
    print(f"Pipeline {pipeline_id} parado!")
    return f"Pipeline {pipeline_id} parado com sucesso!"

# Função assíncrona para processar a requisição de iniciar o pipeline
async def start_test_gstreamer():
    pipeline_id = str(uuid.uuid4())  # Gerar um ID único para o pipeline
    return await start_pipeline(pipeline_id)

# Função assíncrona para processar a requisição de parar o pipeline
async def stop_test_gstreamer(request_id: str):
    return await stop_pipeline(request_id)
