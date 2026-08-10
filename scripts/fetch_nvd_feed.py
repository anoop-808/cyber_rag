#!/usr/bin/env python3
"""Fetch NVD 2.0 yearly JSON feeds."""

import argparse
import logging
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def fetch_feed(year: int, dest_dir: Path, force: bool = False) -> None:
    url = f"https://nvd.nist.gov/feeds/json/cve/2.0/nvdcve-2.0-{year}.json.gz"
    dest_file = dest_dir / f"nvdcve-2.0-{year}.json.gz"
    
    if dest_file.exists() and not force:
        logger.info("File %s already exists. Skipping download.", dest_file)
        return
        
    logger.info("Downloading NVD feed for %d from %s", year, url)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'CyberRAG-Importer/1.0'})
        with urllib.request.urlopen(req) as response:
            with open(dest_file, 'wb') as out_file:
                out_file.write(response.read())
        logger.info("Successfully downloaded to %s", dest_file)
    except urllib.error.HTTPError as e:
        logger.error("HTTP Error %s while downloading %s", e.code, url)
        raise
    except Exception as e:
        logger.error("Error downloading %s: %s", url, e)
        raise

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = argparse.ArgumentParser(description="Fetch NVD 2.0 yearly JSON feeds.")
    parser.add_argument("--start-year", type=int, default=2016, help="Start year (default: 2016)")
    parser.add_argument("--end-year", type=int, default=datetime.now().year, help="End year (inclusive, default: current year)")
    parser.add_argument("--force", action="store_true", help="Force refresh existing files")
    parser.add_argument("--dest", type=str, default="storage/datasets/raw", help="Destination directory")
    
    args = parser.parse_args()
    
    dest_dir = Path(args.dest)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    for year in range(args.start_year, args.end_year + 1):
        try:
            fetch_feed(year, dest_dir, force=args.force)
        except Exception as e:
            logger.error("Failed to fetch feed for %d: %s", year, e)
            raise SystemExit(1)

if __name__ == "__main__":
    main()
