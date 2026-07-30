"""Unit tests for the CVE detail endpoint and service."""

import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.retrieval.cve_detail import get_cve_by_id

client = TestClient(app)

@pytest.fixture
def mock_db_connection():
    """Mock database connection for isolated testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # Initialize schema
    schema_path = Path("app/core/schema.sql")
    if schema_path.exists():
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())

    # Insert some mock data
    conn.executescript("""
        INSERT INTO cves (id, description, severity, cwe_id, "references") VALUES
        ('CVE-2024-0001', 'Test CVE description', 'HIGH', 'CWE-119', '["http://example.com/advisory"]');

        INSERT INTO cpes (id, uri, vendor, product, version) VALUES
        ('CPE-1', 'cpe:2.3:a:microsoft:windows:10.0', 'microsoft', 'windows', '10.0');

        INSERT INTO cve_cpes (cve_id, cpe_id) VALUES
        ('CVE-2024-0001', 'CPE-1');
    """)

    yield conn
    conn.close()

def test_get_cve_by_id_service(mock_db_connection):
    """Test get_cve_by_id service function directly."""
    with patch('app.retrieval.cve_detail.get_db_connection') as mock_get_db:
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db.return_value = mock_ctx

        # Valid CVE
        cve_data = get_cve_by_id("CVE-2024-0001")
        assert cve_data is not None
        assert cve_data["id"] == "CVE-2024-0001"
        assert cve_data["description"] == "Test CVE description"
        assert len(cve_data["references"]) == 1
        assert cve_data["references"][0] == "http://example.com/advisory"

        assert len(cve_data["cpes"]) == 1
        assert cve_data["cpes"][0]["vendor"] == "microsoft"

        # Invalid CVE
        assert get_cve_by_id("CVE-NONEXISTENT") is None

def test_get_cve_endpoint(mock_db_connection):
    """Test GET /cve/{cve_id} endpoint."""
    with patch('app.api.routes.get_cve_by_id') as mock_get_cve:
        mock_cve_data = {
            "id": "CVE-2024-0001",
            "description": "Test CVE description",
            "severity": "HIGH",
            "references": ["http://example.com/advisory"],
            "cpes": [
                {"id": "CPE-1", "vendor": "microsoft"}
            ]
        }

        # Valid request
        mock_get_cve.return_value = mock_cve_data
        response = client.get("/cve/CVE-2024-0001")
        assert response.status_code == 200
        assert response.json()["id"] == "CVE-2024-0001"

        # Invalid request (404)
        mock_get_cve.return_value = None
        response = client.get("/cve/CVE-NONEXISTENT")
        assert response.status_code == 404
        assert response.json()["detail"] == "CVE CVE-NONEXISTENT not found"
