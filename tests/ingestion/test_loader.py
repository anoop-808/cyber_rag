"""Tests for loader.py."""

import json
import gzip
from pathlib import Path
from app.ingestion.loader import load_json_dataset

def test_load_json_dataset_uncompressed(tmp_path):
    json_path = tmp_path / "test.json"
    data = {"vulnerabilities": []}
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f)
        
    loaded = load_json_dataset(str(json_path))
    assert loaded == data

def test_load_json_dataset_compressed(tmp_path):
    gz_path = tmp_path / "test.json.gz"
    data = {"vulnerabilities": [{"cve": {"id": "CVE-2021-1234"}}]}
    
    with gzip.open(gz_path, "wt", encoding="utf-8") as f:
        json.dump(data, f)
        
    loaded = load_json_dataset(str(gz_path))
    assert loaded == data
