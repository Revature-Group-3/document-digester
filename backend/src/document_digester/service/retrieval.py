import re
from time import perf_counter

from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


def _tokenize(text: str) -> list[str]:
    # \w+ keeps identifiers like move_and_slide and CharacterBody2D intact
    return re.findall(r"\w+", text.lower())


class RetrievalService:
    def __init__(self, vector_store, corpus: list[Document] | None = None):
        self.vector_store = vector_store
        self._bm25 = None
        self._bm25_docs: list[Document] = []
        if corpus is not None:
            self.build_keyword_index(corpus)

    @staticmethod
    def _validate(query: str, k: int):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= k <= 20:
            raise ValueError("k must be between 1 and 20")

    # On first run of retrieveHybrid(), this builds the keyword index from existing chunks
    # Run again if new chunks are added to update the keyword list
    def build_keyword_index(self, docs: list[Document] | None = None):
        if docs is None:
            data = self.vector_store.get(include=["documents", "metadatas"])
            docs = [
                Document(page_content=text, metadata=meta or {})
                for text, meta in zip(data["documents"], data["metadatas"])
            ]

        self._bm25_docs = list(docs)
        self._bm25 = (
            BM25Okapi([_tokenize(d.page_content) for d in self._bm25_docs])
            if self._bm25_docs
            else None
        )

    def _keyword_search(self, query: str, k: int):
        if self._bm25 is None:
            return []

        scores = self._bm25.get_scores(_tokenize(query))
        top = sorted(range(len(scores)), key=scores.__getitem__, reverse=True)[:k]
        return [(self._bm25_docs[i], float(scores[i])) for i in top if scores[i] > 0]

    def retrieve_top_k(self, query: str, k: int = 5):
        self._validate(query, k)

        #To measure the latency
        start = perf_counter()

        matches = self.vector_store.similarity_search_with_score(
            query, k=k
        )

        #Latency results
        elapsed_ms = (perf_counter() - start) * 1000
        print(f"Retrieval Latency: {elapsed_ms:.2f} ms")
        
        #We can return latency anywhere by grabbing the elapsed_ms

        return [
            {
                "rank": index,
                "text": document.page_content,
                "metadata": document.metadata,
                "distance": float(distance),
                # Lower distance = closer match; expose a 0..1 "higher is better"
                # score so the API's `score` field is populated for vector search.
                "score": 1.0 / (1.0 + float(distance)),
            }
            for index, (document, distance)
            in enumerate(matches, start=1)
        ]

    # Combines semantic and keyword search using rrf (reciprocal rank fusion)
    # 'alpha' is the fusion weight (0 = keyword only, 1 = semantic only)
    # we may need to tweak this to see what gives us the best results
    def retrieve_hybrid(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20,
        alpha: float = 0.5,
        rrf_k: int = 60,
    ):
        self._validate(query, k)

        if not 0 <= alpha <= 1:
            raise ValueError("alpha must be between 0 and 1")

        if fetch_k < k:
            raise ValueError("fetch_k must be greater than or equal to k")

        if self._bm25 is None:
            self.build_keyword_index()

        start = perf_counter()

        semantic = self.vector_store.similarity_search_with_score(query, k=fetch_k)
        keyword = self._keyword_search(query, fetch_k)

        # This performs the rrf, using rank rather than the incompatible score/distance values
        # of the two search strategies 
        fused: dict[str, dict] = {}
        for weight, results in ((alpha, semantic), (1 - alpha, keyword)):
            for rank, (doc, _) in enumerate(results, start=1):
                entry = fused.setdefault(doc.page_content, {"doc": doc, "score": 0.0})
                entry["score"] += weight / (rrf_k + rank)

        ranked = sorted(fused.values(), key=lambda e: e["score"], reverse=True)[:k]

        elapsed_ms = (perf_counter() - start) * 1000
        print(f"Hybrid Retrieval Latency: {elapsed_ms:.2f} ms")

        return [
            {
                "rank": index,
                "text": entry["doc"].page_content,
                "metadata": entry["doc"].metadata,
                "score": entry["score"],
            }
            for index, entry in enumerate(ranked, start=1)
        ]
