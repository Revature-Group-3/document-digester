import pytest

from document_digester.evaluation.metrics import (
    evaluate,
    hit_at_k,
    precision_at_k,
    reciprocal_rank,
)

SIGNALS = ("getting_started/step_by_step/signals", "Connecting a signal via code")
TIMER = ("classes/class_timer", "Signals")
OTHER = ("tutorials/io/saving_games", "Serializing")


def test_reciprocal_rank():
    assert reciprocal_rank([SIGNALS, OTHER], {SIGNALS}) == 1.0
    assert reciprocal_rank([OTHER, SIGNALS], {SIGNALS}) == 0.5
    assert reciprocal_rank([OTHER, OTHER, SIGNALS], {SIGNALS}) == pytest.approx(1 / 3)
    assert reciprocal_rank([OTHER], {SIGNALS}) == 0.0
    assert reciprocal_rank([], {SIGNALS}) == 0.0


def test_hit_at_k_only_looks_at_top_k():
    ranked = [OTHER, OTHER, SIGNALS]
    assert hit_at_k(ranked, {SIGNALS}, k=3)
    assert not hit_at_k(ranked, {SIGNALS}, k=2)


def test_precision_counts_every_relevant_result():
    ranked = [SIGNALS, OTHER, SIGNALS, OTHER]
    assert precision_at_k(ranked, {SIGNALS}, k=4) == 0.5


def test_evaluate_averages_and_groups_by_type():
    golden = [
        {"id": "q1", "page": SIGNALS[0], "section": SIGNALS[1], "type": "direct"},
        {"id": "q2", "page": TIMER[0], "section": TIMER[1], "type": "paraphrase"},
    ]
    results = {
        "q1": [SIGNALS, OTHER],  # found at rank 1
        "q2": [OTHER, TIMER],    # found at rank 2
    }

    summary = evaluate(golden, results, k=2)

    assert summary["all"]["hit@2"] == 1.0
    assert summary["all"]["mrr"] == 0.75
    assert summary["direct"]["mrr"] == 1.0
    assert summary["paraphrase"]["mrr"] == 0.5


def test_missing_results_count_as_misses():
    golden = [{"id": "q1", "page": SIGNALS[0], "section": SIGNALS[1], "type": "direct"}]

    summary = evaluate(golden, {}, k=5)

    assert summary["all"]["hit@5"] == 0.0
    assert summary["all"]["mrr"] == 0.0
