from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="RAG Document Q&A API",
    description="Production RAG System powered by PostreSQL pgvector & local Ollama",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}
