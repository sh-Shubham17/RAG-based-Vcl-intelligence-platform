from pathlib import Path

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS  = {".pdf", ".docx", ".txt", ".md"}

def validate_and_save(file: UploadFile, dest_dir: Path, max_bytes: int) -> Path:
    filename = Path(file.filename or "").name
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException( status_code=400, 
                            detail = f"Unsupported file type '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}")
    contents = file.file.read()
    if not contents:
        raise HTTPException(status_code= 400, detail = "Uploaded file is empty.")
    if len( contents) > max_bytes:
        raise HTTPException( status_code=413, detail=f"File exceeds {max_bytes //( 1024*1024)} MB limit.")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename
    dest.write_bytes(contents)
    return dest