"""Embedding model loader for CyberRAG retrieval."""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    """Return the shared SentenceTransformer embedding model.

    The model is loaded once when this module is imported and reused
    across CyberRAG retrieval components.

    Returns
    -------
    SentenceTransformer
        The preloaded sentence embedding model configured with
        ``MODEL_NAME``.
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(MODEL_NAME)
    return _embedding_model
