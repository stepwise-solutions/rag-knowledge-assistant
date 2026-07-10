"""Shared Azure OpenAI and Azure AI Search clients."""

from functools import lru_cache

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI

from app.config import get_settings


@lru_cache
def get_openai_client() -> AzureOpenAI:
    """Return a cached Azure OpenAI client."""
    settings = get_settings()
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_api_version,
    )


@lru_cache
def get_search_client() -> SearchClient:
    """Return a cached Azure AI Search client."""
    settings = get_settings()
    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_api_key),
    )
