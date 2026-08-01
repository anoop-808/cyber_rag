"""Embedding model initialization and management."""

from sentence_transformers import SentenceTransformer

from app.core.config import config

MODEL_NAME = config.EMBEDDING_MODEL

_embedding_model: SentenceTransformer | None = None

def get_embedding_model() -> SentenceTransformer:
    """Initialize and return the sentence transformer model lazily.

    Returns
    -------
    SentenceTransformer
        The loaded sentence transformer model.
    """
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(MODEL_NAME)

    return _embedding_model
