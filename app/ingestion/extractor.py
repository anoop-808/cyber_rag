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


def extract_cvss_data(metrics: dict[str, Any] | None) -> dict[str, Any]:
    """Extract full CVSS data from the highest-priority metric available.

    Parameters
    ----------
    metrics : dict or None
        NVD ``metrics`` object from a CVE record.

    Returns
    -------
    dict
        Dictionary containing extracted CVSS fields.
    """
    result = {
        "cvss_version": None,
        "cvss_score": None,
        "cvss_vector": None,
        "severity": None,
        "attack_vector": None,
        "attack_complexity": None,
        "privileges_required": None,
        "user_interaction": None,
        "scope": None,
        "confidentiality": None,
        "integrity": None,
        "availability": None,
    }

    if not metrics:
        return result

    for metric_key in CVSS_METRIC_PRIORITY:
        metric_entries = metrics.get(metric_key)
        if not metric_entries:
            continue

        entry = metric_entries[0]
        cvss_data = entry.get("cvssData", {})

        result["cvss_version"] = cvss_data.get("version")
        result["cvss_score"] = cvss_data.get("baseScore")
        result["cvss_vector"] = cvss_data.get("vectorString")

        # Severity might be in cvssData or the main entry
        result["severity"] = cvss_data.get("baseSeverity") or entry.get("baseSeverity")

        result["attack_vector"] = cvss_data.get("attackVector") or cvss_data.get("accessVector")
        result["attack_complexity"] = cvss_data.get("attackComplexity") or cvss_data.get("accessComplexity")
        result["privileges_required"] = cvss_data.get("privilegesRequired") or cvss_data.get("authentication")
        result["user_interaction"] = cvss_data.get("userInteraction") or ("NONE" if cvss_data.get("userInteractionRequired") is False else "REQUIRED" if cvss_data.get("userInteractionRequired") is True else None)
        result["scope"] = cvss_data.get("scope")
        result["confidentiality"] = cvss_data.get("confidentialityImpact")
        result["integrity"] = cvss_data.get("integrityImpact")
        result["availability"] = cvss_data.get("availabilityImpact")

        # We found a valid metric
        if result["cvss_score"] is not None:
            break

    return result

def extract_cpes(configurations: list[dict[str, Any]] | None) -> list[dict[str, str]]:
    """Extract CPEs from configurations array.

    Parameters
    ----------
    configurations : list or None
        NVD ``configurations`` array from a CVE record.

    Returns
    -------
    list of dict
        Extracted CPE information.
    """
    if not configurations:
        return []

    cpes = []
    for config in configurations:
        for node in config.get("nodes", []):
            for match in node.get("cpeMatch", []):
                criteria = match.get("criteria")
                if not criteria:
                    continue

                parts = criteria.split(":")

                # Minimum cpe format: cpe:2.3:part:vendor:product:version
                cpe_dict = {
                    "id": match.get("matchCriteriaId") or criteria,
                    "uri": criteria,
                    "vendor": parts[3] if len(parts) > 3 and parts[3] != "*" else None,
                    "product": parts[4] if len(parts) > 4 and parts[4] != "*" else None,
                    "version": parts[5] if len(parts) > 5 and parts[5] != "*" else None,
                }
                cpes.append(cpe_dict)

    return cpes


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
        Cleaned record containing fields suitable for the database schema.

    Notes
    -----
    The input dictionary is read only and is not modified.
    """
    cvss_data = extract_cvss_data(cve.get("metrics"))

    return {
        "id": cve.get("id"),
        "description": get_english_description(cve.get("descriptions")),
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        **cvss_data,
        "cwe": get_cwe_ids(cve.get("weaknesses")),
        "references": get_reference_urls(cve.get("references")),
        "cpes": extract_cpes(cve.get("configurations")),
    }
