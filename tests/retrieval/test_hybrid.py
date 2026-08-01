"""Unit tests for the Hybrid Retrieval Engine."""

from unittest import mock

import pytest

from app.retrieval.hybrid import normalize_scores, search_hybrid


def test_normalize_scores_not_inverted():
    """Test score normalization where higher is better."""
    results = [
        {"id": "1", "score": 10},
        {"id": "2", "score": 20},
        {"id": "3", "score": 5},
    ]
    normalize_scores(results, "score", invert=False)

    # Min = 5, Max = 20, Range = 15
    assert results[0]["normalized_score"] == pytest.approx((10 - 5) / 15)
    assert results[1]["normalized_score"] == pytest.approx(1.0)
    assert results[2]["normalized_score"] == pytest.approx(0.0)


def test_normalize_scores_inverted():
    """Test score normalization where lower is better (e.g. distances)."""
    results = [
        {"id": "1", "dist": 0.1},
        {"id": "2", "dist": 0.5},
        {"id": "3", "dist": 0.2},
    ]
    normalize_scores(results, "dist", invert=True)

    # Min = 0.1, Max = 0.5, Range = 0.4
    # Inverted: 1.0 - (val - min)/range
    assert results[0]["normalized_score"] == pytest.approx(1.0) # (0.1 - 0.1)/0.4 = 0.0 -> 1.0 - 0.0 = 1.0
    assert results[1]["normalized_score"] == pytest.approx(0.0) # (0.5 - 0.1)/0.4 = 1.0 -> 1.0 - 1.0 = 0.0
    assert results[2]["normalized_score"] == pytest.approx(0.75) # (0.2 - 0.1)/0.4 = 0.25 -> 1.0 - 0.25 = 0.75


def test_normalize_scores_zero_range():
    """Test normalization when all scores are equal."""
    results = [{"id": "1", "score": 10}, {"id": "2", "score": 10}]
    normalize_scores(results, "score", invert=False)
    assert results[0]["normalized_score"] == 1.0
    assert results[1]["normalized_score"] == 1.0


@mock.patch("app.retrieval.hybrid.search_cves")
@mock.patch("app.retrieval.hybrid.search_cves_fts")
def test_search_hybrid_empty_query(mock_search_fts, mock_search_vector):
    """Test hybrid search with empty query returns empty list."""
    results = search_hybrid("")
    assert results == []
    mock_search_fts.assert_not_called()
    mock_search_vector.assert_not_called()


@mock.patch("app.retrieval.hybrid.search_cves")
@mock.patch("app.retrieval.hybrid.search_cves_fts")
def test_search_hybrid_bm25_only(mock_search_fts, mock_search_vector):
    """Test hybrid search when vector search returns empty or fails."""
    mock_search_fts.return_value = [
        {"id": "CVE-2024-0001", "description": "Desc 1", "score": -5.0},
        {"id": "CVE-2024-0002", "description": "Desc 2", "score": -1.0},
    ]
    mock_search_vector.return_value = []

    results = search_hybrid("test query", bm25_weight=1.0, vector_weight=1.0)

    assert len(results) == 2
    # CVE-2024-0001 has better (lower) score, so should be ranked first
    assert results[0]["id"] == "CVE-2024-0001"
    assert results[1]["id"] == "CVE-2024-0002"
    assert "_bm25_score" not in results[0]
    assert "_vector_score" not in results[0]


@mock.patch("app.retrieval.hybrid.search_cves")
@mock.patch("app.retrieval.hybrid.search_cves_fts")
def test_search_hybrid_vector_only(mock_search_fts, mock_search_vector):
    """Test hybrid search when BM25 search returns empty or fails."""
    mock_search_fts.return_value = []
    mock_search_vector.return_value = [
        {"id": "CVE-2024-0001", "description": "Desc 1", "distance": 0.1, "metadata": {"severity": "HIGH"}},
        {"id": "CVE-2024-0002", "description": "Desc 2", "distance": 0.9, "metadata": {"severity": "LOW"}},
    ]

    results = search_hybrid("test query")

    assert len(results) == 2
    # CVE-2024-0001 has better (lower) distance, so should be ranked first
    assert results[0]["id"] == "CVE-2024-0001"
    assert results[0]["severity"] == "HIGH"
    assert results[1]["id"] == "CVE-2024-0002"


@mock.patch("app.retrieval.hybrid.search_cves")
@mock.patch("app.retrieval.hybrid.search_cves_fts")
def test_search_hybrid_combined_and_dedup(mock_search_fts, mock_search_vector):
    """Test combining results and removing duplicates."""
    mock_search_fts.return_value = [
        {"id": "CVE-2024-0001", "description": "Desc 1", "score": -5.0}, # Best bm25 -> norm: 1.0
        {"id": "CVE-2024-0002", "description": "Desc 2", "score": -1.0}, # Worst bm25 -> norm: 0.0
    ]
    mock_search_vector.return_value = [
        {"id": "CVE-2024-0002", "description": "Desc 2", "distance": 0.1}, # Best vector -> norm: 1.0
        {"id": "CVE-2024-0003", "description": "Desc 3", "distance": 0.9}, # Worst vector -> norm: 0.0
    ]

    results = search_hybrid("test", bm25_weight=0.5, vector_weight=0.5)

    # Should be 3 unique results
    assert len(results) == 3

    # Check scores:
    # CVE-2024-0001: bm25(1.0)*0.5 + vector(0)*0.5 = 0.5
    # CVE-2024-0002: bm25(0.0)*0.5 + vector(1.0)*0.5 = 0.5 (they tie, sort order might be arbitrary but they have valid scores)
    # CVE-2024-0003: bm25(0)*0.5 + vector(0.0)*0.5 = 0.0

    ids = [r["id"] for r in results]
    assert "CVE-2024-0001" in ids
    assert "CVE-2024-0002" in ids
    assert "CVE-2024-0003" in ids
    assert results[-1]["id"] == "CVE-2024-0003" # Worst score


@mock.patch("app.retrieval.hybrid.search_cves")
@mock.patch("app.retrieval.hybrid.search_cves_fts")
def test_search_hybrid_top_k(mock_search_fts, mock_search_vector):
    """Test that the result is limited to top_k."""
    mock_search_fts.return_value = [
        {"id": f"CVE-BM25-{i}", "description": "Desc", "score": -i} for i in range(10)
    ]
    mock_search_vector.return_value = [
        {"id": f"CVE-VEC-{i}", "description": "Desc", "distance": i} for i in range(10)
    ]

    results = search_hybrid("test", top_k=5)

    # We generated 20 distinct IDs, but asked for top_k=5
    assert len(results) == 5
