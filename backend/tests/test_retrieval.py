
import pytest
from types import SimpleNamespace

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

#uv run pytest tests/test_retrieval.py -v
