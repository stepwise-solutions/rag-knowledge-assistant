# RAG Knowledge Assistant

Retrieval-Augmented Generation (RAG) knowledge assistant built on Azure, with a FastAPI backend for querying and a separate ingestion pipeline for indexing documents.

## Project Structure

```text
rag-knowledge-assistant/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Centralised environment settings
│   ├── ingestion/
│   │   ├── ingest.py           # Load, chunk, embed, index, archive documents
│   │   └── chunking.py         # Text splitting for retrieval
│   ├── rag/
│   │   ├── embeddings.py       # Azure OpenAI embedding helpers
│   │   ├── retrieval.py        # Query rewrite, embed, vector search
│   │   ├── generation.py       # Grounded answer generation
│   │   └── prompts.py          # Prompt templates
│   ├── models/
│   │   └── schemas.py          # Shared data models (RetrievalResult, API schemas)
│   ├── services/
│   │   └── azure.py            # Shared Azure OpenAI and AI Search clients
│   └── evaluation/
│       ├── eval.py             # Offline evaluation runner
│       └── dataset.json        # Sample evaluation questions
├── data/
│   ├── raw_docs/               # Documents waiting to be ingested (.pdf, .txt, .md)
│   └── loaded_docs/            # Successfully indexed documents (moved automatically)
├── scripts/
│   ├── create_search_index.py  # Create the Azure AI Search vector index
│   └── test_retrieval.py       # Manual end-to-end RAG test script
├── docker/
├── terraform/                  # Azure infrastructure (OpenAI, Search, Storage)
├── .env                        # Local environment variables (not committed)
├── requirements.txt
└── Dockerfile
```

## Prerequisites

- Python 3.12+
- Azure resources provisioned via [terraform/README.md](terraform/README.md)
- Azure OpenAI, AI Search, and Storage credentials

## Setup (Windows)

1. **Clone the repository** and open PowerShell in the project root:

   ```powershell
   cd C:\path\to\rag-knowledge-assistant
   ```

2. **Create and activate a virtual environment:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   If script execution is blocked, run once:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables** — create a `.env` file in the project root with your Azure credentials (values align with Terraform outputs):

   ```env
   # Azure OpenAI
   AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-key
   AZURE_OPENAI_GPT_DEPLOYMENT=gpt-4.1-mini
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
   AZURE_OPENAI_API_VERSION=2024-06-01

   # Azure AI Search
   AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
   AZURE_SEARCH_API_KEY=your-key
   AZURE_SEARCH_INDEX_NAME=rag-documents

   # Application
   RAW_DOCS_PATH=data/raw_docs
   LOADED_DOCS_PATH=data/loaded_docs
   ```

5. **Create the Azure AI Search index** (required once before first ingestion):

   ```powershell
   python scripts/create_search_index.py
   ```

   The Free tier supports vector search for development and small workloads, with limits.

## Ingest PDF Documents

The ingestion pipeline reads PDFs (and `.txt` / `.md` files), chunks them, generates embeddings, and uploads them to Azure AI Search. Successfully indexed files are moved from `data/raw_docs/` to `data/loaded_docs/`.

### Step 1 — Add documents

Copy your PDF files into `data/raw_docs/`:

```text
data/raw_docs/
├── company-policy.pdf
├── product-guide.pdf
└── reports/
    └── annual-report.pdf
```

Subfolders are supported — the relative path is stored as the document source.

Useful sites for open source publications:
- https://www.nist.gov/publications
- https://www.gov.uk/official-documents
- https://www.who.int/publications

### Step 2 — Run ingestion

From the project root with your virtual environment activated:

```powershell
python -m app.ingestion.ingest
```

Expected output:

```text
Loaded 3 documents
Created 42 chunks
Indexed 42 chunks
Moved 3 documents to loaded_docs:
  - company-policy.pdf
  - product-guide.pdf
  - reports/annual-report.pdf
```

### Step 3 — Verify

- Indexed PDFs appear in `data/loaded_docs/` (removed from `raw_docs/`)
- Query the API or run the test script to confirm retrieval works

```powershell
python scripts/test_retrieval.py
```

You will be prompted to enter your question interactively.

### Ingestion notes

- Only new files in `data/raw_docs/` are processed — already-loaded documents are in `data/loaded_docs/`
- Re-ingesting a document requires moving it back to `data/raw_docs/`
- Partial failures leave affected files in `raw_docs/` (only fully indexed documents are moved)

## Run Locally

Start the API server:

```powershell
uvicorn app.main:app --reload
```

Health check: `GET http://localhost:8000/health`  
Query endpoint: `POST http://localhost:8000/query` with body `{"question": "..."}`

### Test the RAG pipeline

Run an end-to-end retrieval and generation test from the command line:

```powershell
python scripts/test_retrieval.py
```

When prompted, type your question and press Enter:

```text
Enter your question: What impact did Norm AI have on AI in the legal industry?
```

## Evaluation

```powershell
python -m app.evaluation.eval
```

## Docker

```powershell
docker build -t rag-knowledge-assistant .
docker run -p 8000:8000 --env-file .env rag-knowledge-assistant
```

## Infrastructure

Azure resources are defined in the `terraform/` directory. See [terraform/README.md](terraform/README.md) for deployment instructions.
