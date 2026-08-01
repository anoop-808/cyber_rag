"""Hybrid retrieval engine for CyberRAG."""

import logging
from typing import Any

from app.retrieval.search import search_cves
from app.search.sqlite_search import search_cves_fts

logger = logging.getLogger(__name__)


def normalize_scores(
    results: list[dict[str, Any]], score_key: str, invert: bool = False
) -> None:
    """Normalize scores in results list using min-max scaling.

    The normalized score is added as `normalized_score` (between 0.0 and 1.0).
    Higher normalized_score always means a better match.

    Parameters
    ----------
    results : list of dict
        List of result dictionaries.
    score_key : str
        The key in the dictionary containing the raw score.
    invert : bool
        If True, lower raw scores are better (e.g., SQLite BM25, distances).
        If False, higher raw scores are better.
    """
    if not results:
        return

    scores = [res[score_key] for res in results]
    min_score = min(scores)
    max_score = max(scores)

    score_range = max_score - min_score

    for res in results:
        if score_range == 0:
            # If all scores are the same, they are all equally good
            res["normalized_score"] = 1.0
        else:
            normalized = (res[score_key] - min_score) / score_range
            if invert:
                # For SQLite bm25, lower is better. For Chroma distance, lower is better.
                res["normalized_score"] = 1.0 - normalized
            else:
                res["normalized_score"] = normalized


def search_hybrid(
    query: str,
    top_k: int = 10,
    bm25_weight: float = 0.5,
    vector_weight: float = 0.5,
) -> list[dict[str, Any]]:
    """Execute hybrid retrieval combining lexical and semantic search.

    Parameters
    ----------
    query : str
        Search query.
    top_k : int, optional
        Maximum number of matches to return. Default is 10.
    bm25_weight : float, optional
        Weight for the BM25 score. Default is 0.5.
    vector_weight : float, optional
        Weight for the vector score. Default is 0.5.

    Returns
    -------
    list of dict
        Unified ranked result list.
    """
    if not query or not query.strip():
        return []

    bm25_results = []
    vector_results = []

    # 1. Execute BM25 retrieval
    try:
        # Get more results to ensure good overlap
        bm25_results = search_cves_fts(query=query, top_k=max(top_k * 2, 20))
        # SQLite BM25 returns more negative numbers for better matches.
        # e.g., -5 is better than -1.
        # It means lower is better, so we invert.
        normalize_scores(bm25_results, score_key="score", invert=True)
    except Exception as e:
        logger.warning(f"BM25 retrieval failed: {e}")

    # 2. Execute Vector retrieval
    try:
        # Get more results to ensure good overlap
        vector_results = search_cves(query=query, top_k=max(top_k * 2, 20))
        # Chroma distance (L2 or cosine) means lower is better, so invert.
        normalize_scores(vector_results, score_key="distance", invert=True)
    except Exception as e:
        logger.warning(f"Vector retrieval failed: {e}")

    # 3. Merge and deduplicate
    merged_results = {}
    duplicates = 0

    # Add BM25 results
    for res in bm25_results:
        cve_id = res["id"]
        weighted_score = res["normalized_score"] * bm25_weight

        merged_results[cve_id] = {
            "id": cve_id,
            "description": res["description"],
            "severity": res.get("severity"),
            "cwe_id": res.get("cwe_id"),
            "metadata": {},  # SQLite might not have full metadata
            "hybrid_score": weighted_score,
            "_bm25_score": res["normalized_score"],
            "_vector_score": 0.0,
        }

    # Add/Update with Vector results
    for res in vector_results:
        cve_id = res["id"]
        weighted_score = res["normalized_score"] * vector_weight

        if cve_id in merged_results:
            duplicates += 1
            merged_results[cve_id]["hybrid_score"] += weighted_score
            merged_results[cve_id]["_vector_score"] = res["normalized_score"]
            # Prefer vector metadata if available and richer
            if "metadata" in res and res["metadata"]:
                merged_results[cve_id]["metadata"] = res["metadata"]
        else:
            merged_results[cve_id] = {
                "id": cve_id,
                "description": res["description"],
                "severity": res.get("metadata", {}).get("severity"),
                "cwe_id": res.get("metadata", {}).get("cwe_id"),
                "metadata": res.get("metadata", {}),
                "hybrid_score": weighted_score,
                "_bm25_score": 0.0,
                "_vector_score": res["normalized_score"],
            }

    final_results = list(merged_results.values())

    # 4. Sort by hybrid_score descending
    final_results.sort(key=lambda x: x["hybrid_score"], reverse=True)

    # 5. Limit to top_k
    final_results = final_results[:top_k]

    # Clean up internal scores and log stats
    for res in final_results:
        res.pop("_bm25_score", None)
        res.pop("_vector_score", None)

    logger.info(
        f"Hybrid retrieval stats - BM25: {len(bm25_results)}, "
        f"Vector: {len(vector_results)}, Duplicates merged: {duplicates}, "
        f"Final count: {len(final_results)}"
    )

    return final_results
