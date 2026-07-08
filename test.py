from dotenv import load_dotenv

from app.embeddings.embedding_service import EmbeddingService
from app.retrieval import QueryRewriter, Retriever
from app.retrieval.search_service import SearchService

load_dotenv()

question = "what is the IET and what does it stand for?"

retriever = Retriever(
    query_rewriter=QueryRewriter(),
    embedding_service=EmbeddingService(),
    search_service=SearchService(),
)

results = retriever.retrieve(question=question, top_k=5)

print(f"Question: {question}")
print(f"Retrieved {len(results)} chunks\n")

for i, result in enumerate(results, start=1):
    print(f"[{i}] {result.source} (score={result.score:.4f})")
    print(result.content[:200])
    print()
