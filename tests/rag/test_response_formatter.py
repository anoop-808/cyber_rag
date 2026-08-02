import pytest
from app.rag.response_formatter import format_response

def test_format_response_valid_input():
    llm_response = "This is a detailed explanation of the vulnerability."
    retrieved_documents = [
        {"id": "CVE-2024-1234", "severity": "HIGH", "metadata": {"cvss_score": 8.5}},
        {"id": "CVE-2024-5678", "metadata": {"severity": "CRITICAL", "publication_year": 2024}}
    ]

    result = format_response(llm_response, retrieved_documents)

    assert "answer" in result
    assert result["answer"] == llm_response

    assert "sources" in result
    assert "CVE-2024-1234" in result["sources"]
    assert "CVE-2024-5678" in result["sources"]

    assert "metadata" in result
    assert len(result["metadata"]) == 2
    assert result["metadata"][0]["id"] == "CVE-2024-1234"
    assert result["metadata"][0]["severity"] == "HIGH"
    assert result["metadata"][0]["cvss"] == 8.5
    assert result["metadata"][1]["id"] == "CVE-2024-5678"
    assert result["metadata"][1]["severity"] == "CRITICAL"
    assert result["metadata"][1]["published"] == 2024

    assert "formatted_text" in result
    assert result["formatted_text"] == "Answer\n\nThis is a detailed explanation of the vulnerability.\n\nSources\n\n- CVE-2024-1234\n- CVE-2024-5678"

def test_format_response_empty_llm_response():
    with pytest.raises(ValueError, match="LLM response cannot be empty."):
        format_response("", [{"id": "CVE-2024-1234"}])

    with pytest.raises(ValueError, match="LLM response cannot be empty."):
        format_response("   ", [{"id": "CVE-2024-1234"}])

def test_format_response_empty_retrieved_documents():
    with pytest.raises(ValueError, match="Retrieved documents cannot be empty or missing."):
        format_response("Valid response", [])

def test_format_response_missing_retrieved_documents():
    with pytest.raises(ValueError, match="Retrieved documents cannot be empty or missing."):
        format_response("Valid response", None)

def test_format_response_invalid_metadata_missing_id():
    llm_response = "Valid response"
    retrieved_documents = [{"description": "No ID here"}]
    with pytest.raises(ValueError, match="Invalid metadata: Document must contain an 'id'."):
        format_response(llm_response, retrieved_documents)

def test_format_response_duplicate_sources():
    llm_response = "Explanation"
    retrieved_documents = [
        {"id": "CVE-2024-1234"},
        {"id": "CVE-2024-1234"}
    ]

    result = format_response(llm_response, retrieved_documents)

    assert result["sources"] == ["CVE-2024-1234"]
    assert result["formatted_text"] == "Answer\n\nExplanation\n\nSources\n\n- CVE-2024-1234"

def test_format_response_deterministic_output():
    llm_response = "Deterministic output test."
    retrieved_documents = [
        {"id": "CVE-2021-0001"},
        {"id": "CVE-2022-0002"}
    ]

    result1 = format_response(llm_response, retrieved_documents)
    result2 = format_response(llm_response, retrieved_documents)

    assert result1 == result2
    assert result1["formatted_text"] == "Answer\n\nDeterministic output test.\n\nSources\n\n- CVE-2021-0001\n- CVE-2022-0002"
