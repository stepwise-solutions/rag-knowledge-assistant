"""Centralised application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_settings: "Settings | None" = None


class Settings(BaseSettings):
    """Environment-based settings for Azure and local paths."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    azure_openai_endpoint: str = Field(validation_alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(validation_alias="AZURE_OPENAI_API_KEY")
    azure_openai_api_version: str = Field(
        default="2024-06-01",
        validation_alias="AZURE_OPENAI_API_VERSION",
    )
    azure_openai_gpt_deployment: str = Field(
        validation_alias="AZURE_OPENAI_GPT_DEPLOYMENT"
    )
    azure_openai_embedding_deployment: str = Field(
        validation_alias="AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
    )

    azure_search_endpoint: str = Field(validation_alias="AZURE_SEARCH_ENDPOINT")
    azure_search_api_key: str = Field(validation_alias="AZURE_SEARCH_API_KEY")
    azure_search_index_name: str = Field(validation_alias="AZURE_SEARCH_INDEX_NAME")
    azure_search_vector_field: str = Field(
        default="content_vector",
        validation_alias="AZURE_SEARCH_VECTOR_FIELD",
    )

    raw_docs_path: str = Field(default="data/raw_docs", validation_alias="RAW_DOCS_PATH")
    loaded_docs_path: str = Field(
        default="data/loaded_docs",
        validation_alias="LOADED_DOCS_PATH",
    )


def get_settings() -> Settings:
    """Return cached settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
