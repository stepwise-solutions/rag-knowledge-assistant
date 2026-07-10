"""FastAPI entrypoint for the RAG knowledge assistant."""

from dotenv import load_dotenv
from fastapi import FastAPI

from app.models.schemas import QueryRequest, QueryResponse
from app.rag.generation import generate_answer
from app.rag.retrieval import retrieve_documents

load_dotenv()

app = FastAPI(title="RAG Knowledge Assistant", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    retrieval_results = retrieve_documents(request.question)
    answer = generate_answer(request.question, retrieval_results)

    return QueryResponse(
        answer=answer,
        sources=[result.source for result in retrieval_results],
    )
