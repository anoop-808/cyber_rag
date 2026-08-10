import pytest
import asyncio
from unittest.mock import patch

from app.api.dependencies import (
    get_settings,
    get_vector_store,
    get_llm_client,
    get_retrieval_pipeline
)
from app.core.config import Config
from app.llm.client import generate_response
from app.retrieval.pipeline import retrieve

def test_get_settings():
    """Test get_settings returns the Config instance."""
    settings = get_settings()
    assert isinstance(settings, Config)

def test_get_vector_store():
    """Test get_vector_store returns a ChromaDB Collection."""
    # We mock get_vs to avoid actually initializing the database for tests
    # Wait, the dependency itself calls app.retrieval.vector_store.get_vector_store
    # Let's mock it inside the dependency module to see if it returns properly
    with patch("app.api.dependencies.get_vs") as mock_get_vs:
        mock_get_vs.return_value = "mock_collection"
        collection = get_vector_store()
        assert collection == "mock_collection"
        mock_get_vs.assert_called_once()

def test_get_llm_client():
    """Test get_llm_client returns the correct callable."""
    client = get_llm_client()
    assert client is generate_response

def test_get_retrieval_pipeline():
    """Test get_retrieval_pipeline returns the correct callable."""
    pipeline = get_retrieval_pipeline()
    assert pipeline is retrieve

def test_lifespan_lifecycle():
    """Test the application startup and shutdown lifecycle logging and initialization."""
    from app.main import app, lifespan

    with patch("app.main.initialize_database") as mock_init_db:
        async def run_lifespan():
            async with lifespan(app):
                mock_init_db.assert_called_once()

        asyncio.run(run_lifespan())
