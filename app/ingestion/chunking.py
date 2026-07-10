"""Split documents into retrieval-sized chunks."""

import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.schemas import Document


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """Split each document into overlapping chunks with source metadata."""
    # TODO: explore semantic chunking methods
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks: list[dict] = []
    for doc in documents:
        texts = splitter.split_text(doc.content)
        for i, text in enumerate(texts):
            chunks.append(
                {
                    "id": str(uuid.uuid4()),
                    "chunk_id": f"{doc.source}#{i}",
                    "source": doc.source,
                    "content": text,
                }
            )

    return chunks
