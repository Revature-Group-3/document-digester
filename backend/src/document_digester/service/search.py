class SearchService:

    def __init__(self, retrieval_service):
        self.retrieval_service = retrieval_service

    def vector_search(self, query: str, top_k: int):
        return self.retrieval_service.retrieve_top_k(
            query,
            k=top_k
        )

    def hybrid_search(self, query: str, top_k: int):
        return self.retrieval_service.retrieve_hybrid(
            query,
            k=top_k
        )
