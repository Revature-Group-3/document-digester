import os
from pathlib import Path
DOCS_DIR = os.getenv("DOCS_DIR", str(Path(__file__).resolve().parents[3] / "docs"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")