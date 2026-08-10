"""Import the processed NVD CVE dataset into SQLite for deployment builds."""

from pathlib import Path
from typing import Any

from app.core.db import initialize_database, rebuild_fts_index
from app.ingestion.importer import import_cve_data
from app.ingestion.loader import load_json_dataset

PROCESSED_CVES_PATH = Path("storage/datasets/processed/processed_cves.json")


def main() -> None:
    """Initialize SQLite, import processed CVEs, rebuild FTS, and exit."""
    records: Any = load_json_dataset(str(PROCESSED_CVES_PATH))
    if not isinstance(records, list):
        raise ValueError(f"Expected a list of CVE records in {PROCESSED_CVES_PATH}")

    initialize_database()
    import_cve_data(records, rebuild_fts=False, strict=True)
    rebuild_fts_index()


if __name__ == "__main__":
    main()
