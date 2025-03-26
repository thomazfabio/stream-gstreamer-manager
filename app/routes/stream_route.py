from fastapi import APIRouter

router = APIRouter()

@router.get("/start_stream")
def start_stream():
    return "Stream iniciado com sucesso!"

@router.get("/stop_stream")
def stop_stream():
    return "Stream parado com sucesso!"
