from pathlib import Path

from document_digester.settings import settings


def read_page(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        data = f.read()
        lines = data.splitlines()

    return {
        "title": lines[0],
        "source": lines[1],
        "body": "\n".join(lines[3:])
    }

def load_pages() -> list[dict]:
    return [read_page(path) for path in Path(settings.DOCS_DIR).rglob("*.txt")]