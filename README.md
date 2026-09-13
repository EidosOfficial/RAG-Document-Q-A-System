# 🚀 RAG & Agentic Document Q&A System

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-0.5.0-green.svg)](https://github.com/pgvector/pgvector)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://www.langchain.com/langgraph)
[![pytest](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](https://docs.pytest.org/)

An enterprise-ready, self-correcting **Retrieval-Augmented Generation (RAG)** system and **Autonomous AI Agent** built from first principles. 

Featuring **PostgreSQL `pgvector`** vector storage, **Model Tiering** optimization, an **Empirical Evaluation Harness (Recall@K)**, **LangGraph State Graph** orchestration, and **FastAPI Server-Sent Events (SSE)** real-time streaming.

---

## 🌟 Key Features

* 📄 **Multi-Format Ingestion Engine**: Automated document loader supporting `.pdf`, `.md`, and `.txt` files with binary NULL byte (`\x00`) sanitization and state tracking via `scanned_files.json`.
* 🗄️ **High-Performance Vector Storage (`pgvector`)**: Stores 384-dimensional dense embeddings (`SentenceTransformers/all-MiniLM-L6-v2`) in PostgreSQL running inside a containerized Docker setup, executing Cosine Distance (`<=>`) queries in **~93 ms**.
* ⚡ **Model Tiering Architecture**: Dual-model optimization pairing a fast worker model (`qwen2.5:1.5b` for generation) with a reasoning model (`llama3.2:3b` for context evaluation & query rewriting), dropping response latency from **180 seconds down to ~5 seconds** (a **36x speedup**).
* 📊 **Empirical Evaluation Harness**: Benchmarking suite measuring **Recall@K** across ground-truth datasets, empirically proving an optimal **92.86% Recall@3**.
* 🤖 **LangGraph Agentic Orchestration**: Autonomous state machine (`AgentState`) featuring context evaluation nodes, self-correction query rewriters, and function-calling tools (math calculator).
* 📡 **FastAPI & SSE Streaming**: Production REST API supporting standard JSON endpoints (`POST /api/v1/ask`) and Server-Sent Events (`POST /api/v1/ask/stream`) for real-time token and citation streaming (< 0.5s TTFT).

---

## 🏛️ System Architecture

```text
                               +-----------------------------+
                               |     User Input / API Request|
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |      FastAPI Router         |
                               |  (/api/v1/ask/stream [SSE]) |
                               +--------------+--------------+
                                              |
                                              v
                               +-----------------------------+
                               |    LangGraph State Machine  |
                               +--------------+--------------+
                                              |
                     +------------------------+------------------------+
                     | (Document Query)                                | (Math / Function Request)
                     v                                                 v
       +----------------------------+                     +----------------------------+
       |   Vector Search Node       |                     |    Calculator Tool Node    |
       |  (PostgreSQL + pgvector)   |                     +--------------+-------------+
       +-------------+--------------+                                    |
                     |                                                   |
                     v                                                   |
       +----------------------------+                                    |
       |   Context Evaluator Node   |                                    |
       |   (llama3.2:3b Reasoning)  |                                    |
       +------+--------------+------+                                    |
              |              |                                           |
        (Sufficient)   (Insufficient / Poor Retrieval)                   |
              |              |                                           |
              v              v                                           |
       +------------+  +----------------------------+                    |
       | Generator  |  |   Query Rewriter Node      |                    |
       | Node       |  |   (Re-try Retrieval Loop)  |                    |
       +-----+------+  +-------------+--------------+                    |
             |                       |                                   |
             |                       +---> [Loop back to Vector Search]  |
             |                                                           |
             +-----------------------+-----------------------------------+
                                     |
                                     v
                        +----------------------------+
                        |  SSE Streaming Output      |
                        | (Live Tokens & Citations)  |
                        +----------------------------+
```

---

## 📂 Project Structure

```text
Document-QNA-System/
├── config.py                 # Centralized configuration & environment settings
├── main.py                   # FastAPI application entrypoint
├── command_runbook.md        # Operations & CLI runbook
├── eval_dataset.json         # Ground-truth evaluation dataset (14 questions)
├── scanned_files.json        # Incremental ingestion tracking
└── src/                      # Core Application Package
    ├── db/                   # Database session & pgvector table initialization
    │   └── session.py
    ├── core/                 # AI wrappers (Chunker, Embedder, Ollama LLM client)
    │   ├── chunker.py
    │   ├── embedder.py
    │   └── llm.py
    ├── services/             # Business Logic Layer
    │   ├── ingest_service.py # Document loader & vector indexer
    │   ├── vector_service.py # Cosine distance similarity search
    │   └── qa_service.py     # Q&A orchestrator & SSE generator
    ├── api/                  # REST Presentation Layer
    │   ├── schemas.py        # Pydantic Request/Response models
    │   └── routes.py         # FastAPI endpoints (/ask, /ask/stream)
    ├── agent/                # LangGraph State Machine
    │   ├── state.py          # AgentState definition
    │   ├── nodes.py          # Graph nodes & router decision logic
    │   └── graph.py          # StateGraph assembly & compilation
    ├── evaluate/             # Empirical Evaluation Harness
    │   └── evaluate.py       # Recall@K evaluator script
    └── tests/                # Automated Test Suite
        ├── test_qa.py        # Service & API test cases
        └── test_agent.py     # LangGraph agent flow & calculator tool tests
```

---

## 📊 Empirical Evaluation Benchmark Results

The retrieval pipeline was evaluated against a ground-truth dataset of 14 complex queries spanning 15 domain documents (textbooks, whitepapers, resumes, cheat sheets):

| Top-K ($K$) | Total Hits | Recall@K (%) | Avg Search Latency (ms) | Analysis |
| :---: | :---: | :---: | :---: | :--- |
| **$K = 1$** | 10 / 14 | **71.43%** | 92.41 ms | Fast, but misses 4 edge boundary questions. |
| **$K = 2$** | 11 / 14 | **78.57%** | 93.91 ms | Steady improvement. |
| **$K = 3$** | **13 / 14** | **92.86%** | **93.27 ms** | **Optimal Sweet Spot!** Huge +21.4% Recall jump. |
| **$K = 5$** | 13 / 14 | **92.86%** | 91.55 ms | Diminishing returns (same accuracy as $K=3$). |

> **Key Finding**: Proved empirically that $K=3$ achieves the optimal sweet spot (**92.86% Recall@3**) at **~93 ms** vector search time without wasting LLM context window budget.

---

## ⚡ Quick Start Guide

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-username/Document-QNA-System.git
cd Document-QNA-System

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Launch PostgreSQL with `pgvector` (Docker)
```bash
docker run -d \
  --name rag-pgvector \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=rag_db \
  -p 5433:5432 \
  pgvector/pgvector:pg16
```

### 3. Ingest Documents into Vector Database
Place your documents (`.pdf`, `.md`, `.txt`) into `documents/` and run:
```bash
# Incremental ingestion
python -m src.services.ingest_service

# Force re-ingestion (clears database & rescans)
python -m src.services.ingest_service --force
```

### 4. Run Automated Test Suite (`pytest`)
```bash
python -m pytest -v
```

### 5. Run Retrieval Evaluation Harness
```bash
python -m src.evaluate.evaluate --k 3
```

### 6. Start Production Web Application (FastAPI)
```bash
python -m uvicorn main:app --reload --port 8000
```
Open interactive Swagger API Documentation at: `http://localhost:8000/docs`

---

## 📡 API Usage & Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Standard RAG Q&A Endpoint (`POST /api/v1/ask`)
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is progressive overload?", "top_k": 3}'
```

### Real-Time Token & Citation Streaming (SSE) (`POST /api/v1/ask/stream`)
```bash
curl -N -X POST "http://localhost:8000/api/v1/ask/stream" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is progressive overload?", "top_k": 3}'
```

---
