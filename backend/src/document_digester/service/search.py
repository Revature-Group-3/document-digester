from sqlalchemy import select, or_

from document_digester.db.database import DatabaseNotConfiguredError, SessionLocal
from document_digester.domain.user_story import UserStory


class SearchService:
    def __init__(self, retrieval_service):
        self.retrieval_service = retrieval_service

    def vector_search(self, query: str, top_k: int):
        return self.retrieval_service.retrieve_top_k(query, k=top_k)

    def hybrid_search(self, query: str, top_k: int):
        return self.retrieval_service.retrieve_hybrid(query, k=top_k)

    def sql_search(self, query: str, top_k: int):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= top_k <= 20:
            raise ValueError("k must be between 1 and 20")

        search_term = f"%{query.strip()}%"

        with SessionLocal() as db:
            statement = (
                select(UserStory)
                .where(
                    or_(
                        UserStory.title.ilike(search_term),
                        UserStory.description.ilike(search_term)
                    )
                )
                .limit(top_k)
            )

            stories = db.scalars(statement).all()

            return [
                {
                    "text": f"{story.title}\n{story.description or ''}",
                    "metadata": {
                        "title": story.title,
                        "source_name": "PostgreSQL User Stories"
                    },
                    "score": None
                }
                for story in stories
            ]

    def combined_search(self, query: str, top_k: int):
        vector_results = self.vector_search(query, top_k)
        try:
            sql_results = self.sql_search(query, top_k)
        except DatabaseNotConfiguredError:
            sql_results = []

        combined = []

        for i in range(max(len(vector_results), len(sql_results))):
            if i < len(vector_results):
                combined.append(vector_results[i])

            if i < len(sql_results):
                combined.append(sql_results[i])

        return combined[:top_k]
