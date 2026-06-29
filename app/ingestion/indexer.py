"""Embed chunks and upload them to Azure AI Search."""

import os
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from app.rag.embedding_service import EmbeddingService


@dataclass
class IndexResult:
    chunks_indexed: int
    documents_moved: list[str]


def _search_client() -> SearchClient:
    return SearchClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
        credential=AzureKeyCredential(os.environ["AZURE_SEARCH_API_KEY"]),
    )


def _raw_docs_path() -> Path:
    return Path(os.environ.get("RAW_DOCS_PATH", "data/raw_docs"))


def _loaded_docs_path() -> Path:
    return Path(os.environ.get("LOADED_DOCS_PATH", "data/loaded_docs"))


def move_to_loaded_docs(sources: list[str]) -> list[str]:
    """Move successfully indexed documents from raw_docs to loaded_docs."""
    raw_root = _raw_docs_path()
    loaded_root = _loaded_docs_path()
    moved: list[str] = []

    for source in sources:
        src_path = raw_root / source
        if not src_path.is_file():
            continue

        dest_path = loaded_root / source
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dest_path))
        moved.append(source)

    return moved


def _fully_indexed_sources(chunks: list[dict], failed_ids: set[str]) -> list[str]:
    chunks_by_source: dict[str, list[dict]] = defaultdict(list)
    for chunk in chunks:
        chunks_by_source[chunk["source"]].append(chunk)

    return [
        source
        for source, source_chunks in chunks_by_source.items()
        if not any(chunk["id"] in failed_ids for chunk in source_chunks)
    ]


def index_chunks(chunks: list[dict]) -> IndexResult:
    """Upload chunked documents with embeddings to the search index."""
    if not chunks:
        return IndexResult(chunks_indexed=0, documents_moved=[])

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
    failed_ids = {item.key for item in result if not item.succeeded}
    chunks_indexed = sum(1 for item in result if item.succeeded)

    documents_moved = move_to_loaded_docs(_fully_indexed_sources(chunks, failed_ids))

    return IndexResult(
        chunks_indexed=chunks_indexed,
        documents_moved=documents_moved,
    )
