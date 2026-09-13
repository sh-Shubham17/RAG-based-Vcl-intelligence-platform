from pathlib import Path

import docx

from pypdf import PdfReader

from app.config import settings
from app.db.vector_store import get_store
from app.services.llm import get_llm
from app.utils.chunking import chunk_text

def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if ext == ".docx":
        document = docx.Document(str(path))
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    if ext in (".txt", ".md"):
        return path.read_text(encoding="utf-8", errors="ignore")
    raise ValueError(f"Unsupported file type: {ext}")

def ingest_file(path: Path) -> dict:
    text = extract_text(path)
    chunks = chunk_text( text, settings.chunk_size, settings.chuk_overlap)
    if not chunks:
        raise ValueError("no extractable text foud in the document.")
    embeddings = get_llm().embed_many(chunks, task_type="RETRIEVAL_DOCUMENT")
    source = path.name
    ids = [f"{source}::{i}" for i in range(len(chunks))]
    metadatas = [{"source":source, "chunk":i} for i in range(len(chunks))]
    get_store().add(ids, embeddings, chunks, metadatas)
    return {"source": source, "chunks" : len(chunks)}
