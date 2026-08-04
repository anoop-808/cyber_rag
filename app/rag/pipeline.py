"""End-to-End RAG Pipeline Orchestrator for CyberRAG."""

import logging
import time
from typing import Any

from app.retrieval.pipeline import retrieve
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_prompt
from app.llm.client import generate_response
from app.rag.response_formatter import format_response

logger = logging.getLogger(__name__)

def generate_answer(
    query: str,
    filters: dict[str, Any] | None = None,
    retrieval_pipeline: Any = None,
    llm_client: Any = None
) -> dict[str, Any]:
    """Execute the complete RAG workflow to answer a user query.

    Workflow:
    1. User Query
    2. Unified Retrieval Pipeline
    3. Context Builder
    4. Prompt Builder
    5. LLM Interface
    6. Response Formatter
    7. Final Structured Response

    Parameters
    ----------
    query : str
        The user's natural language question.
    filters : dict, optional
        Metadata filters to apply during retrieval.

    Returns
    -------
    dict
        The structured final response including the answer, sources, and metadata.

    Raises
    ------
    ValueError
        If the query is empty or retrieval/context steps return empty results.
    RuntimeError
        If any step in the pipeline fails unexpectedly.
    """
    logger.info(f"RAG Pipeline started for query (length {len(query) if query else 0})")
    start_time = time.time()

    if not query or not query.strip():
        logger.error("Empty query received.")
        raise ValueError("Query cannot be empty.")

    # Use provided dependencies or fall back to default
    if retrieval_pipeline is None:
        retrieval_pipeline = retrieve
    if llm_client is None:
        llm_client = generate_response

    # 1. Retrieval
    logger.info("Step 1/5: Retrieving documents...")
    try:
        documents = retrieval_pipeline(query=query, filters=filters)
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        raise RuntimeError(f"Retrieval failed: {e}") from e

    if not documents:
        logger.warning("Retrieval returned no documents.")
        raise ValueError("No relevant documents found for the given query.")

    # 2. Context Builder
    logger.info("Step 2/5: Building context...")
    try:
        context = build_context(retrieved_documents=documents)
    except Exception as e:
        logger.error(f"Context building failed: {e}")
        raise RuntimeError(f"Context building failed: {e}") from e

    if not context:
        logger.warning("Context builder generated empty context.")
        raise ValueError("Failed to build context from retrieved documents.")

    # 3. Prompt Builder
    logger.info("Step 3/5: Building prompt...")
    try:
        prompts = build_prompt(query=query, context=context)
    except Exception as e:
        logger.error(f"Prompt generation failed: {e}")
        raise RuntimeError(f"Prompt generation failed: {e}") from e

    # 4. LLM Interface
    logger.info("Step 4/5: Generating LLM response...")
    try:
        llm_response = llm_client(
            system_prompt=prompts["system"],
            user_prompt=prompts["user"]
        )
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise RuntimeError(f"LLM generation failed: {e}") from e

    # 5. Response Formatter
    logger.info("Step 5/5: Formatting final response...")
    try:
        final_response = format_response(
            llm_response=llm_response,
            retrieved_documents=documents
        )
    except Exception as e:
        logger.error(f"Response formatting failed: {e}")
        raise RuntimeError(f"Response formatting failed: {e}") from e

    duration = time.time() - start_time
    logger.info(f"RAG Pipeline completed successfully in {duration:.2f}s")

    return final_response
