from dotenv import load_dotenv

from app.ingestion.chunking import chunk_documents
from app.ingestion.indexer import index_chunks
from app.ingestion.load_docs import load_local_documents

load_dotenv()

docs = load_local_documents()
chunks = chunk_documents(docs)

print(f"Loaded {len(docs)} documents, {len(chunks)} chunks")

result = index_chunks(chunks)
print(f"Indexed {result.chunks_indexed} chunks")
print(f"Moved {len(result.documents_moved)} documents to loaded_docs")
