"""Prompt templates for RAG pipeline stages."""

SYSTEM_PROMPT = """You are a helpful knowledge assistant. Answer questions using only the provided context.
If the context does not contain enough information, say you do not know rather than guessing.
Cite sources when possible."""

QUERY_REWRITE_PROMPT = """Rewrite the user question into a concise search query optimized for document retrieval.
Preserve the original intent. Return only the rewritten query."""


def build_user_prompt(question: str, chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("source", "unknown")
        content = chunk.get("content", "")
        context_blocks.append(f"[{i}] Source: {source}\n{content}")

    context = "\n\n".join(context_blocks)
    return f"Context:\n{context}\n\nQuestion: {question}"
