"""Load documents, chunk, embed, index, and archive ingested files."""

from __future__ import annotations

import logging
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

from app.config import get_settings
from app.ingestion.chunking import chunk_documents
from app.models.schemas import Document, IngestionResult
from app.rag.embeddings import generate_embeddings_batch
from app.services.azure import get_search_client

logger = logging.getLogger(__name__)

SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


@dataclass
class _IndexResult:
    chunks_indexed: int
    documents_moved: list[str]


def _read_file_content(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    raise ValueError(f"Unsupported file type: {suffix}")


def load_local_documents(docs_path: str | None = None) -> list[Document]:
    """Read text, markdown, and PDF files from the raw docs directory."""
    settings = get_settings()
    root = Path(docs_path or settings.raw_docs_path)
    documents: list[Document] = []

    if not root.exists():
        return documents

    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.append(
                Document(
                    content=_read_file_content(path),
                    source=str(path.relative_to(root)),
                )
            )

    return documents


def _move_to_loaded_docs(sources: list[str]) -> list[str]:
    settings = get_settings()
    raw_root = Path(settings.raw_docs_path)
    loaded_root = Path(settings.loaded_docs_path)
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


def index_chunks(chunks: list[dict]) -> _IndexResult:
    """Upload chunked documents with embeddings to the search index."""
    if not chunks:
        return _IndexResult(chunks_indexed=0, documents_moved=[])

    embeddings = generate_embeddings_batch([chunk["content"] for chunk in chunks])

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

    result = get_search_client().upload_documents(documents=documents)
    failed_ids = {item.key for item in result if not item.succeeded}
    chunks_indexed = sum(1 for item in result if item.succeeded)
    documents_moved = _move_to_loaded_docs(_fully_indexed_sources(chunks, failed_ids))

    return _IndexResult(
        chunks_indexed=chunks_indexed,
        documents_moved=documents_moved,
    )


def run_ingestion(
    docs_path: str | None = None,
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> IngestionResult:
    """Load raw documents, chunk them, and index into the vector store."""
    documents = load_local_documents(docs_path)
    chunks = chunk_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    index_result = index_chunks(chunks)

    return IngestionResult(
        documents_loaded=len(documents),
        chunks_created=len(chunks),
        chunks_indexed=index_result.chunks_indexed,
        documents_moved=index_result.documents_moved,
    )


def main() -> None:
    load_dotenv()

    result = run_ingestion()

    print(f"Loaded {result.documents_loaded} documents")
    print(f"Created {result.chunks_created} chunks")
    print(f"Indexed {result.chunks_indexed} chunks")

    if result.documents_moved:
        print(f"Moved {len(result.documents_moved)} documents to loaded_docs:")
        for source in result.documents_moved:
            print(f"  - {source}")
    elif result.documents_loaded == 0:
        print("No documents found in raw_docs.")
    else:
        print("No documents moved (indexing may have partially failed).")


if __name__ == "__main__":
    main()
