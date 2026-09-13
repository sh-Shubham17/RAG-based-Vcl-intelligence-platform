from pydantic import BaseModel

class UploadResponse(BaseModel):
    source: str
    chunks: int

class DocumentList(BaseModel):
    documents: dict[str, int]