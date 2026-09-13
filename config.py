import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """Central configuration class loading values from the environment."""

    # Secret Variables (Should be defined in .env file)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://username:password@host:port/database"
    )

    # LLM Details
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "change-me-in-production")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "change-me-in-production")
    OLLAMA_FAST_MODEL: str = os.getenv("OLLAMA_FAST_MODEL", "qwen2.5:1.5b").strip()
    OLLAMA_THINKING_MODEL: str = os.getenv(
        "OLLAMA_THINKING_MODEL", "llama3.2:3b"
    ).strip()

    # File Paths
    SCANNED_FILES_PATH: str = os.getenv("SCANNED_FILES_PATH", "scanned_files.json")
    DOCUMENTS_DIRECTORY: str = os.getenv("DOCUMENTS_DIR", "documents")


settings = Config()
