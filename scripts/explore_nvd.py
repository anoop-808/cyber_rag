"""Explore the structure and sample fields of the NVD CVE JSON dataset."""

from typing import Any

from app.ingestion.loader import load_json_dataset

NVD_DATASET_PATH = "storage/datasets/raw/nvd_cves.json"

CVSS_METRIC_PRIORITY = (
    "cvssMetricV31",
    "cvssMetricV30",
    "cvssMetricV2",
)


def get_english_description(descriptions: list[dict[str, Any]] | None) -> str | None:
    """Return the English description text, if present."""
    if not descriptions:
        return None

    for entry in descriptions:
        if entry.get("lang") == "en":
            return entry.get("value")

    return None


def get_cvss_base_score(metrics: dict[str, Any] | None) -> float | None:
    """Return the CVSS base score from the highest-priority metric version available."""
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
    """Return English CWE identifiers listed under weaknesses."""
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


def format_optional(value: Any) -> str:
    """Format a value for display, using a placeholder when missing."""
    if value is None:
        return "Not available"
    if isinstance(value, list) and not value:
        return "Not available"
    return str(value)


def main() -> None:
    """Load the NVD dataset and print summary and first-vulnerability details."""
    dataset = load_json_dataset(NVD_DATASET_PATH)

    results_per_page = dataset.get("resultsPerPage")
    total_results = dataset.get("totalResults")
    vulnerabilities = dataset.get("vulnerabilities", [])

    print("NVD Dataset Summary")
    print("-" * 40)
    print(f"Results Per Page: {format_optional(results_per_page)}")
    print(f"Total Results: {format_optional(total_results)}")
    print(f"Number of vulnerabilities loaded: {len(vulnerabilities)}")
    print()

    if not vulnerabilities:
        print("No vulnerabilities found in the dataset.")
        return

    first_vulnerability = vulnerabilities[0].get("cve", {})
    cwe_ids = get_cwe_ids(first_vulnerability.get("weaknesses"))

    print("First Vulnerability")
    print("-" * 40)
    print(f"CVE ID: {format_optional(first_vulnerability.get('id'))}")
    print(
        "Description: "
        f"{format_optional(get_english_description(first_vulnerability.get('descriptions')))}"
    )
    print(f"Published Date: {format_optional(first_vulnerability.get('published'))}")
    print(
        "Last Modified Date: "
        f"{format_optional(first_vulnerability.get('lastModified'))}"
    )
    print(
        "CVSS Base Score: "
        f"{format_optional(get_cvss_base_score(first_vulnerability.get('metrics')))}"
    )
    print(f"CWE: {format_optional(cwe_ids if cwe_ids else None)}")


if __name__ == "__main__":
    main()
