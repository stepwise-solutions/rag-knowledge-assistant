#!/usr/bin/env python3
"""Create the Azure AI Search index used by this RAG app.

Schema matches app/ingestion/indexer.py and app/rag/retriever.py:
  - id             unique identifier for the chunk
  - chunk_id       chunk identifier within the source document
  - source         originating file path
  - content        searchable chunk text (BM25 / hybrid keyword leg)
  - content_vector embedding from text-embedding-3-large (3072 dims)

Requires a billable Search SKU (Basic or above) for vector fields.

Environment (or .env via python-dotenv):
  AZURE_SEARCH_ENDPOINT
  AZURE_SEARCH_API_KEY
  AZURE_SEARCH_INDEX_NAME
  AZURE_SEARCH_VECTOR_DIMENSIONS  optional, default 3072
"""

from __future__ import annotations

import os
import sys

from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from dotenv import load_dotenv

DEFAULT_VECTOR_DIMENSIONS = 3072
VECTOR_PROFILE_NAME = "rag-vector-profile"
HNSW_ALGORITHM_NAME = "rag-hnsw"


def _required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def build_index(name: str, vector_dimensions: int) -> SearchIndex:
    """Build a SearchIndex definition for RAG chunk storage and retrieval."""
    return SearchIndex(
        name=name,
        fields=[
            SimpleField(
                name="id",
                type=SearchFieldDataType.String,
                key=True,
            ),
            SimpleField(
                name="chunk_id",
                type=SearchFieldDataType.String,
            ),
            SearchableField(
                name="source",
                type=SearchFieldDataType.String,
                filterable=True,
                facetable=True,
            ),
            SearchableField(
                name="content",
                type=SearchFieldDataType.String,
            ),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=vector_dimensions,
                vector_search_profile_name=VECTOR_PROFILE_NAME,
                retrievable=True,
            ),
        ],
        vector_search=VectorSearch(
            algorithms=[
                HnswAlgorithmConfiguration(
                    name=HNSW_ALGORITHM_NAME,
                    parameters=HnswParameters(
                        m=4,
                        ef_construction=400,
                        ef_search=500,
                        metric="cosine",
                    ),
                )
            ],
            profiles=[
                VectorSearchProfile(
                    name=VECTOR_PROFILE_NAME,
                    algorithm_configuration_name=HNSW_ALGORITHM_NAME,
                )
            ],
        ),
    )


def create_index(client: SearchIndexClient, index: SearchIndex) -> None:
    try:
        client.get_index(index.name)
    except ResourceNotFoundError:
        print(f"Creating index: {index.name}")
        client.create_index(index)
        print("Index created.")
        return

    print(f"Index already exists: {index.name}")


def main() -> None:
    load_dotenv()

    endpoint = _required_env("AZURE_SEARCH_ENDPOINT")
    api_key = _required_env("AZURE_SEARCH_API_KEY")
    index_name = _required_env("AZURE_SEARCH_INDEX_NAME")
    vector_dimensions = int(
        os.environ.get("AZURE_SEARCH_VECTOR_DIMENSIONS", DEFAULT_VECTOR_DIMENSIONS)
    )

    client = SearchIndexClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    index = build_index(index_name, vector_dimensions=vector_dimensions)
    create_index(client, index)

    print(f"Ready: {index_name} ({vector_dimensions}-dim vectors)")


if __name__ == "__main__":
    main()
