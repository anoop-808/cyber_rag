"""Context Builder for CyberRAG."""

import logging
from typing import Any

logger = logging.getLogger(__name__)

def build_context(
    retrieved_documents: list[dict[str, Any]],
    max_documents: int = 10,
    max_characters: int = 10000,
) -> str:
    """Transform retrieved CVE documents into a clean context block.

    Parameters
    ----------
    retrieved_documents : list of dict
        The documents returned by the unified retrieval pipeline.
    max_documents : int, optional
        Maximum number of documents to include in the context. Default is 10.
    max_characters : int, optional
        Maximum length of the generated context string. Default is 10000.

    Returns
    -------
    str
        A formatted, deterministic context block suitable for LLM consumption.
    """
    if not retrieved_documents:
        logger.info("Context Builder: 0 retrieved documents provided.")
        return ""

    included_count = 0
    final_context = ""
    separator = "\n\n------------------\n\n"

    for doc in retrieved_documents:
        if included_count >= max_documents:
            break

        cve_id = doc.get("id", "UNKNOWN")
        description = doc.get("description", "No description available.")

        # Handle fields that might be at root or in metadata
        metadata = doc.get("metadata", {})
        severity = doc.get("severity") or metadata.get("severity")
        cwe = doc.get("cwe_id") or metadata.get("cwe") or metadata.get("cwe_id")
        cvss = metadata.get("cvss_score")
        published = metadata.get("publication_year")

        parts = []
        parts.append(f"[{cve_id}]")
        parts.append(f"Description:\n{description}")

        if severity is not None:
            parts.append(f"Severity:\n{severity}")

        if cvss is not None:
            parts.append(f"CVSS:\n{cvss}")

        if published is not None:
            parts.append(f"Published:\n{published}")

        if cwe is not None:
            parts.append(f"CWE:\n{cwe}")

        doc_text = "\n\n".join(parts)

        # Calculate size if we add this document
        if included_count > 0:
            proposed_addition = separator + doc_text
        else:
            proposed_addition = doc_text

        if len(final_context) + len(proposed_addition) > max_characters:
            # Do not add if it exceeds limit. Stop processing.
            break

        final_context += proposed_addition
        included_count += 1

    logger.info(
        f"Context Builder: Retrieved={len(retrieved_documents)}, "
        f"Included={included_count}, Final Size={len(final_context)} characters"
    )

    return final_context
