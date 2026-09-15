def chunk_text( text:str, size:int, overlap:int) -> list[str]:
    if size <= overlap:
        raise ValueError("Chunk size must be greater than overlap.")
    normalized = " ".join(text.split())
    if not normalized: return []
    step = size - overlap
    chunks: list[str] = []
    for start in range(0, len(normalized), step):
        chunk = normalized[start : start + size].strip()
        if chunk:
            chunks.append(chunk)
        if start + size >= len(normalized):
            break
    return chunks