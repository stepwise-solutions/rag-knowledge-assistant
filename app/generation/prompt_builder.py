"""Build grounded prompts from retrieval results."""

import logging

from app.generation.models import PromptBuilderError
from app.retrieval.models import RetrievalResult

logger = logging.getLogger(__name__)

INSTRUCTIONS = """Instructions:
- Answer only using the supplied context.
- If the answer cannot be determined, explicitly state that.
- Reference the relevant source document(s) in the response.
- Never invent information.
- Produce a concise, professional answer.
- Preserve technical terminology."""


class PromptBuilder:
    """Construct LLM prompts from a question and retrieved chunks."""

    def build_prompt(self, question: str, results: list[RetrievalResult]) -> str:
        """Build the final prompt sent to the language model."""
        if not question.strip():
            raise PromptBuilderError("Question must not be empty")

        context_section = self._format_context(results)
        prompt = (
            f"Question:\n\n{question.strip()}\n\n"
            f"Retrieved Context:\n\n{context_section}\n\n"
            f"{INSTRUCTIONS}"
        )

        logger.info("Prompt built successfully with %d chunks", len(results))
        logger.debug("Prompt length: %d characters", len(prompt))

        return prompt

    @staticmethod
    def _format_context(results: list[RetrievalResult]) -> str:
        if not results:
            return "No relevant context was retrieved."

        blocks = [
            f"Source: {result.source}\n\n{result.content.strip()}"
            for result in results
        ]
        return "\n\n---\n\n".join(blocks)
