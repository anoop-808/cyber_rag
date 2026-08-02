import json
import pytest
from pydantic import ValidationError

from app.api.models import AskRequest, AskResponse, SearchRequest, SearchResponse


def test_ask_request_valid():
    """Test valid AskRequest creation."""
    request = AskRequest(query="How does CVE-2024-1234 work?", filters={"severity": "CRITICAL"})
    assert request.query == "How does CVE-2024-1234 work?"
    assert request.filters == {"severity": "CRITICAL"}


def test_ask_request_valid_no_filters():
    """Test valid AskRequest creation without filters."""
    request = AskRequest(query="How does CVE-2024-1234 work?")
    assert request.query == "How does CVE-2024-1234 work?"
    assert request.filters is None


def test_ask_request_empty_query():
    """Test that empty query raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        AskRequest(query="")
    assert "Query cannot be empty" in str(exc_info.value)

    with pytest.raises(ValidationError) as exc_info:
        AskRequest(query="   ")
    assert "Query cannot be empty" in str(exc_info.value)


def test_ask_request_missing_query():
    """Test that missing query raises ValidationError."""
    with pytest.raises(ValidationError):
        AskRequest()


def test_ask_request_serialization():
    """Test AskRequest JSON serialization."""
    request = AskRequest(query="Test query", filters={"key": "value"})
    json_data = request.model_dump_json()
    parsed = json.loads(json_data)
    assert parsed["query"] == "Test query"
    assert parsed["filters"] == {"key": "value"}


def test_ask_response_valid():
    """Test valid AskResponse creation."""
    response = AskResponse(
        answer="This is the answer.",
        sources=["CVE-2024-1234"],
        metadata=[{"id": "CVE-2024-1234", "severity": "CRITICAL"}],
        confidence=0.95
    )
    assert response.answer == "This is the answer."
    assert response.sources == ["CVE-2024-1234"]
    assert response.metadata == [{"id": "CVE-2024-1234", "severity": "CRITICAL"}]
    assert response.confidence == 0.95


def test_ask_response_valid_no_confidence():
    """Test valid AskResponse creation without confidence."""
    response = AskResponse(
        answer="This is the answer.",
        sources=["CVE-2024-1234"],
        metadata=[{"id": "CVE-2024-1234", "severity": "CRITICAL"}]
    )
    assert response.confidence is None


def test_ask_response_missing_fields():
    """Test that missing required fields raises ValidationError."""
    with pytest.raises(ValidationError):
        AskResponse(sources=[], metadata=[])  # Missing answer


def test_ask_response_serialization():
    """Test AskResponse JSON serialization."""
    response = AskResponse(
        answer="Answer",
        sources=["ID"],
        metadata=[{"k": "v"}]
    )
    json_data = response.model_dump_json()
    parsed = json.loads(json_data)
    assert parsed["answer"] == "Answer"
    assert parsed["sources"] == ["ID"]
    assert parsed["metadata"] == [{"k": "v"}]
    assert parsed.get("confidence") is None


def test_search_request_valid():
    """Test valid SearchRequest creation."""
    request = SearchRequest(query="Buffer overflow", filters={"severity": "HIGH"})
    assert request.query == "Buffer overflow"
    assert request.filters == {"severity": "HIGH"}


def test_search_request_empty_query():
    """Test that empty query raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        SearchRequest(query="")
    assert "Query cannot be empty" in str(exc_info.value)


def test_search_request_missing_query():
    """Test that missing query raises ValidationError."""
    with pytest.raises(ValidationError):
        SearchRequest()


def test_search_request_serialization():
    """Test SearchRequest JSON serialization."""
    request = SearchRequest(query="Test search")
    json_data = request.model_dump_json()
    parsed = json.loads(json_data)
    assert parsed["query"] == "Test search"
    assert parsed.get("filters") is None


def test_search_response_valid():
    """Test valid SearchResponse creation."""
    response = SearchResponse(
        documents=[
            {
                "id": "CVE-2024-1234",
                "description": "Buffer overflow",
                "metadata": {"severity": "HIGH"}
            }
        ]
    )
    assert len(response.documents) == 1
    assert response.documents[0]["id"] == "CVE-2024-1234"


def test_search_response_missing_documents():
    """Test that missing documents field raises ValidationError."""
    with pytest.raises(ValidationError):
        SearchResponse()


def test_search_response_serialization():
    """Test SearchResponse JSON serialization."""
    response = SearchResponse(documents=[{"id": "1"}])
    json_data = response.model_dump_json()
    parsed = json.loads(json_data)
    assert len(parsed["documents"]) == 1
    assert parsed["documents"][0]["id"] == "1"
