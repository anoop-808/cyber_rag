"""Tests for the standalone NVD SQLite import script."""

from pathlib import Path
from unittest.mock import Mock, call

import scripts.import_nvd as import_nvd


def test_import_nvd_runs_build_phase_steps(monkeypatch):
    """The build script should incrementally load raw data in batches, import it, rebuild FTS, and exit."""
    
    # Mock RAW_DIR glob to return a normal feed and the legacy file
    mock_raw_dir = Mock()
    file1 = Mock(name="file1")
    file1.name = "nvdcve-2.0-2024.json"
    file1.__str__ = Mock(return_value="storage/datasets/raw/nvdcve-2.0-2024.json")
    
    file_legacy = Mock(name="legacy")
    file_legacy.name = "nvd_cves.json"
    
    mock_raw_dir.glob.side_effect = lambda pat: [file1] if pat.endswith("*.json") else []
    
    monkeypatch.setattr(import_nvd, "RAW_DIR", mock_raw_dir)

    raw_dataset = {
        "vulnerabilities": [
            {"cve": {"id": "CVE-2024-0001"}},
            {"cve": {"id": "CVE-2024-0002"}},
        ]
    }
    load_json_dataset = Mock(return_value=raw_dataset)
    initialize_database = Mock()
    import_cve_data = Mock()
    rebuild_fts_index = Mock()

    # Mock extract_cve_fields to avoid real parsing logic in this integration test
    monkeypatch.setattr(import_nvd, "extract_cve_fields", lambda x: {"id": x["id"], "processed": True})
    
    monkeypatch.setattr(import_nvd, "load_json_dataset", load_json_dataset)
    monkeypatch.setattr(import_nvd, "initialize_database", initialize_database)
    monkeypatch.setattr(import_nvd, "import_cve_data", import_cve_data)
    monkeypatch.setattr(import_nvd, "rebuild_fts_index", rebuild_fts_index)

    # Force a small batch size to test batching logic
    # In python, variables inside functions can't be easily mocked without mocking the whole function,
    # but we can test that import_cve_data gets called correctly.
    
    # We will test the default batch size of 1000 since there are only 2 items.
    import_nvd.main()

    initialize_database.assert_called_once_with()
    
    # Should only load the non-legacy file
    load_json_dataset.assert_called_once_with("storage/datasets/raw/nvdcve-2.0-2024.json")
    
    expected_processed = [
        {"id": "CVE-2024-0001", "processed": True},
        {"id": "CVE-2024-0002", "processed": True}
    ]
    import_cve_data.assert_called_once_with(expected_processed, rebuild_fts=False, strict=True)
    
    rebuild_fts_index.assert_called_once_with()
