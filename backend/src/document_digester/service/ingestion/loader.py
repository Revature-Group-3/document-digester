import json
from pathlib import Path

from document_digester.settings import DOCS_DIR

def read_page(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    return {
        "title": data.get("title", ""),
        "body": data.get("body", ""),
        "source": data.get("current_page_name", path.stem),
    }


def load_pages() -> list[dict]:
    return [read_page(path) for path in Path(DOCS_DIR).rglob("*.fjson")]