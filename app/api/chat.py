from fastapi import APIRouter, HTTPException

from app.schemas.chat import AskRequest, AskResponse
from app.services import rag

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")
    try:
        result = rag.answer(question, source=req.source)
    except Exception as e:
        raise HTTPException(status_code = 503, detail=f"LLM error: {e}") from e
    return AskResponse(**result)