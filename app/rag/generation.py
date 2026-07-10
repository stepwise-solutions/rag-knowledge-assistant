"""Grounded answer generation using retrieved context."""

from __future__ import annotations

import logging

from openai import OpenAIError

from app.config import get_settings
from app.models.schemas import GenerationError, RetrievalResult
from app.rag.prompts import (
    GENERATION_SYSTEM_PROMPT,
    build_generation_prompt,
    format_retrieval_context,
)
from app.services.azure import get_openai_client

logger = logging.getLogger(__name__)


def generate_answer(question: str, retrieved_chunks: list[RetrievalResult]) -> str:
    """Build a grounded prompt and generate an answer from retrieved chunks."""
    if not question.strip():
        raise GenerationError("Question must not be empty")

    logger.info(
        "Generation started for question with %d retrieved chunks",
        len(retrieved_chunks),
    )

    if not retrieved_chunks:
        logger.info("No retrieval results provided; proceeding with empty context")

    context = format_retrieval_context(
        [(chunk.source, chunk.content) for chunk in retrieved_chunks]
    )
    prompt = build_generation_prompt(question, context)
    logger.info("Prompt built successfully with %d chunks", len(retrieved_chunks))
    logger.debug("Prompt length: %d characters", len(prompt))

    settings = get_settings()
    logger.info("Generation request started")

    try:
        response = get_openai_client().chat.completions.create(
            model=settings.azure_openai_gpt_deployment,
            messages=[
                {"role": "system", "content": GENERATION_SYSTEM_PROMPT},
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
