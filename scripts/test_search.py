"""Validate CyberRAG semantic CVE search with sample security queries."""

from typing import Any

from app.retrieval.search import search_cves

TEST_QUERIES: list[str] = [
    "Remote Code Execution",
    "SQL Injection",
    "Authentication Bypass",
    "Cross Site Scripting",
    "Linux Privilege Escalation",
]

SEPARATOR = "-" * 60


def format_cvss_score(metadata: dict[str, Any]) -> str:
    """Format the CVSS score for display when available.

    Parameters
    ----------
    metadata : dict
        Result metadata returned by ``search_cves()``.

    Returns
    -------
    str
        CVSS score text or a placeholder when unavailable.
    """
    cvss_score = metadata.get("cvss_score")
    if cvss_score is None:
        return "Not available"
    return str(cvss_score)


def display_results(query: str, results: list[dict[str, Any]]) -> None:
    """Print search results for a query in a readable format.

    Parameters
    ----------
    query : str
        The search query that was executed.
    results : list of dict
        Ranked CVE matches returned by ``search_cves()``.
    """
    print(SEPARATOR)
    print(f"Query: {query}")
    print()

    if not results:
        print("No matching CVEs found.")
        return

    for rank, result in enumerate(results, start=1):
        metadata = result.get("metadata", {})
        print(f"Rank: {rank}")
        print(f"CVE ID: {result.get('id')}")
        print(f"Distance: {result.get('distance')}")
        print(f"CVSS Score: {format_cvss_score(metadata)}")
        print(f"Description: {result.get('description')}")
        print()


def run_query_test(query: str, top_k: int = 5) -> None:
    """Run semantic search for a single query and display the results.

    Parameters
    ----------
    query : str
        Natural-language search query.
    top_k : int, optional
        Maximum number of results to retrieve. Default is 5.
    """
    try:
        results = search_cves(query, top_k=top_k)
        display_results(query, results)
    except Exception as exc:
        print(SEPARATOR)
        print(f"Query: {query}")
        print(f"Error: {exc}")
        print()


def main() -> None:
    """Run semantic search tests for predefined cybersecurity queries."""
    for query in TEST_QUERIES:
        run_query_test(query)


if __name__ == "__main__":
    main()
