"""Import the raw NVD CVE dataset into SQLite for deployment builds."""

import logging
from pathlib import Path
from typing import Any

from app.core.db import initialize_database, rebuild_fts_index
from app.ingestion.importer import import_cve_data
from app.ingestion.loader import load_json_dataset
from app.ingestion.extractor import extract_cve_fields

RAW_DIR = Path("storage/datasets/raw")

logger = logging.getLogger(__name__)

def process_vulnerabilities_batch(vulnerabilities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [extract_cve_fields(vuln.get("cve", {})) for vuln in vulnerabilities]

def main() -> None:
    """Initialize SQLite, incrementally import yearly CVE feeds, rebuild FTS, and exit."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    initialize_database()
    
    raw_files = sorted(list(RAW_DIR.glob("nvdcve-2.0-*.json.gz")) + list(RAW_DIR.glob("nvdcve-2.0-*.json")))
    
    if not raw_files:
        logger.info(f"No raw files found in {RAW_DIR}")
        return

    total_imported = 0

    for raw_file in raw_files:
        if raw_file.name == "nvd_cves.json":
            continue
            
        logger.info(f"Processing {raw_file}...")
        dataset = load_json_dataset(str(raw_file))
        vulnerabilities = dataset.get("vulnerabilities", [])
        
        batch_size = 1000
        for i in range(0, len(vulnerabilities), batch_size):
            batch = vulnerabilities[i:i + batch_size]
            processed_cves = process_vulnerabilities_batch(batch)
            import_cve_data(processed_cves, rebuild_fts=False, strict=True)
            total_imported += len(processed_cves)
            
        del vulnerabilities
        del dataset
        
    logger.info(f"Total imported CVEs: {total_imported}")
    
    logger.info("Rebuilding FTS index...")
    rebuild_fts_index()
    logger.info("FTS index rebuild complete.")

if __name__ == "__main__":
    main()
