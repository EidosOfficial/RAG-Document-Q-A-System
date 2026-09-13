# RAG & Agentic Q&A System — Command Runbook

## 1. Environment Activation
Always activate the venv before running any command
```bash
source .venv/bin/activate
```

## 2. Database Service (PostgreSQL + pgvector in Docket)
Start the PostgreSQL container with pgvector pre-compiled on port 5433
```bash
docker run -d \
  --name rag-pgvector \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=rag_db \
  -p 5433:5432 \
  pgvector/pgvector:pg16
```

## 3. Document Ingestion
Populate the PG vector database with all PDFs and MD files from `documents/`:
- **Incremental Ingestion** (skips already scanned files)
```bash
python -m src.services.ingest_service
```
- **Force Re-ingestion** (clears old data)
```bash
python -m src.services.ingest_service --force
```

## 4. Running Automated Tests (via .venv Python)
**Note**: To ensure `pytest` uses your project's `.venv` packages (and avoids global pyenv conflicts), always run via `python -m pytest`:
- Run all tests:
```bash
python -m pytest -v
```
- Run specific test suit:
```bash
python -m pytest src/tests/test_qa.py -v
```

## 5. Running the LangGraph Agentic Workflow
Test the Autonomous LangGraph Agent (Self-Correction, Re-querying, and Math tool execution):
```bash
python -m src.tests.test_agent
```

## 6. Running Retrieval Evaluation (Recall@K Metrics)
Run the emperical evaluation harness against `eval_dataset.json`:
- **Evaluate Top-K = 3** (Optimal Sweet Spot):
```bash
python -m src.evaluate.evaluate --k 3
```

## 7. Running the FastAPI Web Application
Start the Uvicorn production server
```bash
python -m uvicorn main:app --reload --port 8000
```
- **Interactive Swagger API Docs**: Open `http://localhost:8000/docs` in the browser

## 8. Testing API Endpoints via `curl`
- Health Check
```bash
curl http://localhost:8000/health
```
- Standard RAG Q&A Endpoint (`POST /api/v1/ask`)
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is progressive overload?", "top_k": 3}'
```
- Real-Time Token & Citation Streaming (SSE) (`POST /api/v1/ask/stream`):
Notice the `-N` flag to disable terminal output buffering so tokens stream live!
```bash
curl -N -X POST "http://localhost:8000/api/v1/ask/stream" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is progressive overload?", "top_k": 3}'
```