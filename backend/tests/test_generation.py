from langchain_core.language_models.fake_chat_models import FakeListChatModel

from document_digester.service.generation import (
    NO_CONTEXT_ANSWER,
    GenerationService,
    format_context,
)


class FakeRetrieval:
    def __init__(self, results):
        self.results = results
        self.calls = []

    def retrieve_hybrid(self, query, k=5):
        self.calls.append((query, k))
        return self.results


RESULTS = [
    {
        "rank": 1,
        "text": "Signals allow nodes to communicate.",
        "metadata": {"title": "Using signals", "Header 2": "Overview", "Header 3": ""},
        "score": 0.03,
    }
]


def test_format_context_numbers_chunks_with_headings():
    context = format_context(RESULTS)

    assert context.startswith("[1] Using signals > Overview\n")
    assert "Signals allow nodes to communicate." in context


def test_answer_uses_llm_with_retrieved_context():
    retrieval = FakeRetrieval(RESULTS)
    llm = FakeListChatModel(responses=["Use signals [1]."])
    service = GenerationService(retrieval, llm=llm)

    result = service.answer("How do nodes talk?", top_k=3)

    assert retrieval.calls == [("How do nodes talk?", 3)]
    assert result["answer"] == "Use signals [1]."
    assert result["sources"] == RESULTS


def test_answer_without_context_skips_llm():
    llm = FakeListChatModel(responses=[])  # would raise if invoked
    service = GenerationService(FakeRetrieval([]), llm=llm)

    result = service.answer("Anything?")

    assert result == {"answer": NO_CONTEXT_ANSWER, "sources": []}
