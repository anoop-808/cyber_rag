import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_retrieval_pipeline, get_llm_client

def mock_retrieval_pipeline(query: str, filters: dict = None):
    return [{"id": "CVE-123", "description": "test", "metadata": {}, "distance": 0.1}]

def mock_llm_client(system_prompt: str, user_prompt: str):
    return "This is a mock answer."

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_dependencies():
    app.dependency_overrides[get_retrieval_pipeline] = lambda: mock_retrieval_pipeline
    app.dependency_overrides[get_llm_client] = lambda: mock_llm_client
    yield
    app.dependency_overrides.clear()

def test_ask_endpoint():
    response = client.post("/ask", json={"query": "test query"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["answer"] == "This is a mock answer."
    assert "sources" in data
    assert "metadata" in data
    assert data["sources"] == ["CVE-123"]

def test_lifespan_events():
    with TestClient(app) as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "CyberRAG API is running"}

def test_search_endpoint():
    response = client.post("/search", json={"query": "test search query"})
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert len(data["documents"]) == 1
    assert data["documents"][0]["id"] == "CVE-123"
    assert data["documents"][0]["description"] == "test"

def test_ask_validation_error():
    # Empty query should fail validation
    response = client.post("/ask", json={"query": ""})
    assert response.status_code == 422

    # Missing required 'query' field
    response = client.post("/ask", json={"filters": {}})
    assert response.status_code == 422

    # Malformed JSON body
    response = client.post("/ask", data="not a json")
    assert response.status_code == 422

def test_search_validation_error():
    # Empty query should fail validation
    response = client.post("/search", json={"query": ""})
    assert response.status_code == 422

    # Missing required 'query' field
    response = client.post("/search", json={"filters": {}})
    assert response.status_code == 422

    # Malformed JSON body
    response = client.post("/search", data="not a json")
    assert response.status_code == 422
