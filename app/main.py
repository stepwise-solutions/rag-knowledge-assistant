"""FastAPI entrypoint for the RAG knowledge assistant."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import ChatResponse, QueryRequest, QueryResponse
from app.rag.generation import generate_answer
from app.rag.retrieval import retrieve_documents

load_dotenv()

app = FastAPI(title="RAG Knowledge Assistant", version="0.1.0")

cors_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _run_rag(question: str) -> QueryResponse:
    retrieval_results = retrieve_documents(question)
    answer = generate_answer(question, retrieval_results)
    return QueryResponse(
        answer=answer,
        sources=[result.source for result in retrieval_results],
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: QueryRequest) -> ChatResponse:
    result = _run_rag(request.question)
    return ChatResponse(answer=result.answer, sources=result.sources)


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    return _run_rag(request.question)
