"""FastAPI application entry point for CyberRAG."""

from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.api.routes import router
import os
from app.core.db import initialize_database
from app.ingestion.importer import import_cve_data
from app.ingestion.loader import load_json_dataset
from app.api.dependencies import get_vector_store

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    logger.info("Initializing vector store...")
    get_vector_store()

    logger.info("Initializing database...")
    # Initialize database on startup
    initialize_database()

    # Check if processed dataset exists and import it
    processed_path = "storage/datasets/processed/processed_cves.json"
    if os.path.exists(processed_path):
        logger.info(f"Importing dataset from {processed_path}")
        dataset = load_json_dataset(processed_path)
        import_cve_data(dataset)

    yield

    logger.info("Application shutting down...")

app = FastAPI(
    lifespan=lifespan,
    title="CyberRAG API",
    description="AI-powered Retrieval-Augmented Generation API for Cybersecurity Knowledge Retrieval",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    """Return a welcome message indicating the API is running.

    Returns
    -------
    dict
        Response containing a welcome message.
    """
    return {"message": "CyberRAG API is running"}
