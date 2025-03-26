import gi
import asyncio

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Inicializar o GStreamer
Gst.init(None)

# Criar o pipeline
pipeline = Gst.parse_launch("videotestsrc ! autovideosink")

# Função que roda o pipeline (usado no executor)
def run_pipeline():
    pipeline.set_state(Gst.State.PLAYING)
    print("Pipeline rodando!")

    bus = pipeline.get_bus()
    while True:
        message = bus.timed_pop_filtered(100 * Gst.MSECOND, Gst.MessageType.EOS)
        if message:
            break

    print("Pipeline finalizado!")

# Função assíncrona para iniciar o teste
async def start_basic_test():
    loop = asyncio.get_event_loop()

    # Usar o asyncio para rodar o pipeline em um executor (em um thread separado)
    # Esperamos o 'Future' retornar, para garantir que a execução do pipeline
    await loop.run_in_executor(None, run_pipeline)

    # Retorno imediato para liberar o próximo pedido
    return "GStreamer rodando com sucesso! Pipeline em execução."

# Função assíncrona para parar o pipeline
async def stop_basic_test():
    # Parar o pipeline
    pipeline.set_state(Gst.State.NULL)
    print("Pipeline parado!")
    return "GStreamer parado com sucesso!"
