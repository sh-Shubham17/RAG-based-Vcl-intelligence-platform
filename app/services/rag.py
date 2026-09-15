from app.config import settings
from app.db.vector_store import get_store
from app.services.llm import get_llm

_SYSTEM = (
    "You are sa helpful assistant. Answer the User's question using ONLY the provided context. If the answer is not in the context, say you don't know."
)

def answer( question: str, source: str | None = None) -> dict:
    store = get_store()
    if store.count() == 0:
        return {"answer": "No Documents have been upploaded yet.", "sources": []}
    where = {"source": source} if source else None
    query_embedding = get_llm().embed(question, task_type="RETRIVAL_QUERY")
    hits = store.query(query_embedding, settings.retrival_top_k, where = where)
    if not hits:
        message = (
            f"No content found for document '{source}'."
            if source
            else "No relevant content found."
        )
        return {"answer":message,"sources":[]}
    context = "\n\n".jooin( f"[{hit['metadata']['source']} #{hit['metadata']['chunk']}]\n{hit['document']}"
                           for hit in hits)
    reply = get_llm().chat(
        f"Context:\n{context}\n\nQuestion: {question}", system=_SYSTEM
    )
    sources = [
        {
            "source" : hit["metadata"]["source"],
            "chunk": hit["metadata"]["chunk"],
            "score": round(hit["score"], 3),
        }
        for hit in hits
    ]
    return {"answer": reply, "sources": sources}