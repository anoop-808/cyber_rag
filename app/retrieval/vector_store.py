"""Vector store initialization and management."""

import chromadb
from chromadb.api.models.Collection import Collection
from pathlib import Path

from app.core.config import config

COLLECTION_NAME = "cyberrag_cves"
_vector_collection: Collection | None = None

def get_vector_store() -> Collection:
    """Initialize and return the ChromaDB collection for embeddings.

    Returns
    -------
    chromadb.api.models.Collection.Collection
        The ChromaDB collection for CVE embeddings.
    """
    global _vector_collection

    if _vector_collection is None:
        db_path = Path(config.VECTOR_DB_PATH)
        db_path.mkdir(parents=True, exist_ok=True)

        client = chromadb.PersistentClient(path=str(db_path))
        _vector_collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    return _vector_collection
