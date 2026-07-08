"""Generate query embeddings for vector retrieval."""

from app.embeddings.embedding_service import EmbeddingService


def get_query_embedding(rewritten_query: str) -> list[float]:
    """Embed a rewritten query for Azure AI Search vector search."""
    return EmbeddingService().generate(rewritten_query.strip())
