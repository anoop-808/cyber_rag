"""Metadata filtering engine for CyberRAG."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def apply_filters(
    results: list[dict[str, Any]], filters: dict[str, Any]
) -> list[dict[str, Any]]:
    """Filter retrieval results using structured CVE metadata.

    Parameters
    ----------
    results : list of dict
        The ranked results produced by the retrieval engine.
        Each result must contain a ``metadata`` dictionary.
    filters : dict
        A dictionary of metadata constraints. Supported keys are:
        - severity
        - cvss_score
        - vendor
        - product
        - cwe
        - publication_year

    Returns
    -------
    list of dict
        A filtered list of documents satisfying all supplied filters.
        The original document schema is preserved.

    Raises
    ------
    ValueError
        If an unsupported or malformed filter key is provided.
    """
    if not results:
        return []

    if not filters:
        return results

    supported_filters = {
        "severity",
        "cvss_score",
        "vendor",
        "product",
        "cwe",
        "publication_year",
    }

    # Validate filters
    for key in filters:
        if key not in supported_filters:
            raise ValueError(f"Unsupported filter key: {key}")

    filtered_results = []

    for result in results:
        metadata = result.get("metadata", {})

        # Check if the result passes all filters
        passes_all = True
        for key, filter_val in filters.items():
            if filter_val is None:
                continue

            meta_val = metadata.get(key)
            if meta_val is None:
                passes_all = False
                break

            # Perform type-appropriate matching
            if key == "cvss_score":
                try:
                    if float(meta_val) != float(filter_val):
                        passes_all = False
                        break
                except ValueError:
                    passes_all = False
                    break
            elif key == "publication_year":
                try:
                    if int(meta_val) != int(filter_val):
                        passes_all = False
                        break
                except ValueError:
                    passes_all = False
                    break
            else:
                # String comparison, case-insensitive
                if str(meta_val).strip().lower() != str(filter_val).strip().lower():
                    passes_all = False
                    break

        if passes_all:
            filtered_results.append(result)

    logger.info(
        f"Filter execution: Applied {len([k for k, v in filters.items() if v is not None])} filters. "
        f"Input count: {len(results)}. Output count: {len(filtered_results)}."
    )

    return filtered_results
