"""Unit tests for metadata filtering engine."""

import pytest
from app.retrieval.filters import apply_filters


@pytest.fixture
def sample_results():
    """Return a sample list of results for testing."""
    return [
        {
            "id": "CVE-2024-0001",
            "description": "First CVE",
            "metadata": {
                "severity": "CRITICAL",
                "cvss_score": 9.8,
                "vendor": "microsoft",
                "product": "windows",
                "cwe": "CWE-79",
                "publication_year": 2024,
            },
            "distance": 0.1,
        },
        {
            "id": "CVE-2024-0002",
            "description": "Second CVE",
            "metadata": {
                "severity": "HIGH",
                "cvss_score": 8.5,
                "vendor": "apache",
                "product": "http_server",
                "cwe": "CWE-20",
                "publication_year": 2024,
            },
            "distance": 0.2,
        },
        {
            "id": "CVE-2023-0003",
            "description": "Third CVE",
            "metadata": {
                "severity": "MEDIUM",
                "cvss_score": 5.3,
                "vendor": "microsoft",
                "product": "office",
                "cwe": "CWE-79",
                "publication_year": 2023,
            },
            "distance": 0.3,
        },
    ]


def test_empty_results():
    """Test filtering an empty results list."""
    assert apply_filters([], {"severity": "CRITICAL"}) == []


def test_empty_filters(sample_results):
    """Test with empty filters dictionary."""
    assert apply_filters(sample_results, {}) == sample_results


def test_single_filter(sample_results):
    """Test applying a single filter."""
    filtered = apply_filters(sample_results, {"severity": "CRITICAL"})
    assert len(filtered) == 1
    assert filtered[0]["id"] == "CVE-2024-0001"


def test_multiple_filters(sample_results):
    """Test applying multiple filters simultaneously."""
    filtered = apply_filters(
        sample_results, {"vendor": "microsoft", "publication_year": 2024}
    )
    assert len(filtered) == 1
    assert filtered[0]["id"] == "CVE-2024-0001"

    filtered2 = apply_filters(
        sample_results, {"vendor": "microsoft", "cwe": "cwe-79"}
    )
    assert len(filtered2) == 2


def test_no_matching_documents(sample_results):
    """Test filters that match no documents."""
    filtered = apply_filters(sample_results, {"severity": "LOW"})
    assert len(filtered) == 0

    filtered = apply_filters(
        sample_results, {"vendor": "microsoft", "publication_year": 2020}
    )
    assert len(filtered) == 0


def test_case_insensitive_matching(sample_results):
    """Test that string matching is case-insensitive."""
    filtered = apply_filters(sample_results, {"vendor": "Microsoft"})
    assert len(filtered) == 2

    filtered = apply_filters(sample_results, {"cwe": "cwe-79"})
    assert len(filtered) == 2


def test_number_matching(sample_results):
    """Test filtering by numbers (cvss_score, publication_year)."""
    filtered = apply_filters(sample_results, {"cvss_score": "9.8"})
    assert len(filtered) == 1
    assert filtered[0]["id"] == "CVE-2024-0001"

    filtered = apply_filters(sample_results, {"publication_year": "2023"})
    assert len(filtered) == 1
    assert filtered[0]["id"] == "CVE-2023-0003"


def test_invalid_filter_key(sample_results):
    """Test that unsupported filters raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported filter key"):
        apply_filters(sample_results, {"unsupported": "value"})


def test_missing_metadata(sample_results):
    """Test handling of results missing the requested metadata."""
    results_missing_meta = [
        {"id": "CVE-X", "description": "No metadata", "metadata": {}}
    ]
    filtered = apply_filters(results_missing_meta, {"severity": "HIGH"})
    assert len(filtered) == 0


def test_none_filter_value(sample_results):
    """Test that a filter with a None value is ignored."""
    filtered = apply_filters(
        sample_results, {"vendor": "microsoft", "severity": None}
    )
    assert len(filtered) == 2
