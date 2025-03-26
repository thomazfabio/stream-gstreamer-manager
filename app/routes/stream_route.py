from fastapi import APIRouter
from ..controllers import stream_controller
from pydantic import BaseModel

router = APIRouter()

# Definir o modelo para entrada de dados
class StartStreamRequest(BaseModel):
    rtsp_url: str  # O JSON deve conter esse campo

@router.post("/start_stream")
async def start_stream(request: StartStreamRequest, streamScaleW: int = 640, streamScaleH: int = 480):
    return await stream_controller.start_stream(request.rtsp_url)

@router.get("/list_streams")
async def list_streams():
    return await stream_controller.list_streams()

@router.get("/stop_stream/")
async def stop_stream(stream_id: str):
    return await stream_controller.stop_stream(stream_id)

@router.get("/stop_all_streams")
async def stop_all_streams():
    return await stream_controller.stop_all_streams()
