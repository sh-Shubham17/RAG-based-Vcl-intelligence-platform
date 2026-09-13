from fastapi import FastAPI
from app.api import health, llm
from app.config import settings


app = FastAPI(title=settings.app_name, version="0.1.0")

app.include_router(health.router, prefix="/api")
app.include_router(llm.router, prefix="/api")

@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs"}