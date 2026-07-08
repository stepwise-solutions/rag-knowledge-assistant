"""Orchestrate the full retrieval pipeline."""

from __future__ import annotations

import logging

from openai import OpenAIError

from app.embeddings.embedding_service import EmbeddingService
from app.retrieval.models import RetrievalResult, RetrieverError, SearchServiceError
from app.retrieval.query_rewriter import QueryRewriter
from app.retrieval.search_service import SearchService

logger = logging.getLogger(__name__)


class Retriever:
    """Run query rewriting, embedding, and vector search as one pipeline."""

    def __init__(
        self,
        query_rewriter: QueryRewriter,
        embedding_service: EmbeddingService,
        search_service: SearchService,
    ) -> None:
        self._query_rewriter = query_rewriter
        self._embedding_service = embedding_service
        self._search_service = search_service

    def retrieve(self, question: str, top_k: int = 5) -> list[RetrievalResult]:
        """Retrieve the top matching document chunks for a user question."""
        logger.info("Retrieval started for question: %s", question)

        rewritten_query = self._rewrite_query(question)
        query_embedding = self._embed_query(rewritten_query)
        results = self._search(query_embedding, top_k)

        logger.info("Retrieved %d chunks", len(results))
        self._log_results(results)

        return results

    def _rewrite_query(self, question: str) -> str:
        try:
            rewritten_query = self._query_rewriter.rewrite(question)
        except OpenAIError as exc:
            logger.error("Query rewriting failed")
            raise RetrieverError("Query rewriting failed") from exc

        logger.info("Rewritten query: %s", rewritten_query)
        return rewritten_query

    def _embed_query(self, rewritten_query: str) -> list[float]:
        try:
            query_embedding = self._embedding_service.generate(rewritten_query.strip())
        except OpenAIError as exc:
            logger.error("Query embedding generation failed")
            raise RetrieverError("Query embedding generation failed") from exc

        logger.info(
            "Query embedding generated successfully (%d dimensions)",
            len(query_embedding),
        )
        return query_embedding

    def _search(
        self,
        query_embedding: list[float],
        top_k: int,
    ) -> list[RetrievalResult]:
        try:
            return self._search_service.vector_search(
                query_embedding=query_embedding,
                top_k=top_k,
            )
        except SearchServiceError:
            raise
        except Exception as exc:
            logger.error("Vector search failed unexpectedly")
            raise RetrieverError("Vector search failed") from exc

    @staticmethod
    def _log_results(results: list[RetrievalResult]) -> None:
        if not results:
            logger.info("No chunks matched the query")
            return

        for result in results:
            logger.debug(
                "Retrieved source=%s score=%.4f",
                result.source,
                result.score,
            )


def create_retriever() -> Retriever:
    """Build a Retriever with default service dependencies."""
    return Retriever(
        query_rewriter=QueryRewriter(),
        embedding_service=EmbeddingService(),
        search_service=SearchService(),
    )
