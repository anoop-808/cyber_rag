"""Tests for the standalone NVD SQLite import script."""

from unittest.mock import Mock

import scripts.import_nvd as import_nvd


def test_import_nvd_runs_build_phase_steps(monkeypatch):
    """The build script should load data, import it, rebuild FTS, and exit."""
    records = [{"id": "CVE-2024-0001"}]
    load_json_dataset = Mock(return_value=records)
    initialize_database = Mock()
    import_cve_data = Mock()
    rebuild_fts_index = Mock()

    monkeypatch.setattr(import_nvd, "load_json_dataset", load_json_dataset)
    monkeypatch.setattr(import_nvd, "initialize_database", initialize_database)
    monkeypatch.setattr(import_nvd, "import_cve_data", import_cve_data)
    monkeypatch.setattr(import_nvd, "rebuild_fts_index", rebuild_fts_index)

    import_nvd.main()

    load_json_dataset.assert_called_once_with(str(import_nvd.PROCESSED_CVES_PATH))
    initialize_database.assert_called_once_with()
    import_cve_data.assert_called_once_with(records, rebuild_fts=False, strict=True)
    rebuild_fts_index.assert_called_once_with()
