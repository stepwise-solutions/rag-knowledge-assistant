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
    from app.generation.generator import create_generator
    from app.retrieval.retriever import create_retriever

    retrieval_results = create_retriever().retrieve(request.question)
    answer = create_generator().generate_answer(request.question, retrieval_results)

    return QueryResponse(
        answer=answer,
        sources=[result.source for result in retrieval_results],
    )
