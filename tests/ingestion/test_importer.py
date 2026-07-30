"""Unit tests for NVD CVE importer."""

import json
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from app.ingestion.importer import import_cve_data


@pytest.fixture
def mock_db_connection():
    """Mock database connection for isolated testing."""
    # Use an in-memory database for testing
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # Initialize schema
    schema_path = Path("app/core/schema.sql")
    if schema_path.exists():
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
    else:
        # Create a basic schema if running tests without the file
        conn.executescript('''
            CREATE TABLE cves (id TEXT PRIMARY KEY, description TEXT, published TEXT, modified TEXT, severity TEXT, cvss_version TEXT, cvss_score REAL, cvss_vector TEXT, attack_vector TEXT, attack_complexity TEXT, privileges_required TEXT, user_interaction TEXT, scope TEXT, confidentiality TEXT, integrity TEXT, availability TEXT, cwe_id TEXT, "references" TEXT);
            CREATE TABLE cpes (id TEXT PRIMARY KEY, uri TEXT UNIQUE NOT NULL, vendor TEXT, product TEXT, version TEXT);
            CREATE TABLE cve_cpes (cve_id TEXT NOT NULL, cpe_id TEXT NOT NULL, PRIMARY KEY (cve_id, cpe_id));
        ''')

    yield conn
    conn.close()


def test_import_cve_data(mock_db_connection):
    """Test importing CVE records and their relationships."""

    test_records = [
        {
            "id": "CVE-2024-1234",
            "description": "Test vulnerability",
            "published": "2024-01-01T00:00:00.000",
            "last_modified": "2024-01-02T00:00:00.000",
            "cvss_version": "3.1",
            "cvss_score": 9.8,
            "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            "severity": "CRITICAL",
            "attack_vector": "NETWORK",
            "attack_complexity": "LOW",
            "privileges_required": "NONE",
            "user_interaction": "NONE",
            "scope": "UNCHANGED",
            "confidentiality": "HIGH",
            "integrity": "HIGH",
            "availability": "HIGH",
            "cwe": ["CWE-79"],
            "references": ["http://example.com/advisory"],
            "cpes": [
                {
                    "id": "cpe-uuid-1",
                    "uri": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*",
                    "vendor": "vendor",
                    "product": "product",
                    "version": "1.0"
                }
            ]
        }
    ]

    # Patch get_db_connection to return our in-memory DB
    with patch('app.ingestion.importer.get_db_connection') as mock_get_db:
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db.return_value = mock_ctx

        import_cve_data(test_records)

        # Verify CVE was inserted
        cursor = mock_db_connection.cursor()
        cursor.execute("SELECT * FROM cves WHERE id = 'CVE-2024-1234'")
        cve_row = cursor.fetchone()
        assert cve_row is not None
        assert cve_row["description"] == "Test vulnerability"
        assert cve_row["cvss_score"] == 9.8
        assert cve_row["cwe_id"] == "CWE-79"
        assert json.loads(cve_row["references"]) == ["http://example.com/advisory"]

        # Verify CPE was inserted
        cursor.execute("SELECT * FROM cpes WHERE id = 'cpe-uuid-1'")
        cpe_row = cursor.fetchone()
        assert cpe_row is not None
        assert cpe_row["vendor"] == "vendor"

        # Verify relationship was created
        cursor.execute("SELECT * FROM cve_cpes WHERE cve_id = 'CVE-2024-1234' AND cpe_id = 'cpe-uuid-1'")
        cve_cpe_row = cursor.fetchone()
        assert cve_cpe_row is not None


def test_import_cve_missing_id():
    """Test importing CVE with missing ID handles gracefully."""
    test_records = [{"description": "Missing ID"}]

    with patch('app.ingestion.importer.get_db_connection') as mock_get_db:
        mock_conn = MagicMock()
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_conn
        mock_get_db.return_value = mock_ctx

        # It should log error but not crash
        with patch('app.ingestion.importer.logger') as mock_logger:
            import_cve_data(test_records)
            mock_logger.error.assert_called_once()

        # Commit should still be called
        mock_conn.commit.assert_called_once()
