"""Shared schemas for ingestion, retrieval, and the API."""

from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Document:
    content: str
    source: str


@dataclass
class IngestionResult:
    documents_loaded: int
    chunks_created: int
    chunks_indexed: int
    documents_moved: list[str]


class RetrievalResult(BaseModel):
    id: str
    content: str
    source: str
    score: float


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class RetrievalError(Exception):
    """Raised when document retrieval fails."""


class GenerationError(Exception):
    """Raised when answer generation fails."""
