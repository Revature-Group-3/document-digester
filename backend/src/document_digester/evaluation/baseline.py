"""Baseline retriever: split raw .rst pages by heading, embed, search.

Gives the evaluation harness real results before the team pipeline exists,
and a floor for the team pipeline to beat.

    uv run --with sentence-transformers python -m document_digester.evaluation.baseline ~/IdeaProjects/godot-docs
"""

import argparse
import re
from pathlib import Path

import numpy as np

from document_digester.evaluation.metrics import evaluate, load_golden_set, relevant_set

UNDERLINE = re.compile(r"^([=\-~^\"#*+])\1{2,}$")
DEFAULT_GOLDEN = Path(__file__).resolve().parents[3] / "eval" / "golden_set.jsonl"


def split_sections(rst_path, docs_root):
    """Yield (page, section, text) for each heading in one .rst file."""
    page = rst_path.relative_to(docs_root).with_suffix("").as_posix()
    lines = rst_path.read_text(encoding="utf-8").splitlines()

    section, body = None, []
    for i, line in enumerate(lines):
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        title = line.strip()
        if title and UNDERLINE.match(nxt) and len(nxt) >= len(title) - 1 and not UNDERLINE.match(title):
            if section and body:
                yield page, section, "\n".join(body)
            section, body = title, []
        elif section and not UNDERLINE.match(title):
            body.append(line)

    if section and body:
        yield page, section, "\n".join(body)


def load_sections(docs_root):
    docs_root = Path(docs_root).expanduser()
    sections = []
    for rst in sorted(docs_root.rglob("*.rst")):
        sections.extend(split_sections(rst, docs_root))
    return sections


class BaselineRetriever:
    def __init__(self, sections, embed):
        self.labels = [(page, section) for page, section, _ in sections]
        texts = [f"{section}\n{text}" for _, section, text in sections]
        self.embed = embed
        self.vectors = embed(texts)
        self.is_class = np.array([page.startswith("classes/") for page, _ in self.labels])

    def search(self, query, k=5, class_penalty=0.0):
        """Rank sections for a query.

        class_penalty is subtracted from the score of class reference pages.
        Use float("inf") to exclude them entirely.
        """
        q = query if isinstance(query, np.ndarray) else self.embed([query])[0]
        scores = self.vectors @ q
        if class_penalty:
            scores = np.where(self.is_class, scores - class_penalty, scores)
        top = np.argsort(-scores)[:k]
        return [self.labels[i] for i in top]


def sentence_transformer_embedder(model_name="all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)

    def embed(texts):
        return model.encode(texts, normalize_embeddings=True, show_progress_bar=len(texts) > 100)

    return embed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("docs_root", help="path to a godot-docs checkout")
    parser.add_argument("--golden", default=DEFAULT_GOLDEN)
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument(
        "--class-penalties",
        type=float,
        nargs="+",
        default=[0.0, 0.03, 0.05, 0.1, float("inf")],
        help="penalties to compare for classes/ pages (inf = exclude)",
    )
    args = parser.parse_args()

    sections = load_sections(args.docs_root)
    print(f"Loaded {len(sections)} sections")

    retriever = BaselineRetriever(sections, sentence_transformer_embedder())
    golden = load_golden_set(args.golden)
    query_vectors = retriever.embed([q["question"] for q in golden])

    def run(penalty):
        return {
            q["id"]: retriever.search(vec, args.k, class_penalty=penalty)
            for q, vec in zip(golden, query_vectors)
        }

    def found(results):
        return {q["id"] for q in golden if relevant_set(q) & set(results[q["id"]])}

    baseline_results = run(0.0)
    baseline_found = found(baseline_results)

    print(f"\n{'class penalty':<14}{'hit@' + str(args.k):>8}{'mrr':>8}   changes vs no penalty")
    for penalty in args.class_penalties:
        results = run(penalty)
        stats = evaluate(golden, results, args.k)["all"]
        now_found = found(results)
        fixed = sorted(now_found - baseline_found)
        broke = sorted(baseline_found - now_found)
        label = "exclude" if penalty == float("inf") else f"{penalty:g}"
        changes = " ".join([f"+{q}" for q in fixed] + [f"-{q}" for q in broke]) or "-"
        print(f"{label:<14}{stats[f'hit@{args.k}']:>8.3f}{stats['mrr']:>8.3f}   {changes}")

    print("\nMisses with no penalty:")
    for q in golden:
        if q["id"] not in baseline_found:
            print(f"  {q['id']} {q['question']}")
            print(f"     expected: {q['page']} > {q['section']}")
            print(f"     got #1:   {' > '.join(baseline_results[q['id']][0])}")


if __name__ == "__main__":
    main()
