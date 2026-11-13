from fastapi.testclient import TestClient

from document_digester.api.main import app
from document_digester.api.routers.search import get_search_service


class FakeSearchService:

    def vector_search(self, query: str, top_k: int):
        return [
            {
                "rank": 1,
                "text": "Godot nodes are the basic building blocks of a scene.",
                "metadata": {
                    "title": "Nodes",
                    "Header 2": "Introduction",
                    "Header 3": "Node basics",
                    "source": "https://docs.godotengine.org/"
                },
                "distance": 0.25
            }
        ][:top_k]

    def hybrid_search(self, query: str, top_k: int):
        return [
            {
                "rank": 1,
                "text": "Godot scenes contain a hierarchy of nodes.",
                "metadata": {
                    "title": "Scenes",
                    "Header 2": "Introduction",
                    "source": "https://docs.godotengine.org/"
                },
                "score": 0.85
            }
        ][:top_k]


app.dependency_overrides[get_search_service] = (
    lambda: FakeSearchService()
)

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_vector_search():
    response = client.post(
        "/api/search/vector",
        json={
            "query": "What are Godot nodes?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "What are Godot nodes?"
    assert len(data["results"]) == 1
    assert "Godot nodes" in data["results"][0]["content"]


def test_hybrid_search():
    response = client.post(
        "/api/search/hybrid",
        json={
            "query": "How do Godot scenes work?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["results"]) == 1
    assert data["results"][0]["score"] == 0.85


def test_invalid_top_k():
    response = client.post(
        "/api/search/vector",
        json={
            "query": "Godot nodes",
            "top_k": 25
        }
    )

    assert response.status_code == 422


def test_empty_query():
    response = client.post(
        "/api/search/vector",
        json={
            "query": "",
            "top_k": 5
        }
    )

    assert response.status_code == 422
