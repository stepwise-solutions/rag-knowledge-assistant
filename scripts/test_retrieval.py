import sys
from pathlib import Path

# Allow `app.*` imports when running this file from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from app.rag.generation import generate_answer
from app.rag.prompts import build_generation_prompt, format_retrieval_context
from app.rag.retrieval import retrieve_documents

load_dotenv(PROJECT_ROOT / ".env")


def main() -> int:
    question = input("Enter your question: ").strip()
    if not question:
        print("Error: question must not be empty.")
        return 1

    retrieval_results = retrieve_documents(question, top_k=5)
    context = format_retrieval_context(
        [(result.source, result.content) for result in retrieval_results]
    )
    prompt = build_generation_prompt(question, context)
    answer = generate_answer(question, retrieval_results)

    assert isinstance(prompt, str) and prompt.strip(), "Prompt should be a non-empty string"
    assert "Question:" in prompt, "Prompt should include the question"
    assert "Retrieved Context:" in prompt, "Prompt should include retrieved context"
    assert "Instructions:" in prompt, "Prompt should include generation instructions"

    assert isinstance(answer, str) and answer.strip(), "Answer should be a non-empty string"

    print(f"Question: {question}")
    print(f"Retrieved chunks: {len(retrieval_results)}")
    print(f"Prompt length: {len(prompt)} chars")
    print(f"Answer length: {len(answer)} chars")
    print(f"Sources: {[result.source for result in retrieval_results]}")
    print(f"\nAnswer:\n{answer}")
    print("\nRAG pipeline validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
