from fastapi import FastAPI
from app.api import upload, infer, ask
from app.services.vector_store import create_collection

app = FastAPI()

app.include_router(upload.router)
app.include_router(infer.router)
app.include_router(ask.router)

@app.on_event("startup")
def on_startup():
    create_collection()  # optional default
