"""RAG orchestrator for CyberRAG question answering."""

from typing import Any

from app.llm.client import generate_response
from app.llm.prompt_builder import build_prompt
from app.retrieval.retriever import retrieve_context


def answer_question(query: str, top_k: int = 5) -> dict[str, Any]:
    """Answer a cybersecurity question using the complete RAG pipeline.

    Parameters
    ----------
    query : str
        Natural-language question to answer.
    top_k : int, optional
        Maximum number of CVEs to retrieve. Default is 5.

    Returns
    -------
    dict
        Standardized response containing the original ``query``, the generated
        ``answer``, the ``sources`` from retrieval, and the ``count`` of matches.

    Raises
    ------
    ValueError
        If ``query`` is empty or contains only whitespace, or if ``top_k`` is
        less than or equal to 0.
    """
    if not query or not query.strip():
        raise ValueError("Query must not be empty or contain only whitespace.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    retrieval_context = retrieve_context(query, top_k=top_k)
    prompt = build_prompt(retrieval_context)
    answer = generate_response(prompt)

    return {
        "query": query,
        "answer": answer,
        "sources": retrieval_context["results"],
        "count": retrieval_context["count"],
    }
