from typing import Union

from fastapi import FastAPI

app = FastAPI(
    title="Meu Servidor de Inferência",  # Nome customizado
    version="1.0.0",  # Versão customizada
    description="API para processamento de frames e inferência usando DeepStream."
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}