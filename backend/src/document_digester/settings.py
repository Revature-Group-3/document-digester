import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

DOCS_DIR = os.getenv("DOCS_DIR", str(Path(__file__).resolve().parents[3] / "docs"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")

load_dotenv()

class Settings(BaseModel):
    DATABASE_URL: str
    ENV: str = "development"
    DEBUG: bool = False

settings = Settings(
    DATABASE_URL=os.getenv("DATABASE_URL")
)
