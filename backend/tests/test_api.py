from fastapi.testclient import TestClient
from document_digester.main import app
from document_digester.models import SearchResult
from document_digester import main

client = TestClient(app)


def mock_search_documents(query, top_k):
    results = [
        SearchResult(
            content="Signals allow nodes to communicate.",
            score=0.95,
            source="Godot Documentation",
            section="Using Signals",
            url="https://docs.godotengine.org/"
        ),
        SearchResult(
            content="Nodes can emit signals.",
            score=0.87,
            source="Godot Documentation",
            section="Signals",
            url="https://docs.godotengine.org/"
        )
    ]

    return results[:top_k]

main.search_documents = mock_search_documents

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Documentation Digester API"


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search():
    response = client.post(
        "/api/search",
        json={"query": "Godot signals", "top_k": 2}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Godot signals"
    assert len(data["results"]) == 2


def test_search_top_k():
    response = client.post(
        "/api/search",
        json={"query": "Godot signals", "top_k": 1}
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) == 1


def test_invalid_top_k():
    response = client.post(
        "/api/search",
        json={"query": "Godot signals", "top_k": 0}
    )
    assert response.status_code == 422


def test_empty_search():
    response = client.post(
        "/api/search",
        json={"query": "   ", "top_k": 5}
    )
    assert response.status_code == 400


def test_missing_query():
    response = client.post(
        "/api/search",
        json={"top_k": 5}
    )
    assert response.status_code == 422


def test_max_top_k():
    response = client.post(
        "/api/search",
        json={"query": "Godot signals", "top_k": 20}
    )
    assert response.status_code == 200


def test_top_k_too_large():
    response = client.post(
        "/api/search",
        json={"query": "Godot signals", "top_k": 21}
    )
    assert response.status_code == 422
