from dotenv import load_dotenv

from app.generation import GenerationService, Generator, PromptBuilder
from app.retrieval.retriever import create_retriever

load_dotenv()

question = "what is the IET and what does it stand for?"

retrieval_results = create_retriever().retrieve(question, top_k=5)

prompt_builder = PromptBuilder()
generation_service = GenerationService()
generator = Generator(
    prompt_builder=prompt_builder,
    generation_service=generation_service,
)

prompt = prompt_builder.build_prompt(question, retrieval_results)
answer = generator.generate_answer(question, retrieval_results)

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
print("\nGeneration stage validated successfully.")
