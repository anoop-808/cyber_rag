"""SQLite FTS5 keyword search service."""

from typing import Any, Optional

from app.core.db import get_db_connection


def search_cves_fts(
    query: str,
    top_k: int = 5,
    severity: Optional[str] = None,
    vendor: Optional[str] = None,
    product: Optional[str] = None,
    cwe: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Search for CVEs using SQLite FTS5.

    Parameters
    ----------
    query : str
        Keyword search query.
    top_k : int, optional
        Maximum number of matches to return. Default is 5.
    severity : str, optional
        Filter by severity.
    vendor : str, optional
        Filter by vendor.
    product : str, optional
        Filter by product.
    cwe : str, optional
        Filter by CWE ID.

    Returns
    -------
    list of dict
        Ranked CVE matches from the FTS index.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty or contain only whitespace.")

    match_parts = [query]

    if severity:
        match_parts.append(f"severity:{severity}")
    if vendor:
        match_parts.append(f"vendor:{vendor}")
    if product:
        match_parts.append(f"product:{product}")
    if cwe:
        match_parts.append(f"cwe_id:{cwe}")

    # Combine all parts with AND
    match_query = " AND ".join(match_parts)

    sql = """
        SELECT
            cves.id,
            cves.description,
            cves.severity,
            cves.cwe_id,
            bm25(cves_fts) as rank
        FROM cves_fts
        JOIN cves ON cves.id = cves_fts.id
        WHERE cves_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """

    results = []
    with get_db_connection() as conn:
        cursor = conn.execute(sql, (match_query, top_k))
        for row in cursor:
            results.append(
                {
                    "id": row["id"],
                    "description": row["description"],
                    "severity": row["severity"],
                    "cwe_id": row["cwe_id"],
                    "score": row["rank"],
                }
            )

    return results
