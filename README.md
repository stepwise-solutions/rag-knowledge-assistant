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
│   ├── create_search_index.py
│   └── test_retrieval.py
├── frontend/                   # React chat UI (Vite + TypeScript)
├── docker/
├── terraform/                  # Azure infrastructure (OpenAI, Search, Storage)
├── .env                        # Local environment variables (not committed)
├── requirements.txt
└── Dockerfile
```

## Prerequisites

- Python 3.12+
- [Node.js](https://nodejs.org/) 18+ (for the chat UI)
- Azure resources provisioned via [terraform/README.md](terraform/README.md)
- Azure OpenAI and AI Search credentials

## Run locally (Windows)

### 1. One-time setup

Open PowerShell in the project root:

```powershell
cd C:\path\to\rag-knowledge-assistant
```

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If script execution is blocked:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Azure credentials (values align with [Terraform outputs](terraform/README.md#connect-to-the-application)):

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

Create the Azure AI Search index (once per environment):

```powershell
python scripts/create_search_index.py
```

Install frontend dependencies (once):

```powershell
cd frontend
Copy-Item .env.example .env
npm install
cd ..
```

The frontend `.env` should contain:

```env
VITE_API_URL=http://localhost:8000
```

### 2. Ingest documents (first time, or when adding new files)

Copy PDFs (or `.txt` / `.md` files) into `data/raw_docs/`, then from the project root:

```powershell
python -m app.ingestion.ingest
```

Successfully indexed files are moved to `data/loaded_docs/`. See [Ingest PDF Documents](#ingest-pdf-documents) for details.

### 3. Start the application

Use **two terminals**, both with the Python venv activated for the backend.

**Terminal 1 — Backend API:**

```powershell
cd C:\path\to\rag-knowledge-assistant
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`  
Health check: `GET http://localhost:8000/health`

**Terminal 2 — Chat UI:**

```powershell
cd C:\path\to\rag-knowledge-assistant\frontend
npm run dev
```

Open `http://localhost:5173` in your browser, type a question, and click **Send**.

### 4. Verify (optional)

**Browser:** Ask a question in the chat UI at `http://localhost:5173`.

**CLI:** Run the interactive test script from the project root:

```powershell
python scripts/test_retrieval.py
```

**API directly:**

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"question\": \"What is the IET?\"}"
```

On Windows PowerShell without `curl`, use the chat UI or `test_retrieval.py` instead.

### Quick reference

| Service | URL | Command |
|---------|-----|---------|
| Backend API | http://localhost:8000 | `uvicorn app.main:app --reload` |
| Chat UI | http://localhost:5173 | `npm run dev` (in `frontend/`) |
| Ingestion | — | `python -m app.ingestion.ingest` |
| Create index | — | `python scripts/create_search_index.py` |

> **Azure Free tier:** Vector search works for dev workloads with a 50 MB storage limit. See [terraform/README.md](terraform/README.md#search-sku-notes) for details.

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

### Ingestion notes

- Only new files in `data/raw_docs/` are processed — already-loaded documents are in `data/loaded_docs/`
- Re-ingesting a document requires moving it back to `data/raw_docs/`
- Partial failures leave affected files in `raw_docs/` (only fully indexed documents are moved)

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
