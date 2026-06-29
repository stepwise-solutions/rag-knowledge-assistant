"""Retrieve relevant document chunks from Azure AI Search."""

import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


def _search_client() -> SearchClient:
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    api_key = os.environ["AZURE_SEARCH_API_KEY"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]

    return SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(api_key),
    )


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """Run a hybrid search and return the top matching chunks."""
    client = _search_client()
    results = client.search(
        search_text=query,
        top=top_k,
        select=["content", "source", "chunk_id"],
    )

    return [dict(result) for result in results]
