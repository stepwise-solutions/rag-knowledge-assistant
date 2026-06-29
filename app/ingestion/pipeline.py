"""Ingestion pipeline: load documents, chunk, embed, and index into Azure AI Search."""

from dataclasses import dataclass

from dotenv import load_dotenv

from app.ingestion.chunking import chunk_documents
from app.ingestion.indexer import index_chunks
from app.ingestion.load_docs import load_local_documents


@dataclass
class IngestionResult:
    documents_loaded: int
    chunks_created: int
    chunks_indexed: int
    documents_moved: list[str]


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
