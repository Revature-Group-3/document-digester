from time import perf_counter

class RetrievalService:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_top_k(self, query: str, k: int = 5):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= k <= 20:
            raise ValueError("k must be between 1 and 20")

        #To measure the latency
        start = perf_counter()

        matches = self.vector_store.similarity_search_with_score(
            query, k=k
        )

        #Latency results
        elapsed_ms = (perf_counter() - start) * 1000
        print(f"Retreival Latency: {elapsed_ms:.2f} ms")
        
        #We can return latency anywhere by grabbing the elapsed_ms

        return [
            {
                "rank": index,
                "text": document.page_content,
                "metadata": document.metadata,
                "distance": float(distance)
            }
            for index, (document, distance)
            in enumerate(matches, start=1)
        ]
