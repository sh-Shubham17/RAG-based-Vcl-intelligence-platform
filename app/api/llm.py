from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.llm import get_llm

router = APIRouter(prefix="/llm", tags=["llm"])

@router.get("/check")
def check() -> dict:
    """confirm the Gemini free API key works with one lightweight call."""
    try:
        reply = get_llm().ping()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    return {"status": "ok", "model": settings.gemini_chat_model, "reply": reply}