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
    from app.rag.query_rewriter import rewrite_query
    from app.rag.retriever import retrieve
    from app.rag.generator import generate_answer

    rewritten = rewrite_query(request.question)
    chunks = retrieve(rewritten)
    answer = generate_answer(request.question, chunks)

    return QueryResponse(
        answer=answer,
        sources=[chunk.get("source", "") for chunk in chunks],
    )
