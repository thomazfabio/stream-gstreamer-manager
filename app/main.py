from typing import Union
from fastapi import FastAPI
from .routes import stream_route , services_route
import asyncio

app = FastAPI(
    title="Gerenciador de Streaming",  # Nome customizado
    version="1.0.0",  # Versão customizada
    description="API para gerenciamento de streaming com controlle de frames."
)


app.include_router(stream_route.router, tags=["Streaming Manager"], prefix="/stream")  # Incluindo as rotas do stream_route.py
app.include_router(services_route.router, tags=["Services"], prefix="/services")  # Incluindo as rotas do services_route.py
