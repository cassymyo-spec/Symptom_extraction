from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="V-Vet Symptom Extraction API",
    description="Livestock symptom extraction service",
    version="1.0.0"
)


app.include_router(router)
