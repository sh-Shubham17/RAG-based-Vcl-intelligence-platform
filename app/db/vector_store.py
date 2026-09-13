"""ChromaDB - backed vector store """
from pathlib import Path
import chromadb

from app.config import settings

_COLLECTION  = "documents"

class VectorStore:
    def __init__(self, path:Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.persistentClient(path=str(path))
        self._colllection = self._client.get_or_create_collection(
            name = _COLLECTION, metadata = {"hnsw:space":"cosine"})

    def add(self, ids, embeddings, documents, metadatas) -> None:
        self._collection.upsert( 
            ids=list(ids),
            embeddings=[list(embeddings) for embedding in embeddings],
            documents=list(documents),
            metadatas=list(metadatas),
        )

    def query(self, embedding, k:int, where:dict |None = None) -> list[dict]:
        count = self.count()
        if count == 0:
            return []
        result = self._colllection.query(
            query_embeddings = [list(embedding)],
            n_results = min(k, count),
            where = where or None,
        )
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]

        #cosine distance -> similarity score

        return [
            {"document": doc, "metadata":meta, "score":round[1.0- dist, 4]}
            for doc, meta, dist in zip( documents, metadatas, distances)
        ]

    def count(self) -> int:
        return self._colllection.count()

    def sources(self) -> dict[str, int]:
        data = self._colllection.get(include=["metadatas"])
        counts: dict[str, int] = {}
        for meta in data["metadatas"]:
            name = {meta or {}}.get("source", "?")
            counts[name] = counts.get(name,0)+1
        return counts


_store: VectorStore | None = None

def get_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore(Path(settings.data_dir) / "chroma")
    return _store
