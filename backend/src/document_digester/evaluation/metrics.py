import json
from collections import defaultdict
from pathlib import Path


def load_golden_set(path):
    with Path(path).open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def relevant_set(question):
    """The (page, section) pairs that count as a correct answer."""
    pairs = {(question["page"], question["section"])}
    pairs.update(tuple(pair) for pair in question.get("also_relevant", []))
    return pairs

def reciprocal_rank(ranked, relevant):
    for position, item in enumerate(ranked, start=1):
        if item in relevant:
            return 1 / position
    return 0.0


def hit_at_k(ranked, relevant, k):
    return any(item in relevant for item in ranked[:k])


def precision_at_k(ranked, relevant, k):
    return sum(item in relevant for item in ranked[:k]) / k


def evaluate(golden_set, results, k=5):
    """Score ranked results against the golden set.

    results maps question id -> ranked list of (page, section) tuples.
    A question with no results counts as a miss.
    """
    scores = defaultdict(list)

    for question in golden_set:
        relevant = relevant_set(question)
        ranked = results.get(question["id"], [])

        row = {
            "hit": hit_at_k(ranked, relevant, k),
            "rr": reciprocal_rank(ranked, relevant),
            "precision": precision_at_k(ranked, relevant, k),
        }
        scores["all"].append(row)
        scores[question["type"]].append(row)

    summary = {}
    for group, rows in scores.items():
        n = len(rows)
        summary[group] = {
            "questions": n,
            f"hit@{k}": sum(r["hit"] for r in rows) / n,
            "mrr": sum(r["rr"] for r in rows) / n,
            f"precision@{k}": sum(r["precision"] for r in rows) / n,
        }
    return summary
