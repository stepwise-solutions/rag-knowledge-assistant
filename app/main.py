"""FastAPI entrypoint for the RAG knowledge assistant."""

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="RAG Knowledge Assistant", version="0.1.0")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    from app.retrieval.retriever import create_retriever
    from app.rag.generator import generate_answer

    results = create_retriever().retrieve(request.question)
    chunks = [result.model_dump() for result in results]
    answer = generate_answer(request.question, chunks)

    return QueryResponse(
        answer=answer,
        sources=[chunk.get("source", "") for chunk in chunks],
    )
