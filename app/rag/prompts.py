"""Prompt templates for query rewriting and answer generation."""

QUERY_REWRITE_PROMPT = """Rewrite the user question into a concise search query optimized for document retrieval.
Preserve the original intent. Return only the rewritten query."""

GENERATION_SYSTEM_PROMPT = (
    "You are a knowledge assistant. Follow the user instructions precisely "
    "and answer only from the supplied context."
)

GENERATION_INSTRUCTIONS = """Instructions:
- Answer only using the supplied context.
- If the answer cannot be determined, explicitly state that.
- Reference the relevant source document(s) in the response.
- Never invent information.
- Produce a concise, professional answer.
- Preserve technical terminology."""


def build_generation_prompt(question: str, context_section: str) -> str:
    """Build the user prompt for grounded answer generation."""
    return (
        f"Question:\n\n{question.strip()}\n\n"
        f"Retrieved Context:\n\n{context_section}\n\n"
        f"{GENERATION_INSTRUCTIONS}"
    )


def format_retrieval_context(sources: list[tuple[str, str]]) -> str:
    """Format retrieved chunks as labelled context blocks."""
    if not sources:
        return "No relevant context was retrieved."

    blocks = [f"Source: {source}\n\n{content.strip()}" for source, content in sources]
    return "\n\n---\n\n".join(blocks)
