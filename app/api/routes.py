"""FastAPI routes for CyberRAG RAG endpoint."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.rag import answer_question


class QuestionRequest(BaseModel):
    """Request model for the /ask endpoint."""

    query: str = Field(..., description="Natural-language question to answer.")
    top_k: int = Field(5, description="Maximum number of CVEs to retrieve.")


router = APIRouter()


@router.post("/ask")
def ask_question(request: QuestionRequest) -> dict[str, Any]:
    """Answer a cybersecurity question using the RAG pipeline.

    Parameters
    ----------
    request : QuestionRequest
        Request containing the query and optional top_k parameter.

    Returns
    -------
    dict
        Response containing the original query, generated answer, sources,
        and count of matches.

    Raises
    ------
    HTTPException
        If the query or top_k validation fails (status code 400).
    """
    try:
        return answer_question(request.query, request.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
