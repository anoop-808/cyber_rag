import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from app.api.models import SearchResponse

client = TestClient(app)

def test_search_success():
    """Test successful POST /search request."""
    with patch("app.api.routes.retrieve") as mock_retrieve:
        mock_retrieve.return_value = [
            {"id": "CVE-2024-1234", "description": "Buffer overflow", "metadata": {"severity": "HIGH"}, "distance": 0.123}
        ]

        response = client.post("/search", json={"query": "Buffer overflow in OpenSSL", "filters": {"severity": "HIGH"}})

        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert len(data["documents"]) == 1
        assert data["documents"][0]["id"] == "CVE-2024-1234"
        mock_retrieve.assert_called_once_with(query="Buffer overflow in OpenSSL", filters={"severity": "HIGH"})

def test_search_empty_query():
    """Test POST /search with an empty query (handled by pydantic validation)."""
    response = client.post("/search", json={"query": ""})

    assert response.status_code == 422
    data = response.json()
    assert "Query cannot be empty" in data["detail"][0]["msg"]

def test_search_invalid_body():
    """Test POST /search with an invalid JSON body."""
    response = client.post("/search", data="invalid json")

    assert response.status_code == 422

def test_search_missing_query():
    """Test POST /search with missing required query field."""
    response = client.post("/search", json={"filters": {"severity": "HIGH"}})

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "query"]
    assert data["detail"][0]["type"] == "missing"

def test_search_retrieval_failure():
    """Test POST /search when retrieval raises a ValueError."""
    with patch("app.api.routes.retrieve") as mock_retrieve:
        mock_retrieve.side_effect = ValueError("Invalid filter value")

        response = client.post("/search", json={"query": "A valid query"})

        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid filter value"

def test_search_internal_error():
    """Test POST /search when retrieval raises a RuntimeError."""
    with patch("app.api.routes.retrieve") as mock_retrieve:
        mock_retrieve.side_effect = RuntimeError("Database connection failed")

        response = client.post("/search", json={"query": "What is xz?"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

def test_search_generic_error():
    """Test POST /search when retrieval raises a generic Exception."""
    with patch("app.api.routes.retrieve") as mock_retrieve:
        mock_retrieve.side_effect = Exception("Unexpected failure")

        response = client.post("/search", json={"query": "What is xz?"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

def test_search_response_schema_validation():
    """Test that the endpoint enforces SearchResponse structure."""
    with patch("app.api.routes.retrieve") as mock_retrieve:
        mock_retrieve.return_value = [
            {"id": "CVE-2024-1234", "description": "Description here"}
        ]

        response = client.post("/search", json={"query": "Schema test"})

        assert response.status_code == 200
        # SearchResponse schema checks should pass
        SearchResponse(**response.json())
