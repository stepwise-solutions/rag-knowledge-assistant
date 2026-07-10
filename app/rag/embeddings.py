"""Azure OpenAI embedding helpers."""

from app.config import get_settings
from app.services.azure import get_openai_client


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for a single text."""
    settings = get_settings()
    result = get_openai_client().embeddings.create(
        model=settings.azure_openai_embedding_deployment,
        input=text,
    )
    return result.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for a batch of texts."""
    if not texts:
        return []

    settings = get_settings()
    result = get_openai_client().embeddings.create(
        model=settings.azure_openai_embedding_deployment,
        input=texts,
    )
    return [item.embedding for item in result.data]
