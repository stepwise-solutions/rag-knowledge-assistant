"""Run offline evaluation against a labeled question dataset."""

import json
from pathlib import Path

from app.rag.generator import generate_answer
from app.retrieval.retriever import create_retriever


def load_dataset(path: str | Path | None = None) -> list[dict]:
    dataset_path = Path(path or Path(__file__).parent / "dataset.json")
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def run_evaluation(dataset: list[dict] | None = None) -> list[dict]:
    """Execute the RAG pipeline for each evaluation example."""
    examples = dataset or load_dataset()
    results: list[dict] = []

    retriever = create_retriever()

    for example in examples:
        question = example["question"]
        results = retriever.retrieve(question)
        chunks = [result.model_dump() for result in results]
        answer = generate_answer(question, chunks)

        results.append(
            {
                "question": question,
                "answer": answer,
                "expected_answer": example.get("expected_answer"),
                "sources": [chunk.get("source", "") for chunk in chunks],
            }
        )

    return results


if __name__ == "__main__":
    for result in run_evaluation():
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}\n")
