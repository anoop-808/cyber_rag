"""Retrieval service interface for CyberRAG."""

from typing import Any

from app.retrieval.search import search_cves


def retrieve_context(query: str, top_k: int = 5) -> dict[str, Any]:
    """Retrieve ranked CVE context for a natural-language query.

    Parameters
    ----------
    query : str
        Natural-language search query.
    top_k : int, optional
        Maximum number of CVEs to retrieve. Default is 5.

    Returns
    -------
    dict
        Standardized retrieval response containing the original ``query``,
        a ``results`` list from semantic search, and a ``count`` of matches.

    Raises
    ------
    ValueError
        If ``query`` is empty or contains only whitespace.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty or contain only whitespace.")

    results = search_cves(query, top_k=top_k)

    return {
        "query": query,
        "results": results,
        "count": len(results),
    }
