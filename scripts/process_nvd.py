"""Process raw NVD CVE data into a cleaned JSON dataset."""

import json
from pathlib import Path
from typing import Any

from app.ingestion.extractor import extract_cve_fields
from app.ingestion.loader import load_json_dataset

RAW_NVD_PATH = Path("storage/datasets/raw/nvd_cves.json")
PROCESSED_DIR = Path("storage/datasets/processed")
PROCESSED_OUTPUT_PATH = PROCESSED_DIR / "processed_cves.json"


def process_vulnerabilities(vulnerabilities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract cleaned CVE fields from each raw NVD vulnerability entry.

    Parameters
    ----------
    vulnerabilities : list of dict
        The ``vulnerabilities`` array from an NVD API response.

    Returns
    -------
    list of dict
        Cleaned CVE records ready for downstream ingestion.
    """
    processed_cves: list[dict[str, Any]] = []

    for vulnerability in vulnerabilities:
        cve = vulnerability.get("cve", {})
        processed_cves.append(extract_cve_fields(cve))

    return processed_cves


def save_processed_dataset(
    processed_cves: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Write processed CVE records to a JSON file.

    Parameters
    ----------
    processed_cves : list of dict
        Cleaned CVE records to persist.
    output_path : Path
        Destination file path for the processed dataset.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        json.dump(processed_cves, output_file, indent=4, ensure_ascii=False)


def main() -> None:
    """Load, process, and save the NVD CVE dataset."""
    dataset = load_json_dataset(str(RAW_NVD_PATH))
    vulnerabilities = dataset.get("vulnerabilities", [])

    processed_cves = process_vulnerabilities(vulnerabilities)
    save_processed_dataset(processed_cves, PROCESSED_OUTPUT_PATH)

    print(f"Number of raw CVEs loaded: {len(vulnerabilities)}")
    print(f"Number of processed CVEs: {len(processed_cves)}")
    print(f"Output file path: {PROCESSED_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
