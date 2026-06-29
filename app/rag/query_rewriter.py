"""Rewrite user queries for improved retrieval."""

import os

from openai import AzureOpenAI

from app.rag.prompts import QUERY_REWRITE_PROMPT


def _openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )


def rewrite_query(question: str) -> str:
    """Expand or clarify the user question for search retrieval."""
    client = _openai_client()
    deployment = os.environ["AZURE_OPENAI_GPT_DEPLOYMENT"]

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": QUERY_REWRITE_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.0,
    )

    rewritten = response.choices[0].message.content
    return rewritten.strip() if rewritten else question
