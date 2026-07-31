"""Embedding model loader for CyberRAG retrieval."""

from sentence_transformers import SentenceTransformer

from app.core.config import config

MODEL_NAME = config.EMBEDDING_MODEL

_embedding_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Return the shared SentenceTransformer embedding model.

    The model is loaded on first use and reused across CyberRAG
    retrieval components.

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
