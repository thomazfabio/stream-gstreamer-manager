from fastapi import APIRouter
from ..controllers import services_controller
import uuid

router = APIRouter()

@router.post("/start_test_gstreamer")
async def start_test():
    rtsp = 'rtsp://th:th0202@5.189.183.118:8554/transit_VGA_640x480_1'
    pipeline_id = await services_controller.start_test_gstreamer(rtsp)  # Inicia o pipeline e recebe o ID
    return {"pipeline_id": pipeline_id}  # Retorna o ID para o usuário

@router.post('/list_pipelines')
async def list_pipelines():
    return await services_controller.list_pipelines()

@router.post("/stop_test_gstreamer/{pipeline_id}")
async def stop_test(pipeline_id: str):
    return await services_controller.stop_test_gstreamer(pipeline_id)

@router.post("/stop_all_pipelines")
async def stop_all():
    return await services_controller.stop_all_pipelines()