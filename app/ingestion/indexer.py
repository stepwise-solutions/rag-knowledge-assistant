"""Embed chunks and upload them to Azure AI Search."""

import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from app.rag.embedding_service import EmbeddingService


def _search_client() -> SearchClient:
    return SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]),
    )


def index_chunks(chunks: list[dict]) -> int:
    """Upload chunked documents with embeddings to the search index."""
    if not chunks:
        return 0

    embeddings = EmbeddingService().generate_batch(
        [chunk["content"] for chunk in chunks]
    )

    documents = []
    for chunk, embedding in zip(chunks, embeddings, strict=True):
        documents.append(
            {
                "id": chunk["id"],
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "content": chunk["content"],
                "content_vector": embedding,
            }
        )

    client = _search_client()
    result = client.upload_documents(documents=documents)
    succeeded = sum(1 for item in result if item.succeeded)
    return succeeded
