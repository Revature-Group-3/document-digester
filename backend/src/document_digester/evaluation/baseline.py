"""Baseline retriever: split the docs/*.txt pages by heading, embed each section, search.

No cleaning, no semantic chunking, no vector database. It searches the same pages as
the real pipeline, so its score is a fair floor for the pipeline to beat.

    uv run --with sentence-transformers python -m document_digester.evaluation.baseline
"""

import argparse
import re
from pathlib import Path

import numpy as np

from document_digester.evaluation.adapter import normalize, normalize_question, page_from_url
from document_digester.evaluation.metrics import evaluate, load_golden_set, relevant_set

REPO_DIR = Path(__file__).resolve().parents[4]
DEFAULT_DOCS = REPO_DIR / "docs"
DEFAULT_GOLDEN = REPO_DIR / "backend" / "eval" / "golden_set.jsonl"
UNDERLINE = re.compile(r"^(=+|-+)$")


def split_sections(txt_path):
    """Yield (page, section, text) for one Sphinx text page.

    Line 1 is the title, line 2 the docs URL, line 3 the title underline.
    Text before the first heading is filed under the page title.
    """
    lines = Path(txt_path).read_text(encoding="utf-8").splitlines()
    title, page = lines[0].strip(), page_from_url(lines[1].strip())

    section, body = title, []
    for i in range(3, len(lines)):
        line = lines[i].strip()
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if line and UNDERLINE.match(nxt) and len(nxt) >= len(line) - 1:
            if body:
                yield page, normalize(section), "\n".join(body)
            section, body = line, []
        elif not UNDERLINE.match(line):
            body.append(lines[i])

    if body:
        yield page, normalize(section), "\n".join(body)


def load_sections(docs_dir):
    sections = []
    for txt in sorted(Path(docs_dir).expanduser().glob("*.txt")):
        sections.extend(split_sections(txt))
    return sections


class BaselineRetriever:
    def __init__(self, sections, embed):
        self.labels = [(page, section) for page, section, _ in sections]
        self.embed = embed
        self.vectors = embed([f"{section}\n{text}" for _, section, text in sections])

    def search(self, query, k=5):
        q = query if isinstance(query, np.ndarray) else self.embed([query])[0]
        top = np.argsort(-(self.vectors @ q))[:k]
        return [self.labels[i] for i in top]


def sentence_transformer_embedder(model_name="all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    return lambda texts: model.encode(texts, normalize_embeddings=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", default=DEFAULT_DOCS)
    parser.add_argument("--golden", default=DEFAULT_GOLDEN)
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    sections = load_sections(args.docs)
    print(f"Loaded {len(sections)} sections from {len({p for p, _, _ in sections})} pages")

    retriever = BaselineRetriever(sections, sentence_transformer_embedder())
    golden = [normalize_question(q) for q in load_golden_set(args.golden)]
    results = {q["id"]: retriever.search(q["question"], args.k) for q in golden}

    for group, stats in evaluate(golden, results, args.k).items():
        print(group, {name: round(value, 3) for name, value in stats.items()})

    print("\nMisses:")
    for q in golden:
        if not relevant_set(q) & set(results[q["id"]]):
            print(f"  {q['id']} {q['question']}")
            print(f"     expected: {q['page']} > {q['section']}")
            print(f"     got #1:   {' > '.join(results[q['id']][0])}")


if __name__ == "__main__":
    main()
