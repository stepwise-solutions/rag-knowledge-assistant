# RAG Knowledge Assistant

Retrieval-Augmented Generation (RAG) knowledge assistant built on Azure, with a FastAPI backend for querying and a separate ingestion pipeline for indexing documents.

## Project Structure

```text
rag-knowledge-assistant/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── rag/                    # Query pipeline (rewrite → retrieve → generate)
│   ├── ingestion/              # Document loading, chunking, indexing
│   └── evaluation/             # Offline evaluation dataset and runner
├── data/raw_docs/              # Local source documents (.txt, .md)
├── docker/                     # Additional Docker-related assets
├── terraform/                  # Azure infrastructure (OpenAI, Search, Storage)
├── .env                        # Local environment variables (not committed)
├── requirements.txt
└── Dockerfile
```

## Prerequisites

- Python 3.12+
- Azure resources provisioned via [terraform/README.md](terraform/README.md)
- Azure OpenAI, AI Search, and Storage credentials

## Setup

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy and fill in `.env` at the project root with your Azure credentials (values align with Terraform outputs).

3. Place documents in `data/raw_docs/`.

## Run Locally

Start the API server:

```bash
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/health`  
Query endpoint: `POST http://localhost:8000/query` with body `{"question": "..."}`

## Ingestion

Index local documents into Azure AI Search:

```python
from app.ingestion.load_docs import load_local_documents
from app.ingestion.chunking import chunk_documents
from app.ingestion.indexer import index_chunks

docs = load_local_documents()
chunks = chunk_documents(docs)
index_chunks(chunks)
```

## Evaluation

```bash
python -m app.evaluation.eval
```

## Docker

```bash
docker build -t rag-knowledge-assistant .
docker run -p 8000:8000 --env-file .env rag-knowledge-assistant
```

## Infrastructure

Azure resources are defined in the `terraform/` directory. See [terraform/README.md](terraform/README.md) for deployment instructions.
