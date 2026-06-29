from dotenv import load_dotenv

from app.ingestion.chunking import chunk_documents
from app.ingestion.indexer import index_chunks, _search_client
from app.ingestion.load_docs import load_local_documents

load_dotenv()

docs = load_local_documents()
chunks = chunk_documents(docs)

print(f"Loaded {len(docs)} documents, {len(chunks)} chunks")

indexed = index_chunks(chunks)
print(f"Indexed {indexed} chunks")
