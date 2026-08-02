from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    """
    Request model for the /ask endpoint.
    """
    query: str = Field(
        ...,
        description="The natural language question to ask the RAG pipeline.",
        examples=["How does CVE-2024-1234 work?"],
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional filters to apply to the document retrieval (e.g., severity).",
        examples=[{"severity": "CRITICAL"}],
    )

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty.")
        return v


class AskResponse(BaseModel):
    """
    Response model for the /ask endpoint.
    """
    answer: str = Field(
        ...,
        description="The generated answer from the LLM based on retrieved context.",
    )
    sources: List[str] = Field(
        ...,
        description="A list of source document IDs (e.g., CVE IDs) cited in the answer.",
        examples=[["CVE-2024-1234"]],
    )
    metadata: List[Dict[str, Any]] = Field(
        ...,
        description="Detailed metadata for each source document.",
        examples=[[{"id": "CVE-2024-1234", "severity": "CRITICAL", "cvss": 9.8}]],
    )
    confidence: Optional[float] = Field(
        default=None,
        description="An optional confidence score for the generated answer.",
    )


class SearchRequest(BaseModel):
    """
    Request model for the /search endpoint.
    """
    query: str = Field(
        ...,
        description="The query string to search for in the database.",
        examples=["Buffer overflow in OpenSSL"],
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional filters to apply to the search results.",
        examples=[{"severity": "HIGH"}],
    )

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty.")
        return v


class SearchResponse(BaseModel):
    """
    Response model for the /search endpoint.
    """
    documents: List[Dict[str, Any]] = Field(
        ...,
        description="The retrieved documents matching the search criteria.",
        examples=[
            [
                {
                    "id": "CVE-2024-1234",
                    "description": "A buffer overflow vulnerability...",
                    "metadata": {"severity": "CRITICAL"},
                    "distance": 0.123
                }
            ]
        ],
    )
