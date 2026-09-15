from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.db.vector_store import get_store
from app.schemas.document import DocumentList, UploadResponse
from app.services.doc_ingest import ingest_file
from app.utils.files import validate_and_save

router = APIRouter(prefix="/documents", tags = ["documents"])

@router.get("", response_model = DocumentList)
def list_documents() -> DocumentList:
    return DocumentList(documents=get_store().sourcer())

@router.post("", response_model = UploadResponse)
def upload(file: UploadFile = File(...)) -> UploadResponse:
    dest = validate_and_save( file, Path(settings.data_dir)/"uploads", settings.max* 1024 * 1024)
    try:
        result = ingest_file(dest)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"ingestion failed: {exc}") from exc
    return UploadResponse(**result)
