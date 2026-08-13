"""FastAPI application entry point for CyberRAG."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.db import initialize_database

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    logger.info("Initializing vector store... (Skipped for lazy loading)")
    # get_vector_store() is lazy loaded when actually needed

    logger.info("Initializing database...")
    # Initialize database on startup
    initialize_database()

    yield

    logger.info("Application shutting down...")

app = FastAPI(
    lifespan=lifespan,
    title="CyberRAG API",
    description="AI-powered Retrieval-Augmented Generation API for Cybersecurity Knowledge Retrieval",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        "https://cyber-rag-frontend-awxn.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.get("/health")
def health() -> dict[str, str]:
    """Return application health status.

    Returns
    -------
    dict
        Response containing the current health status.
    """
    return {"status": "healthy"}
