
from document_digester.models import SearchResult
from document_digester.retrieval import RetrievalService
from document_digester.service.ingestion.vectorization import create_vector_store

vector_store = create_vector_store()
retrieval_service = RetrievalService(vector_store)


def search_documents(query: str, top_k: int) -> list[SearchResult]:
    results = retrieval_service.retrieve_hybrid(query, k=top_k)

    search_results = []

    for result in results:
        metadata = result["metadata"]

        section = " > ".join(
            part for part in [
                metadata.get("Header 2", ""),
                metadata.get("Header 3", "")
            ] if part
        )

        search_results.append(
            SearchResult(
                content=result["text"],
                score=result["score"],
                source=metadata.get("title", "Godot Documentation"),
                section=section or metadata.get("title", ""),
                url=metadata.get("source")
            )
        )

    return search_results
