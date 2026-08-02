"""FastAPI routes for CyberRAG RAG endpoint."""

from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.search.sqlite_search import search_cves_fts
from app.api.models import AskRequest, AskResponse
from app.rag.pipeline import generate_answer
import logging
import time

from app.retrieval.cve_detail import get_cve_detail
logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> dict[str, Any]:
    """Answer a cybersecurity question using the RAG pipeline.

    Parameters
    ----------
    request : AskRequest
        Request containing the query and optional filters.

    Returns
    -------
    dict
        Response containing the generated answer, sources, and metadata.

    Raises
    ------
    HTTPException
        If the query validation fails (status code 400) or an internal error occurs (status code 500).
    """
    logger.info(f"Received /ask request. Query length: {len(request.query) if request.query else 0}")
    start_time = time.time()
    try:
        response = generate_answer(query=request.query, filters=request.filters)
        duration = time.time() - start_time
        logger.info(f"Successfully processed /ask request in {duration:.2f}s")
        return response
    except ValueError as exc:
        logger.warning(f"Validation error in /ask: {exc}")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.error(f"Runtime error in /ask: {exc}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
    except Exception as exc:
        logger.error(f"Unexpected error in /ask: {exc}")
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc

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
