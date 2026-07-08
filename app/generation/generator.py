"""Orchestrate prompt building and answer generation."""

from __future__ import annotations

import logging

from app.generation.generation_service import GenerationService
from app.generation.models import GenerationError, GeneratorError, PromptBuilderError
from app.generation.prompt_builder import PromptBuilder
from app.retrieval.models import RetrievalResult

logger = logging.getLogger(__name__)


class Generator:
    """Build a grounded prompt and generate an answer from retrieval results."""

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        generation_service: GenerationService,
    ) -> None:
        self._prompt_builder = prompt_builder
        self._generation_service = generation_service

    def generate_answer(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> str:
        """Generate an answer using retrieved document chunks as context."""
        logger.info(
            "Generation started for question with %d retrieved chunks",
            len(results),
        )

        if not results:
            logger.info("No retrieval results provided; proceeding with empty context")

        prompt = self._build_prompt(question, results)

        try:
            return self._generation_service.generate(prompt)
        except GenerationError:
            raise
        except Exception as exc:
            logger.error("Answer generation failed unexpectedly")
            raise GeneratorError("Answer generation failed") from exc

    def _build_prompt(
        self,
        question: str,
        results: list[RetrievalResult],
    ) -> str:
        try:
            return self._prompt_builder.build_prompt(question, results)
        except PromptBuilderError:
            raise
        except Exception as exc:
            logger.error("Prompt construction failed")
            raise GeneratorError("Prompt construction failed") from exc


def create_generator() -> Generator:
    """Build a Generator with default service dependencies."""
    return Generator(
        prompt_builder=PromptBuilder(),
        generation_service=GenerationService(),
    )
