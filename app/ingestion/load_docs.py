"""Load raw documents from local disk or Azure Blob Storage."""

import os
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass
class Document:
    content: str
    source: str

SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}


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
    root = Path(docs_path or os.environ.get("RAW_DOCS_PATH", "data/raw_docs"))
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