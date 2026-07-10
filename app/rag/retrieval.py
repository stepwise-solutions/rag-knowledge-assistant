"""Document retrieval via query rewriting, embedding, and vector search."""

from __future__ import annotations

import logging
from typing import Any

from azure.core.exceptions import AzureError
from azure.search.documents.models import VectorizedQuery
from openai import OpenAIError

from app.config import get_settings
from app.models.schemas import RetrievalError, RetrievalResult
from app.rag.embeddings import generate_embedding
from app.rag.prompts import QUERY_REWRITE_PROMPT
from app.services.azure import get_openai_client, get_search_client

logger = logging.getLogger(__name__)

SELECT_FIELDS = ["id", "content", "source"]
SCORE_FIELD = "@search.score"


def retrieve_documents(query: str, top_k: int = 5) -> list[RetrievalResult]:
    """Rewrite, embed, and vector-search for the top matching document chunks."""
    logger.info("Retrieval started for question: %s", query)

    rewritten_query = _rewrite_query(query)
    logger.info("Rewritten query: %s", rewritten_query)

    query_embedding = _embed_query(rewritten_query)
    logger.info(
        "Query embedding generated successfully (%d dimensions)",
        len(query_embedding),
    )

    results = _vector_search(query_embedding, top_k)
    logger.info("Retrieved %d chunks", len(results))

    if not results:
        logger.info("No chunks matched the query")
    else:
        for result in results:
            logger.debug(
                "Retrieved source=%s score=%.4f",
                result.source,
                result.score,
            )

    return results


def _rewrite_query(question: str) -> str:
    settings = get_settings()
    try:
        response = get_openai_client().chat.completions.create(
            model=settings.azure_openai_gpt_deployment,
            messages=[
                {"role": "system", "content": QUERY_REWRITE_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.0,
        )
    except OpenAIError as exc:
        logger.error("Query rewriting failed")
        raise RetrievalError("Query rewriting failed") from exc

    rewritten = response.choices[0].message.content
    return rewritten.strip() if rewritten else question


def _embed_query(rewritten_query: str) -> list[float]:
    try:
        return generate_embedding(rewritten_query.strip())
    except OpenAIError as exc:
        logger.error("Query embedding generation failed")
        raise RetrievalError("Query embedding generation failed") from exc


def _vector_search(query_embedding: list[float], top_k: int) -> list[RetrievalResult]:
    if not query_embedding:
        logger.warning("Vector search skipped: query embedding is empty")
        return []

    settings = get_settings()
    vector_query = VectorizedQuery(
        vector=query_embedding,
        k_nearest_neighbors=top_k,
        fields=settings.azure_search_vector_field,
    )

    try:
        response = get_search_client().search(
            search_text=None,
            vector_queries=[vector_query],
            select=SELECT_FIELDS,
            top=top_k,
        )
        raw_results = [dict(item) for item in response]
    except AzureError as exc:
        logger.error(
            "Azure AI Search request failed for index '%s'",
            settings.azure_search_index_name,
        )
        raise RetrievalError("Vector search request failed") from exc

    return [_map_result(item) for item in raw_results]


def _map_result(raw: dict[str, Any]) -> RetrievalResult:
    return RetrievalResult(
        id=str(raw.get("id", "")),
        content=str(raw.get("content", "")),
        source=str(raw.get("source", "")),
        score=float(raw.get(SCORE_FIELD, 0.0)),
    )
