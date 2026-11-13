import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Settings(BaseModel):
    # Optional: only the /api/search/sql and /api/search/combined endpoints
    # need PostgreSQL. Everything else (vector search, RAG chat) works without it.
    DATABASE_URL: str | None = None
    ENV: str = "development"
    DEBUG: bool = False
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    EMBEDDING_MODEL: str = "all-minilm"
    LLM_MODEL: str = "llama3.2"
    LLM_TEMPERATURE: float = 0.2
    DOCS_DIR: str
    CHROMA_PERSIST_DIRECTORY: str


settings = Settings(
    DATABASE_URL=os.getenv("DATABASE_URL") or None,
    ENV=os.getenv("ENV", "development"),
    DEBUG=_env_bool("DEBUG"),
    OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "all-minilm"),
    LLM_MODEL=os.getenv("LLM_MODEL", "llama3.2"),
    LLM_TEMPERATURE=float(os.getenv("LLM_TEMPERATURE", "0.2")),
    DOCS_DIR=os.getenv("DOCS_DIR", str(Path(__file__).resolve().parents[3] / "docs")),
    CHROMA_PERSIST_DIRECTORY=os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        str(Path(__file__).resolve().parents[2] / "data" / "chroma"),
    ),
)
