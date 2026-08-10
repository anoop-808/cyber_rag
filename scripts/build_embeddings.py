"""Build the ChromaDB CVE embedding index from populated SQLite data."""

import logging
from typing import Any

from app.core.db import get_db_connection
from app.retrieval.embeddings import get_embedding_model
from app.retrieval.vector_store import get_vector_store

BATCH_SIZE = 100

logger = logging.getLogger(__name__)


def iter_cves() -> list[dict[str, Any]]:
    """Return CVEs ready for vector indexing from SQLite.

    Returns
    -------
    list of dict
        CVE rows containing an ID, description, and metadata fields.
    """
    with get_db_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, description, published, modified, severity, cvss_score, cwe_id
            FROM cves
            WHERE description IS NOT NULL 
              AND TRIM(description) != ''
              AND severity IN ('CRITICAL', 'HIGH')
              AND published >= '2026-01-01'
            ORDER BY id
            """
        ).fetchall()

    return [dict(row) for row in rows]


def metadata_for(row: dict[str, Any]) -> dict[str, Any]:
    """Build Chroma-compatible metadata for one CVE row.

    Parameters
    ----------
    row : dict
        SQLite CVE row.

    Returns
    -------
    dict
        Metadata with null values removed.
    """
    metadata = {
        "published": row.get("published"),
        "last_modified": row.get("modified"),
        "severity": row.get("severity"),
        "cvss_score": row.get("cvss_score"),
        "cwe_id": row.get("cwe_id"),
    }
    return {key: value for key, value in metadata.items() if value is not None}


def build_embeddings(batch_size: int = BATCH_SIZE) -> int:
    """Generate and upsert CVE embeddings into ChromaDB.

    Parameters
    ----------
    batch_size : int
        Number of CVEs to encode per batch.

    Returns
    -------
    int
        Number of CVEs upserted.
    """
    rows = iter_cves()
    if not rows:
        raise RuntimeError("No CVEs found in SQLite. Run scripts.import_nvd first.")

    model = get_embedding_model()
    collection = get_vector_store()
    indexed_count = 0

    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        descriptions = [row["description"] for row in batch]
        embeddings = model.encode(descriptions).tolist()

        collection.upsert(
            ids=[row["id"] for row in batch],
            documents=descriptions,
            embeddings=embeddings,
            metadatas=[metadata_for(row) for row in batch],
        )
        indexed_count += len(batch)

    return indexed_count


def main() -> None:
    """Build CVE embeddings as a standalone deployment build step."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    indexed_count = build_embeddings()
    logger.info("Upserted %s CVE vectors into ChromaDB.", indexed_count)


if __name__ == "__main__":
    main()
