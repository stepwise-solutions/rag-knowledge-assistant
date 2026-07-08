"""Azure AI Search client for vector document retrieval."""

from __future__ import annotations

import logging
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from app.retrieval.models import RetrievalResult, SearchServiceError, SearchSettings

logger = logging.getLogger(__name__)

SELECT_FIELDS = ["id", "content", "source"]
SCORE_FIELD = "@search.score"


class SearchService:
    """Retrieve document chunks from Azure AI Search."""

    def __init__(
        self,
        settings: SearchSettings | None = None,
        client: SearchClient | None = None,
    ) -> None:
        self._settings = settings or SearchSettings()
        self._client = client or self._create_client(self._settings)

    @staticmethod
    def _create_client(settings: SearchSettings) -> SearchClient:
        return SearchClient(
            endpoint=settings.endpoint,
            index_name=settings.index_name,
            credential=AzureKeyCredential(settings.api_key),
        )

    def vector_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """Run pure vector search against the configured index."""
        if not query_embedding:
            logger.warning("Vector search skipped: query embedding is empty")
            return []

        try:
            raw_results = self._execute_vector_search(query_embedding, top_k)
        except AzureError as exc:
            logger.error(
                "Azure AI Search request failed for index '%s'",
                self._settings.index_name,
            )
            raise SearchServiceError("Vector search request failed") from exc

        results = [self._map_result(item) for item in raw_results]

        if not results:
            logger.info("Vector search returned no results")
            return results

        logger.debug("Retrieved %d chunks from Azure AI Search", len(results))
        for result in results:
            logger.debug(
                "Retrieved chunk id=%s source=%s score=%.4f",
                result.id,
                result.source,
                result.score,
            )

        return results

    def _execute_vector_search(
        self,
        query_embedding: list[float],
        top_k: int,
    ) -> list[dict[str, Any]]:
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=top_k,
            fields=self._settings.vector_field,
        )

        response = self._client.search(
            search_text=None,
            vector_queries=[vector_query],
            select=SELECT_FIELDS,
            top=top_k,
        )

        return [dict(item) for item in response]

    @staticmethod
    def _map_result(raw: dict[str, Any]) -> RetrievalResult:
        return RetrievalResult(
            id=str(raw.get("id", "")),
            content=str(raw.get("content", "")),
            source=str(raw.get("source", "")),
            score=float(raw.get(SCORE_FIELD, 0.0)),
        )
