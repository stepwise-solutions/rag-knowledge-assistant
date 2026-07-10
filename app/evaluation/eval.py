"""Run offline evaluation against a labeled question dataset."""

import json
from pathlib import Path

from app.rag.generation import generate_answer
from app.rag.retrieval import retrieve_documents


def load_dataset(path: str | Path | None = None) -> list[dict]:
    dataset_path = Path(path or Path(__file__).parent / "dataset.json")
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def run_evaluation(dataset: list[dict] | None = None) -> list[dict]:
    """Execute the RAG pipeline for each evaluation example."""
    examples = dataset or load_dataset()
    evaluation_results: list[dict] = []

    for example in examples:
        question = example["question"]
        retrieval_results = retrieve_documents(question)
        answer = generate_answer(question, retrieval_results)

        evaluation_results.append(
            {
                "question": question,
                "answer": answer,
                "expected_answer": example.get("expected_answer"),
                "sources": [result.source for result in retrieval_results],
            }
        )

    return evaluation_results


if __name__ == "__main__":
    for result in run_evaluation():
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}\n")
