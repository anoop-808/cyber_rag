"""Unit tests for the unified retrieval pipeline."""

import pytest
from unittest.mock import patch, MagicMock

from app.retrieval.pipeline import retrieve, DEFAULT_TOP_K, RETRIEVAL_LIMIT


@patch("app.retrieval.pipeline.search_hybrid")
@patch("app.retrieval.pipeline.rerank_results")
@patch("app.retrieval.pipeline.apply_filters")
def test_retrieve_end_to_end(mock_apply_filters, mock_rerank_results, mock_search_hybrid):
    """Test full pipeline execution without filters."""
    # Setup mock returns
    mock_search_hybrid.return_value = [{"id": "CVE-1"}]
    mock_rerank_results.return_value = [{"id": "CVE-1"}]

    # Execute
    results = retrieve(query="test query")

    # Assert
    assert len(results) == 1
    assert results[0]["id"] == "CVE-1"

    mock_search_hybrid.assert_called_once()
    mock_rerank_results.assert_called_once()
    mock_apply_filters.assert_not_called()


def test_retrieve_empty_query():
    """Test empty query handling."""
    results = retrieve(query="")
    assert results == []

    results = retrieve(query="   ")
    assert results == []


@patch("app.retrieval.pipeline.search_hybrid")
@patch("app.retrieval.pipeline.rerank_results")
def test_retrieve_empty_results(mock_rerank_results, mock_search_hybrid):
    """Test pipeline behavior when hybrid retrieval returns empty results."""
    mock_search_hybrid.return_value = []

    results = retrieve(query="test")
    assert results == []

    mock_search_hybrid.assert_called_once()
    mock_rerank_results.assert_not_called()


@patch("app.retrieval.pipeline.search_hybrid")
def test_retrieve_hybrid_failure(mock_search_hybrid):
    """Test pipeline failure when hybrid retrieval throws exception."""
    mock_search_hybrid.side_effect = ValueError("Index not found")

    with pytest.raises(RuntimeError) as exc_info:
        retrieve(query="test")

    assert "Hybrid retrieval failed" in str(exc_info.value)


@patch("app.retrieval.pipeline.search_hybrid")
@patch("app.retrieval.pipeline.rerank_results")
@patch("app.retrieval.pipeline.apply_filters")
def test_metadata_filtering(mock_apply_filters, mock_rerank_results, mock_search_hybrid):
    """Test pipeline correctly applies filters."""
    mock_search_hybrid.return_value = [{"id": "CVE-1"}, {"id": "CVE-2"}]
    mock_rerank_results.return_value = [{"id": "CVE-1"}, {"id": "CVE-2"}]
    mock_apply_filters.return_value = [{"id": "CVE-1"}]

    filters = {"vendor": "microsoft"}
    results = retrieve(query="test", filters=filters)

    assert len(results) == 1
    assert results[0]["id"] == "CVE-1"
    mock_apply_filters.assert_called_once_with([{"id": "CVE-1"}, {"id": "CVE-2"}], filters=filters)


@patch("app.retrieval.pipeline.search_hybrid")
@patch("app.retrieval.pipeline.rerank_results")
def test_top_k_behavior(mock_rerank_results, mock_search_hybrid):
    """Test pipeline truncates final results to top_k."""
    # Create 20 mock results
    mock_results = [{"id": f"CVE-{i}"} for i in range(20)]

    mock_search_hybrid.return_value = mock_results
    mock_rerank_results.return_value = mock_results

    # Request top_k = 5
    results = retrieve(query="test", top_k=5)

    assert len(results) == 5
    assert results[-1]["id"] == "CVE-4"
