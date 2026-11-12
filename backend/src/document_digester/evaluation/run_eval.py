"""Running the question set against the team's RetrievalService and report precision, latency and provenance.

Needs Ollama running with the embedding model pulled, and the Chroma index built.

    uv run python -m document_digester.evaluation.run_eval
"""

import argparse
import contextlib
import io
import os
import statistics
from pathlib import Path
from time import perf_counter

from document_digester.evaluation.adapter import chunk_labels, normalize_question, page_from_url
from document_digester.evaluation.metrics import evaluate, load_golden_set, relevant_set

BACKEND_DIR = Path(__file__).resolve().parents[3]
DEFAULT_GOLDEN = BACKEND_DIR / "eval" / "golden_set.jsonl"
DEFAULT_CHROMA_DIR = BACKEND_DIR / "data" / "chroma"


def label_results(results, relevant):
    """Pick one label per result: the one that matches the answer if any, else the most specific."""
    labels = []
    for result in results:
        options = chunk_labels(result["metadata"])
        match = next((label for label in options if label in relevant), None)
        labels.append(match or (options[0] if options else ("", "")))
    return labels


def has_provenance(result):
    meta = result["metadata"]
    return bool(page_from_url(meta.get("source"))) and any(
        meta.get(key) for key in ("Header 2", "Header 3", "title")
    )


def run_mode(search, golden, k):
    """search(query, k) -> list of result dicts with "metadata", like RetrievalService returns."""
    labeled, latencies, provenance = {}, [], []
    for question in golden:
        start = perf_counter()
        with contextlib.redirect_stdout(io.StringIO()):  # retrieval prints its own latency
            results = search(question["question"], k)
        latencies.append((perf_counter() - start) * 1000)
        provenance.extend(has_provenance(r) for r in results)
        labeled[question["id"]] = label_results(results, relevant_set(question))

    summary = evaluate(golden, labeled, k)
    summary["latency_ms"] = {
        "p50": statistics.median(latencies),
        "p95": statistics.quantiles(latencies, n=20)[-1] if len(latencies) > 1 else latencies[0],
    }
    summary["provenance"] = sum(provenance) / len(provenance) if provenance else 0.0
    return summary


def indexed_pages(vector_store):
    metadatas = vector_store.get(include=["metadatas"])["metadatas"]
    return {page_from_url((m or {}).get("source")) for m in metadatas} - {None}


def answerable(golden, pages):
    """Questions whose correct section's page is actually in the index."""
    return [q for q in golden if any(page in pages for page, _ in relevant_set(q))]


def build_retriever(chroma_dir, collection):
    from langchain_chroma import Chroma
    from langchain_ollama import OllamaEmbeddings

    from document_digester.retrieval import RetrievalService

    embeddings = OllamaEmbeddings(model=os.getenv("EMBEDDING_MODEL", "all-minilm"))
    store = Chroma(collection_name=collection, embedding_function=embeddings, persist_directory=str(chroma_dir))
    return store, RetrievalService(store)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", default=DEFAULT_GOLDEN)
    parser.add_argument("--chroma-dir", default=os.getenv("CHROMA_PERSIST_DIRECTORY", DEFAULT_CHROMA_DIR))
    parser.add_argument("--collection", default="godot_docs")
    parser.add_argument("-k", type=int, default=5)
    parser.add_argument("--alphas", type=float, nargs="+", default=[0.0, 0.25, 0.5, 0.75, 1.0])
    args = parser.parse_args()

    store, retriever = build_retriever(args.chroma_dir, args.collection)
    pages = indexed_pages(store)
    golden = [normalize_question(q) for q in load_golden_set(args.golden)]
    scored = answerable(golden, pages)
    print(f"Index covers {len(pages)} pages; {len(scored)} of {len(golden)} questions are answerable")
    if not scored:
        return

    modes = {"semantic": lambda q, k: retriever.retrieve_top_k(q, k)}
    for alpha in args.alphas:
        modes[f"hybrid a={alpha:g}"] = lambda q, k, a=alpha: retriever.retrieve_hybrid(q, k, alpha=a)

    hit = f"hit@{args.k}"
    print(f"\n{'mode':<16}{hit:>8}{'mrr':>8}{'p50 ms':>9}{'p95 ms':>9}{'provenance':>12}")
    for name, search in modes.items():
        s = run_mode(search, scored, args.k)
        print(
            f"{name:<16}{s['all'][hit]:>8.3f}{s['all']['mrr']:>8.3f}"
            f"{s['latency_ms']['p50']:>9.1f}{s['latency_ms']['p95']:>9.1f}{s['provenance']:>12.0%}"
        )


if __name__ == "__main__":
    main()
