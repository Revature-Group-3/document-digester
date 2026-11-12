import pytest
from types import SimpleNamespace

from langchain_core.documents import Document

from document_digester.retrieval import RetrievalService


class FakeVectorStore:
    def similarity_search_with_score(self, query, k):
        data = [
            (
                SimpleNamespace(
                    page_content="Godot signals allow nodes to communicate.",
                    metadata={"source": "signals"}
                ),
                0.1
            ),
            (
                SimpleNamespace(
                    page_content="Nodes are arranged in a scene tree.",
                    metadata={"source": "nodes"}
                ),
                0.4
            )
        ]
        return data[:k]


def test_top_k():
    service = RetrievalService(FakeVectorStore())

    results = service.retrieve_top_k(
        "How do nodes communicate?", k=1
    )

    assert len(results) == 1
    assert results[0]["rank"] == 1
    assert results[0]["metadata"]["source"] == "signals"


def test_empty_query():
    service = RetrievalService(FakeVectorStore())

    with pytest.raises(ValueError):
        service.retrieve_top_k("")


def test_invalid_k():
    service = RetrievalService(FakeVectorStore())

    with pytest.raises(ValueError):
        service.retrieve_top_k("test", k=0)


# ---------------------------------------------------------------------------
# Hybrid retrieval tests
# ---------------------------------------------------------------------------

SIGNALS = Document(
    page_content="Signals allow Godot nodes to communicate without directly referencing each other.",
    metadata={"source": "signals"},
)
SCENE_TREE = Document(
    page_content="The scene tree organizes nodes into parent-child relationships.",
    metadata={"source": "scene_tree"},
)
MOVEMENT = Document(
    page_content="CharacterBody2D uses move_and_slide to handle movement and collision.",
    metadata={"source": "movement"},
)
ANIMATION = Document(
    page_content="AnimationPlayer allows you to create and control animations.",
    metadata={"source": "animation"},
)
CORPUS = [SIGNALS, SCENE_TREE, MOVEMENT, ANIMATION]


class RankedVectorStore:
    """Returns a fixed semantic ranking, ignoring the query, so tests can
    control exactly what the vector side contributes."""

    def __init__(self, ranking, corpus=None):
        self.ranking = ranking
        self.corpus = corpus or []
        self.get_calls = 0

    def similarity_search_with_score(self, query, k):
        return [(doc, 0.1 * i) for i, doc in enumerate(self.ranking[:k], start=1)]

    def get(self, include=None):
        self.get_calls += 1
        return {
            "documents": [d.page_content for d in self.corpus],
            "metadatas": [d.metadata for d in self.corpus],
        }

def test_hybrid_scores_are_descending():
    store = RankedVectorStore([SCENE_TREE, SIGNALS, ANIMATION, MOVEMENT])
    service = RetrievalService(store, corpus=CORPUS)

    results = service.retrieve_hybrid("nodes", k=4)
    scores = [r["score"] for r in results]

    assert scores == sorted(scores, reverse=True)
    assert [r["rank"] for r in results] == list(range(1, len(results) + 1))


def test_hybrid_alpha_one_is_semantic_only():
    store = RankedVectorStore([ANIMATION, SIGNALS])
    service = RetrievalService(store, corpus=CORPUS)

    results = service.retrieve_hybrid("CharacterBody2D", k=1, alpha=1.0)

    assert results[0]["metadata"]["source"] == "animation"


def test_hybrid_alpha_zero_is_keyword_only():
    store = RankedVectorStore([ANIMATION, SIGNALS])
    service = RetrievalService(store, corpus=CORPUS)

    results = service.retrieve_hybrid("CharacterBody2D", k=1, alpha=0.0)

    assert results[0]["metadata"]["source"] == "movement"

@pytest.mark.parametrize(
    "kwargs",
    [
        {"query": ""},
        {"query": "   "},
        {"query": "test", "k": 0},
        {"query": "test", "k": 21},
        {"query": "test", "alpha": 1.5},
        {"query": "test", "alpha": -0.1},
        {"query": "test", "k": 10, "fetch_k": 5},
    ],
)
def test_hybrid_invalid_arguments(kwargs):
    service = RetrievalService(RankedVectorStore([SIGNALS]), corpus=CORPUS)

    with pytest.raises(ValueError):
        service.retrieve_hybrid(**kwargs)

#uv run pytest tests/test_retrieval.py -v
