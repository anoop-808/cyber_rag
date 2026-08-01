"""Result re-ranking module for CyberRAG retrieval."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

def rerank_results(results: list[dict[str, Any]], top_k: int = 10) -> list[dict[str, Any]]:
    """Re-rank retrieval results to improve ordering and handle duplicates.

    Parameters
    ----------
    results : list of dict
        The list of results from the retrieval engine. Each dictionary should
        ideally contain 'id' and either 'score' or 'distance'.
    top_k : int, optional
        Maximum number of refined results to return. Default is 10.

    Returns
    -------
    list of dict
        A refined and ranked list of results, deduplicated and truncated to top_k.
    """
    logger.info("Executing re-ranking engine")

    if not results:
        logger.info("Input result count: 0, Output result count: 0")
        return []

    logger.info(f"Input result count: {len(results)}")

    # Deduplicate and normalize score
    unique_results: dict[str, dict[str, Any]] = {}

    for result in results:
        if not isinstance(result, dict):
            logger.warning("Invalid result format found and skipped.")
            continue

        cve_id = result.get("id")
        if not cve_id:
            logger.warning("Result missing 'id' found and skipped.")
            continue

        # Determine a sorting score
        # Assume 'score' (higher is better) or 'distance' (lower is better, so we negate)
        if "score" in result:
            current_score = result["score"]
        elif "distance" in result:
            current_score = -result["distance"]
        else:
            current_score = 0.0

        if cve_id in unique_results:
            existing = unique_results[cve_id]

            if "score" in existing:
                existing_score = existing["score"]
            elif "distance" in existing:
                existing_score = -existing["distance"]
            else:
                existing_score = 0.0

            if current_score > existing_score:
                unique_results[cve_id] = result
        else:
            unique_results[cve_id] = result

    # Sort results
    # Primary key: derived score (descending)
    # Secondary key: id string (descending) to deterministically resolve ties
    def sort_key(item: dict[str, Any]) -> tuple[float, str]:
        if "score" in item:
            score = item["score"]
        elif "distance" in item:
            score = -item["distance"]
        else:
            score = 0.0
        return (score, str(item.get("id", "")))

    refined_results = sorted(unique_results.values(), key=sort_key, reverse=True)

    # Truncate to top_k
    final_results = refined_results[:top_k]

    logger.info(f"Output result count: {len(final_results)}")

    return final_results
