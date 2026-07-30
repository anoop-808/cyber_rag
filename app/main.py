"""FastAPI application entry point for CyberRAG."""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
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
