"""Retrieval layer models and configuration."""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SearchSettings(BaseSettings):
    """Azure AI Search configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    endpoint: str = Field(validation_alias="AZURE_SEARCH_ENDPOINT")
    api_key: str = Field(validation_alias="AZURE_SEARCH_API_KEY")
    index_name: str = Field(validation_alias="AZURE_SEARCH_INDEX_NAME")
    vector_field: str = Field(
        default="content_vector",
        validation_alias="AZURE_SEARCH_VECTOR_FIELD",
    )


class RetrievalResult(BaseModel):
    """One chunk returned from vector similarity search."""

    id: str
    content: str
    source: str
    score: float


class SearchServiceError(Exception):
    """Raised when Azure AI Search retrieval operations fail."""


class RetrieverError(Exception):
    """Raised when the retrieval pipeline fails."""
