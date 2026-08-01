"""Unit tests for the Context Builder."""

import logging
from app.rag.context_builder import build_context


def test_build_context_empty():
    """Test building context with empty results."""
    assert build_context([]) == ""


def test_build_context_single_document():
    """Test building context with a single complete document."""
    docs = [
        {
            "id": "CVE-2024-1234",
            "description": "Test description.",
            "severity": "CRITICAL",
            "cwe_id": "CWE-79",
            "metadata": {
                "cvss_score": 9.8,
                "publication_year": 2024
            }
        }
    ]

    context = build_context(docs)

    assert "[CVE-2024-1234]" in context
    assert "Description:\nTest description." in context
    assert "Severity:\nCRITICAL" in context
    assert "CVSS:\n9.8" in context
    assert "Published:\n2024" in context
    assert "CWE:\nCWE-79" in context
    assert "------------------" not in context


def test_build_context_multiple_documents():
    """Test building context with multiple documents and ordering."""
    docs = [
        {
            "id": "CVE-2024-1111",
            "description": "Desc 1",
            "severity": "HIGH",
        },
        {
            "id": "CVE-2024-2222",
            "description": "Desc 2",
            "metadata": {
                "severity": "LOW"
            }
        }
    ]

    context = build_context(docs)

    assert "[CVE-2024-1111]" in context
    assert "[CVE-2024-2222]" in context
    assert "Severity:\nHIGH" in context
    assert "Severity:\nLOW" in context

    # Check ordering
    idx1 = context.find("[CVE-2024-1111]")
    idx2 = context.find("[CVE-2024-2222]")
    assert idx1 < idx2
    assert "------------------" in context


def test_build_context_missing_metadata():
    """Test building context with missing metadata gracefully."""
    docs = [
        {
            "id": "CVE-2024-0000",
            # Missing description, should default
        }
    ]

    context = build_context(docs)

    assert "[CVE-2024-0000]" in context
    assert "Description:\nNo description available." in context
    assert "Severity:" not in context
    assert "CVSS:" not in context
    assert "Published:" not in context
    assert "CWE:" not in context


def test_build_context_max_documents():
    """Test context size limit for maximum documents."""
    docs = [
        {"id": f"CVE-2024-000{i}", "description": "Desc"}
        for i in range(5)
    ]

    context = build_context(docs, max_documents=2)

    assert "[CVE-2024-0000]" in context
    assert "[CVE-2024-0001]" in context
    assert "[CVE-2024-0002]" not in context

    # Should only have one separator between the two docs
    assert context.count("------------------") == 1


def test_build_context_max_characters():
    """Test context size limit for maximum characters."""
    docs = [
        {"id": "CVE-2024-1000", "description": "A very long description that takes up space."},
        {"id": "CVE-2024-2000", "description": "Another description."},
    ]

    # Set max_characters to be enough for the first doc, but not the second
    context = build_context(docs, max_characters=100)

    assert "[CVE-2024-1000]" in context
    assert "[CVE-2024-2000]" not in context


def test_build_context_logging(caplog):
    """Test context builder logging."""
    with caplog.at_level(logging.INFO):
        docs = [{"id": "CVE-1", "description": "Desc"}]
        build_context(docs)

        assert "Context Builder: Retrieved=1" in caplog.text
        assert "Included=1" in caplog.text

    with caplog.at_level(logging.INFO):
        build_context([])
        assert "0 retrieved documents" in caplog.text
