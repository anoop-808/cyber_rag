"""Unified retrieval pipeline for CyberRAG."""

import logging
from typing import Any

from app.retrieval.hybrid import search_hybrid
from app.retrieval.reranker import rerank_results
from app.retrieval.filters import apply_filters

logger = logging.getLogger(__name__)

# Centralized retrieval configuration
DEFAULT_TOP_K = 10
DEFAULT_BM25_WEIGHT = 0.5
DEFAULT_VECTOR_WEIGHT = 0.5
RETRIEVAL_LIMIT = 50  # Fetch more candidates initially to allow for filtering


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute the complete unified retrieval workflow.

    Workflow:
    1. User Query
    2. Hybrid Retrieval
    3. Result Re-ranking
    4. Metadata Filtering
    5. Top-K Results

    Parameters
    ----------
    query : str
        The user's natural language search query.
    top_k : int, optional
        The maximum number of final results to return. Default is 10.
    filters : dict, optional
        Metadata filters to apply to the retrieved results.

    Returns
    -------
    list of dict
        A filtered, ranked, and truncated list of retrieval results.

    Raises
    ------
    RuntimeError
        If an unexpected failure occurs in the retrieval components.
    """
    logger.info(f"Pipeline started: received query (length {len(query)})")

    if not query or not query.strip():
        logger.info("Empty query received, returning empty results.")
        return []

    # 1. Hybrid Retrieval
    try:
        logger.info("Executing hybrid retrieval...")
        hybrid_results = search_hybrid(
            query=query,
            top_k=RETRIEVAL_LIMIT,
            bm25_weight=DEFAULT_BM25_WEIGHT,
            vector_weight=DEFAULT_VECTOR_WEIGHT,
        )
    except Exception as e:
        logger.error(f"Hybrid retrieval failed: {e}")
        raise RuntimeError(f"Hybrid retrieval failed: {e}") from e

    if not hybrid_results:
        logger.info("Hybrid retrieval returned 0 results. Pipeline complete.")
        return []

    # 2. Result Re-ranking
    try:
        logger.info("Executing result re-ranking...")
        ranked_results = rerank_results(hybrid_results, top_k=RETRIEVAL_LIMIT)
    except Exception as e:
        logger.error(f"Result re-ranking failed: {e}")
        raise RuntimeError(f"Result re-ranking failed: {e}") from e

    if not ranked_results:
        logger.info("Re-ranking returned 0 results. Pipeline complete.")
        return []

    # 3. Metadata Filtering
    if filters:
        try:
            logger.info("Executing metadata filtering...")
            filtered_results = apply_filters(ranked_results, filters=filters)
        except Exception as e:
            logger.error(f"Metadata filtering failed: {e}")
            raise RuntimeError(f"Metadata filtering failed: {e}") from e
    else:
        logger.info("No metadata filters provided. Skipping filtering step.")
        filtered_results = ranked_results

    # 4. Top-K Results
    final_results = filtered_results[:top_k]

    logger.info(f"Pipeline complete: Returning {len(final_results)} final results.")
    return final_results
