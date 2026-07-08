"""Generation layer models and configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GenerationSettings(BaseSettings):
    """Azure OpenAI chat configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    endpoint: str = Field(validation_alias="AZURE_OPENAI_ENDPOINT")
    api_key: str = Field(validation_alias="AZURE_OPENAI_API_KEY")
    api_version: str = Field(
        default="2024-06-01",
        validation_alias="AZURE_OPENAI_API_VERSION",
    )
    deployment: str = Field(validation_alias="AZURE_OPENAI_GPT_DEPLOYMENT")


class GenerationError(Exception):
    """Raised when Azure OpenAI answer generation fails."""


class GeneratorError(Exception):
    """Raised when the generation pipeline fails."""


class PromptBuilderError(Exception):
    """Raised when prompt construction fails."""
