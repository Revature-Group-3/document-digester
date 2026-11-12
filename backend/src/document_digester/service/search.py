from document_digester.models import SearchResult

def search_documents(query: str, top_k: int) -> list[SearchResult]:
     # TODO: Replace mock results with RetrievalService.retrieve_hybrid()
    # once the vector store is initialized.

    mock_results = [
        SearchResult(
            content="Signals allow nodes to communicate with one another.",
            score=0.95,
            source="Godot Documentation",
            section="Using Signals",
            url="https://docs.godotengine.org/"
        ),
        SearchResult(
            content="Nodes can emit signals when events occur.",
            score=0.87,
            source="Godot Documentation",
            section="Signals",
            url="https://docs.godotengine.org/"
        )
    ]

    return mock_results[:top_k]
