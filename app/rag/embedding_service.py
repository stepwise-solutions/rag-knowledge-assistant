"""Generate text embeddings with Azure OpenAI."""

import os

from openai import AzureOpenAI


class EmbeddingService:
    def __init__(self) -> None:
        self.client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        )
        self.model = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]

    def generate(self, text: str) -> list[float]:
        result = self.client.embeddings.create(model=self.model, input=text)
        return result.data[0].embedding

    def generate_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        result = self.client.embeddings.create(model=self.model, input=texts)
        return [item.embedding for item in result.data]
