"""Embedding generation pipeline for CyberRAG."""

import logging
from typing import Any

from app.core.db import get_db_connection
from app.retrieval.embeddings import get_embedding_model
from app.retrieval.vector_store import get_vector_store

logger = logging.getLogger(__name__)


def generate_and_store_embeddings(batch_size: int = 100) -> None:
    """Generate and store embeddings for all CVEs in the database.

    Reads CVEs from the SQLite database, generates embeddings for their
    descriptions using the configured sentence transformer model, and
    stores the resulting vectors and metadata in ChromaDB.

    Parameters
    ----------
    batch_size : int, optional
        The number of CVEs to process in a single batch, by default 100.
    """
    model = get_embedding_model()
    collection = get_vector_store()

    logger.info("Starting embedding generation pipeline.")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cves")
        total_cves = cursor.fetchone()[0]
        logger.info(f"Found {total_cves} CVEs to process.")

        cursor.execute("SELECT id, description, severity, published FROM cves")

        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break

            ids = []
            documents = []
            metadatas = []

            for row in rows:
                cve_id = row["id"]
                description = row["description"] or ""

                # Combine id and description for a richer embedding text
                # We mainly rely on description based on requirements
                text_to_embed = f"{cve_id}: {description}"

                ids.append(cve_id)
                documents.append(text_to_embed)
                metadatas.append(
                    {
                        "severity": row["severity"] or "UNKNOWN",
                        "published": row["published"] or "",
                    }
                )

            # Generate embeddings
            embeddings = model.encode(documents).tolist()

            # Store in ChromaDB
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )

            logger.info(f"Processed and stored batch of {len(rows)} CVEs.")

    logger.info("Embedding generation pipeline completed successfully.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_and_store_embeddings()
