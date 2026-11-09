import os
from pathlib import Path
DOCS_DIR = os.getenv("DOCS_DIR", str(Path(__file__).resolve().parents[3] / "docs"))