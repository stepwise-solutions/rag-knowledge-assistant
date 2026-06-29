"""Generate answers using Azure OpenAI with retrieved context."""

import os

from openai import AzureOpenAI

from app.rag.prompts import SYSTEM_PROMPT, build_user_prompt


def _openai_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )


def generate_answer(question: str, chunks: list[dict]) -> str:
    """Produce a grounded answer from retrieved document chunks."""
    client = _openai_client()
    deployment = os.environ["AZURE_OPENAI_GPT_DEPLOYMENT"]

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(question, chunks)},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""
