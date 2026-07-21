"""Semantic search utilities for CyberRAG CVE retrieval."""

from typing import Any

from app.retrieval.embeddings import get_embedding_model
from app.retrieval.vector_store import get_vector_store


def search_cves(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search indexed CVEs using semantic vector similarity.

    Parameters
    ----------
    query : str
        Natural-language search query.
    top_k : int, optional
        Maximum number of similar CVEs to return. Default is 5.

    Returns
    -------
    list of dict
        Ranked CVE matches. Each dictionary contains ``id``,
        ``description``, ``metadata``, and ``distance``.

    Raises
    ------
    ValueError
        If ``query`` is empty or contains only whitespace.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty or contain only whitespace.")

    model = get_embedding_model()
    collection = get_vector_store()

    query_embedding = model.encode(query.strip()).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    result_ids = results.get("ids", [[]])[0]
    if not result_ids:
        return []

    result_documents = results.get("documents", [[]])[0]
    result_metadatas = results.get("metadatas", [[]])[0]
    result_distances = results.get("distances", [[]])[0]

    formatted_results: list[dict[str, Any]] = []
    for index, cve_id in enumerate(result_ids):
        formatted_results.append(
            {
                "id": cve_id,
                "description": result_documents[index],
                "metadata": result_metadatas[index] or {},
                "distance": result_distances[index],
            }
        )

    return formatted_results
