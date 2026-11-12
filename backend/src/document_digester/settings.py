import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str
    ENV: str = "development"
    DEBUG: bool = False
    EMBEDDING_MODEL: str
    DOCS_DIR: str
    CHROMA_PERSIST_DIRECTORY: str

settings = Settings(
    DATABASE_URL=os.getenv("DATABASE_URL"),
    EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "all-minilm"),
    DOCS_DIR=os.getenv("DOCS_DIR", str(Path(__file__).resolve().parents[3] / "docs")),
    CHROMA_PERSIST_DIRECTORY=os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        str(Path(__file__).resolve().parents[2] / "data" / "chroma"),
    )
)
