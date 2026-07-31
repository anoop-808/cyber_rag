"""ChromaDB vector store initialization for CyberRAG retrieval."""

from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

from app.core.config import config

VECTOR_DB_PATH = config.VECTOR_DB_PATH
COLLECTION_NAME = "cyberrag_cves"

_vector_collection: Collection | None = None


def get_vector_store() -> Collection:
    """Return the persistent ChromaDB collection for CyberRAG CVEs.

    On first access, this function creates the vector store directory if
    needed, initializes a persistent ChromaDB client, and creates the
    collection when it does not already exist. Later calls reuse the same
    collection instance.

    Returns
    -------
    Collection
        The ChromaDB collection configured for CyberRAG CVE storage.
    """
    global _vector_collection

    if _vector_collection is None:
        vector_db_path = Path(VECTOR_DB_PATH)
        vector_db_path.mkdir(parents=True, exist_ok=True)

        client = chromadb.PersistentClient(path=str(vector_db_path))
        _vector_collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=None,
        )

    return _vector_collection
