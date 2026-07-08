"""Document retrieval from Azure AI Search."""

from app.retrieval.models import RetrievalResult, RetrieverError, SearchServiceError
from app.retrieval.query_embedding import get_query_embedding
from app.retrieval.query_rewriter import QueryRewriter, rewrite_query
from app.retrieval.retriever import Retriever, create_retriever
from app.retrieval.search_service import SearchService

__all__ = [
    "RetrievalResult",
    "Retriever",
    "RetrieverError",
    "SearchService",
    "SearchServiceError",
    "QueryRewriter",
    "create_retriever",
    "get_query_embedding",
    "rewrite_query",
]
