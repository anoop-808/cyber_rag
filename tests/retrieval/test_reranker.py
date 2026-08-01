import pytest
import logging
from app.retrieval.reranker import rerank_results

def test_rerank_empty_input():
    results = []
    refined = rerank_results(results)
    assert refined == []

def test_rerank_single_result():
    results = [{"id": "CVE-2024-0001", "score": 0.85}]
    refined = rerank_results(results)
    assert len(refined) == 1
    assert refined[0]["id"] == "CVE-2024-0001"

def test_rerank_multiple_results_ordering():
    results = [
        {"id": "CVE-2024-0001", "score": 0.5},
        {"id": "CVE-2024-0002", "score": 0.9},
        {"id": "CVE-2024-0003", "score": 0.7}
    ]
    refined = rerank_results(results)
    assert len(refined) == 3
    assert refined[0]["id"] == "CVE-2024-0002"
    assert refined[1]["id"] == "CVE-2024-0003"
    assert refined[2]["id"] == "CVE-2024-0001"

def test_rerank_stable_ordering_tie_breaking():
    # Both have the same score, should fallback to ID (descending)
    results = [
        {"id": "CVE-2024-0001", "score": 0.8},
        {"id": "CVE-2024-0002", "score": 0.8}
    ]
    refined = rerank_results(results)
    assert len(refined) == 2
    assert refined[0]["id"] == "CVE-2024-0002"
    assert refined[1]["id"] == "CVE-2024-0001"

def test_rerank_duplicate_protection():
    # Duplicate IDs, should keep the one with the highest score
    results = [
        {"id": "CVE-2024-0001", "score": 0.5},
        {"id": "CVE-2024-0002", "score": 0.9},
        {"id": "CVE-2024-0001", "score": 0.8}
    ]
    refined = rerank_results(results)
    assert len(refined) == 2
    assert refined[0]["id"] == "CVE-2024-0002"
    assert refined[1]["id"] == "CVE-2024-0001"
    assert refined[1]["score"] == 0.8

def test_rerank_missing_scores():
    # If missing, it should default to 0.0
    results = [
        {"id": "CVE-2024-0001"},
        {"id": "CVE-2024-0002", "score": 0.5},
        {"id": "CVE-2024-0003"}
    ]
    refined = rerank_results(results)
    assert len(refined) == 3
    # 0.5 should be first
    assert refined[0]["id"] == "CVE-2024-0002"
    # Tie between 0003 and 0001 (score 0.0), tie-broken by ID descending
    assert refined[1]["id"] == "CVE-2024-0003"
    assert refined[2]["id"] == "CVE-2024-0001"

def test_rerank_distance_score_handling():
    # Test distance (lower is better) is inverted to score
    results = [
        {"id": "CVE-2024-0001", "distance": 0.2}, # -0.2
        {"id": "CVE-2024-0002", "distance": 0.5}, # -0.5
        {"id": "CVE-2024-0003", "distance": 0.1}  # -0.1
    ]
    refined = rerank_results(results)
    assert len(refined) == 3
    # -0.1 > -0.2 > -0.5
    assert refined[0]["id"] == "CVE-2024-0003"
    assert refined[1]["id"] == "CVE-2024-0001"
    assert refined[2]["id"] == "CVE-2024-0002"

def test_rerank_invalid_results(caplog):
    # Invalid entries should be skipped
    results = [
        {"id": "CVE-2024-0001", "score": 0.8},
        "not-a-dict",
        {"score": 0.9} # missing id
    ]
    with caplog.at_level(logging.WARNING):
        refined = rerank_results(results)

    assert len(refined) == 1
    assert refined[0]["id"] == "CVE-2024-0001"
    assert "Invalid result format found" in caplog.text
    assert "Result missing 'id' found" in caplog.text

def test_rerank_top_k():
    results = [
        {"id": f"CVE-2024-{i:04d}", "score": i} for i in range(1, 15)
    ]
    refined = rerank_results(results, top_k=5)
    assert len(refined) == 5
    assert refined[0]["id"] == "CVE-2024-0014"
    assert refined[4]["id"] == "CVE-2024-0010"
