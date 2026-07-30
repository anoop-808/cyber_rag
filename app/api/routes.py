"""FastAPI routes for CyberRAG RAG endpoint."""

from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.rag import answer_question
from app.search.sqlite_search import search_cves_fts
from app.retrieval.cve_detail import get_cve_detail


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

@router.get("/cve/{cve_id}")
def get_cve_endpoint(cve_id: str) -> dict[str, Any]:
    """Retrieve detailed information for a specific CVE.

    Parameters
    ----------
    cve_id : str
        The ID of the CVE to retrieve (e.g., CVE-2024-3094).

    Returns
    -------
    dict
        Response containing the CVE details.

    Raises
    ------
    HTTPException
        If the CVE is not found (status code 404).
    """
    cve_detail = get_cve_detail(cve_id)
    if cve_detail is None:
        raise HTTPException(status_code=404, detail="CVE not found")
    return cve_detail

@router.get("/search")
def search_cves_endpoint(
    query: str = Query(..., description="Keyword search query."),
    top_k: int = Query(5, description="Maximum number of CVEs to retrieve."),
    severity: Optional[str] = Query(None, description="Filter by severity."),
    vendor: Optional[str] = Query(None, description="Filter by vendor."),
    product: Optional[str] = Query(None, description="Filter by product."),
    cwe: Optional[str] = Query(None, description="Filter by CWE ID.")
) -> dict[str, Any]:
    """Search for CVEs using keyword search.

    Parameters
    ----------
    query : str
        Keyword search query.
    top_k : int, optional
        Maximum number of matches to return.
    severity : str, optional
        Filter by severity.
    vendor : str, optional
        Filter by vendor.
    product : str, optional
        Filter by product.
    cwe : str, optional
        Filter by CWE ID.

    Returns
    -------
    dict
        Response containing the original query, results, and count of matches.

    Raises
    ------
    HTTPException
        If the query validation fails (status code 400).
    """
    try:
        results = search_cves_fts(
            query=query,
            top_k=top_k,
            severity=severity,
            vendor=vendor,
            product=product,
            cwe=cwe
        )
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
