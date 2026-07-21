"""Prompt builder for CyberRAG LLM interactions."""

from typing import Any

_SYSTEM_INSTRUCTION_WITH_CONTEXT = (
    "You are a cybersecurity knowledge assistant. Answer the user's question "
    "using ONLY the retrieved CVE information provided below. Do not use "
    "external knowledge or invent details not present in the retrieved CVEs."
)

_SYSTEM_INSTRUCTION_WITHOUT_CONTEXT = (
    "You are a cybersecurity knowledge assistant. No relevant CVE information "
    "was retrieved for this query. Inform the user that there is insufficient "
    "retrieved context to answer the question. Do not invent or speculate about "
    "specific CVE details."
)

_FINAL_INSTRUCTION = (
    "Answer only from the retrieved CVEs above. If the information is "
    "insufficient, explicitly state that you cannot answer based on the "
    "retrieved context."
)


def _format_cvss_score(metadata: dict[str, Any]) -> str | None:
    """Return a CVSS score string when present in result metadata."""
    cvss_score = metadata.get("cvss_score")
    if cvss_score is None:
        return None
    return str(cvss_score)


def _format_cve_entry(rank: int, result: dict[str, Any]) -> str:
    """Format a single retrieved CVE entry for inclusion in the prompt."""
    metadata = result.get("metadata", {})
    lines = [f"{rank}. CVE ID: {result.get('id', 'Unknown')}"]

    cvss_score = _format_cvss_score(metadata)
    if cvss_score is not None:
        lines.append(f"   CVSS Score: {cvss_score}")

    description = result.get("description", "Not available")
    lines.append(f"   Description: {description}")

    return "\n".join(lines)


def build_prompt(retrieval_context: dict[str, Any]) -> str:
    """Build an LLM prompt from standardized retrieval context.

    Parameters
    ----------
    retrieval_context : dict
        Retrieval response returned by ``retrieve_context()`` containing
        ``query``, ``results``, and ``count`` keys.

    Returns
    -------
    str
        A prompt string ready to send to an LLM.
    """
    query = retrieval_context.get("query", "")
    results = retrieval_context.get("results", [])

    if not results:
        system_instruction = _SYSTEM_INSTRUCTION_WITHOUT_CONTEXT
        retrieved_cves_section = "No CVEs were retrieved for this query."
    else:
        system_instruction = _SYSTEM_INSTRUCTION_WITH_CONTEXT
        cve_entries = [
            _format_cve_entry(rank, result)
            for rank, result in enumerate(results, start=1)
        ]
        retrieved_cves_section = "\n\n".join(cve_entries)

    return (
        f"=== SYSTEM ===\n{system_instruction}\n\n"
        f"=== USER QUERY ===\n{query}\n\n"
        f"=== RETRIEVED CVEs ===\n{retrieved_cves_section}\n\n"
        f"{_FINAL_INSTRUCTION}"
    )
