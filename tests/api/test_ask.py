import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.api.models import AskResponse

client = TestClient(app)

def test_ask_success():
    """Test successful /ask request."""
    with patch("app.api.routes.generate_answer") as mock_generate:
        mock_generate.return_value = {
            "answer": "This is a mock answer.",
            "sources": ["CVE-2024-1234"],
            "metadata": [{"id": "CVE-2024-1234", "severity": "CRITICAL"}],
            "formatted_text": "Mock format",
            "confidence": None
        }

        response = client.post("/ask", json={"query": "How does CVE-2024-1234 work?", "filters": {"severity": "CRITICAL"}})

        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "This is a mock answer."
        assert data["sources"] == ["CVE-2024-1234"]
        assert data["metadata"] == [{"id": "CVE-2024-1234", "severity": "CRITICAL"}]
        mock_generate.assert_called_once_with(query="How does CVE-2024-1234 work?", filters={"severity": "CRITICAL"})

def test_ask_empty_query():
    """Test /ask with an empty query (handled by pydantic validation)."""
    response = client.post("/ask", json={"query": ""})

    assert response.status_code == 422
    data = response.json()
    assert "Query cannot be empty" in data["detail"][0]["msg"]

def test_ask_invalid_body():
    """Test /ask with an invalid JSON body."""
    response = client.post("/ask", data="invalid json")

    assert response.status_code == 422

def test_ask_missing_query():
    """Test /ask with missing required query field."""
    response = client.post("/ask", json={"filters": {"severity": "CRITICAL"}})

    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "query"]
    assert data["detail"][0]["type"] == "missing"

def test_ask_pipeline_validation_error():
    """Test /ask when the pipeline raises a ValueError (e.g., no documents found)."""
    with patch("app.api.routes.generate_answer") as mock_generate:
        mock_generate.side_effect = ValueError("No relevant documents found for the given query.")

        response = client.post("/ask", json={"query": "A valid query that returns nothing"})

        assert response.status_code == 400
        assert response.json()["detail"] == "No relevant documents found for the given query."

def test_ask_pipeline_internal_error():
    """Test /ask when the pipeline raises a RuntimeError."""
    with patch("app.api.routes.generate_answer") as mock_generate:
        mock_generate.side_effect = RuntimeError("LLM connection failed.")

        response = client.post("/ask", json={"query": "What is xz?"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

def test_ask_pipeline_unexpected_error():
    """Test /ask when the pipeline raises a generic Exception."""
    with patch("app.api.routes.generate_answer") as mock_generate:
        mock_generate.side_effect = Exception("Unexpected failure")

        response = client.post("/ask", json={"query": "What is xz?"})

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal Server Error"

def test_ask_response_schema_validation():
    """Test that the endpoint enforces AskResponse structure."""
    with patch("app.api.routes.generate_answer") as mock_generate:
        # Return something missing required fields to see if FastAPI throws an internal error
        # (Though technically it returns 500 if response validation fails, but let's test a valid return first)
        mock_generate.return_value = {
            "answer": "Answer only",
            "sources": ["CVE-1"],
            "metadata": [{"id": "CVE-1"}]
        }

        response = client.post("/ask", json={"query": "Schema test"})

        assert response.status_code == 200
        # AskResponse schema checks should pass because the mock return value is valid for the response model
        AskResponse(**response.json())
