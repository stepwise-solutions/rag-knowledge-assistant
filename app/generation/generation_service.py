"""Azure OpenAI chat completions for answer generation."""

from __future__ import annotations

import logging

from openai import AzureOpenAI, OpenAIError

from app.generation.models import GenerationError, GenerationSettings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a knowledge assistant. Follow the user instructions precisely "
    "and answer only from the supplied context."
)


class GenerationService:
    """Send prompts to Azure OpenAI and return generated answers."""

    def __init__(self, settings: GenerationSettings | None = None) -> None:
        self._settings = settings or GenerationSettings()
        self._client = AzureOpenAI(
            azure_endpoint=self._settings.endpoint,
            api_key=self._settings.api_key,
            api_version=self._settings.api_version,
        )

    def generate(self, prompt: str) -> str:
        """Generate an answer for a completed prompt."""
        logger.info("Generation request started")

        try:
            response = self._client.chat.completions.create(
                model=self._settings.deployment,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
        except OpenAIError as exc:
            logger.error("Azure OpenAI generation failed")
            raise GenerationError("Answer generation failed") from exc

        answer = response.choices[0].message.content or ""
        logger.info("Generation completed successfully")
        return answer
