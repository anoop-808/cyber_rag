"""Field extraction utilities for NVD CVE records."""

from typing import Any

CVSS_METRIC_PRIORITY = (
    "cvssMetricV31",
    "cvssMetricV30",
    "cvssMetricV2",
)


def get_english_description(
    descriptions: list[dict[str, Any]] | None,
) -> str | None:
    """Return the English description text from an NVD descriptions list.

    Parameters
    ----------
    descriptions : list of dict or None
        NVD ``descriptions`` array from a CVE record.

    Returns
    -------
    str or None
        English description value, or ``None`` if unavailable.
    """
    if not descriptions:
        return None

    for entry in descriptions:
        if entry.get("lang") == "en":
            return entry.get("value")

    return None


def get_cvss_base_score(metrics: dict[str, Any] | None) -> float | None:
    """Return the CVSS base score from the highest-priority metric available.

    Parameters
    ----------
    metrics : dict or None
        NVD ``metrics`` object from a CVE record.

    Returns
    -------
    float or None
        CVSS base score, or ``None`` if no metric is present.
    """
    if not metrics:
        return None

    for metric_key in CVSS_METRIC_PRIORITY:
        metric_entries = metrics.get(metric_key)
        if not metric_entries:
            continue

        cvss_data = metric_entries[0].get("cvssData", {})
        base_score = cvss_data.get("baseScore")
        if base_score is not None:
            return base_score

    return None


def get_cwe_ids(weaknesses: list[dict[str, Any]] | None) -> list[str]:
    """Return English CWE identifiers from an NVD weaknesses list.

    Parameters
    ----------
    weaknesses : list of dict or None
        NVD ``weaknesses`` array from a CVE record.

    Returns
    -------
    list of str
        CWE identifiers, or an empty list if none are present.
    """
    if not weaknesses:
        return []

    cwe_ids: list[str] = []
    for weakness in weaknesses:
        for entry in weakness.get("description", []):
            if entry.get("lang") == "en":
                value = entry.get("value")
                if value:
                    cwe_ids.append(value)

    return cwe_ids


def get_reference_urls(references: list[dict[str, Any]] | None) -> list[str]:
    """Return reference URLs from an NVD references list.

    Parameters
    ----------
    references : list of dict or None
        NVD ``references`` array from a CVE record.

    Returns
    -------
    list of str
        Reference URLs, or an empty list if none are present.
    """
    if not references:
        return []

    urls: list[str] = []
    for reference in references:
        url = reference.get("url")
        if url:
            urls.append(url)

    return urls


def extract_cve_fields(cve: dict[str, Any]) -> dict[str, Any]:
    """Extract and normalize key fields from a single NVD CVE record.

    Parameters
    ----------
    cve : dict
        The ``cve`` object from an NVD ``vulnerabilities`` entry.

    Returns
    -------
    dict
        Cleaned record with keys ``id``, ``description``, ``published``,
        ``last_modified``, ``cvss_score``, ``cwe``, and ``references``.
        Missing scalar values are ``None``; missing lists are ``[]``.

    Notes
    -----
    The input dictionary is read only and is not modified.
    """
    return {
        "id": cve.get("id"),
        "description": get_english_description(cve.get("descriptions")),
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        "cvss_score": get_cvss_base_score(cve.get("metrics")),
        "cwe": get_cwe_ids(cve.get("weaknesses")),
        "references": get_reference_urls(cve.get("references")),
    }
