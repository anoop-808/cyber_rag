from typing import Callable, Any

from app.core.config import config, Config
from app.retrieval.vector_store import get_vector_store as get_vs
from app.llm.client import generate_response
from app.retrieval.pipeline import retrieve


def get_settings() -> Config:
    """Provide the application configuration settings.

    Returns
    -------
    Config
        The application configuration instance.
    """
    return config


def get_vector_store() -> Any:
    """Provide the initialized ChromaDB vector store collection.

    Returns
    -------
    Collection
        The persistent ChromaDB collection.
    """
    return get_vs()


def get_llm_client() -> Callable:
    """Provide the LLM client interface for generating responses.

    Returns
    -------
    Callable
        The `generate_response` function.
    """
    return generate_response


def get_retrieval_pipeline() -> Callable:
    """Provide the unified retrieval pipeline.

    Returns
    -------
    Callable
        The `retrieve` function.
    """
    return retrieve
