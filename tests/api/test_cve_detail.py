"""Tests for the API routes including CVE detail."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sqlite3
from pathlib import Path

from app.main import app

@pytest.fixture
def mock_db_connection():
    """Mock database connection for isolated testing."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    # Initialize schema
    schema_path = Path("app/core/schema.sql")
    if schema_path.exists():
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())

    # Insert some mock data
    conn.executescript("""
        INSERT INTO cwes (id, name, description) VALUES
        ('CWE-79', 'Improper Neutralization of Input During Web Page Generation (Cross-site Scripting)', 'XSS');

        INSERT INTO cves (
            id, description, published, modified, severity,
            cvss_version, cvss_score, cvss_vector,
            attack_vector, attack_complexity, privileges_required, user_interaction,
            scope, confidentiality, integrity, availability,
            cwe_id, "references"
        ) VALUES (
            'CVE-2024-3094', 'Malicious code was discovered in xz', '2024-03-29', '2024-03-30', 'CRITICAL',
            '3.1', 10.0, 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H',
            'NETWORK', 'LOW', 'NONE', 'NONE',
            'CHANGED', 'HIGH', 'HIGH', 'HIGH',
            'CWE-79', '["https://example.com/reference1", "https://example.com/reference2"]'
        );

        INSERT INTO cpes (id, uri, vendor, product, version) VALUES
        ('CPE-1', 'cpe:2.3:a:tukaani:xz:5.6.0:*:*:*:*:*:*:*', 'tukaani', 'xz', '5.6.0');

        INSERT INTO cve_cpes (cve_id, cpe_id) VALUES
        ('CVE-2024-3094', 'CPE-1');
    """)

    yield conn
    conn.close()


@pytest.fixture
def client():
    """Return FastAPI TestClient."""
    return TestClient(app)


def test_get_cve_detail_success(client, mock_db_connection):
    """Test retrieving an existing CVE."""
    with patch('app.retrieval.cve_detail.get_db_connection') as mock_get_db:
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db.return_value = mock_ctx

        response = client.get("/cve/CVE-2024-3094")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == "CVE-2024-3094"
        assert data["description"] == "Malicious code was discovered in xz"
        assert data["severity"] == "CRITICAL"
        assert data["cwe"]["id"] == "CWE-79"
        assert data["cwe"]["name"] == "Improper Neutralization of Input During Web Page Generation (Cross-site Scripting)"
        assert len(data["cpes"]) == 1
        assert data["cpes"][0]["vendor"] == "tukaani"
        assert len(data["references"]) == 2
        assert data["references"][0] == "https://example.com/reference1"


def test_get_cve_detail_not_found(client, mock_db_connection):
    """Test retrieving a non-existent CVE returns 404."""
    with patch('app.retrieval.cve_detail.get_db_connection') as mock_get_db:
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db.return_value = mock_ctx

        response = client.get("/cve/CVE-UNKNOWN")
        assert response.status_code == 404
        assert response.json() == {"detail": "CVE not found"}


def test_search_regression(client):
    """Verify that the existing /search endpoint still functions."""
    # We will just mock the actual search function to test the routing
    with patch('app.api.routes.search_cves_fts') as mock_search:
        mock_search.return_value = [
            {"id": "CVE-2024-123", "description": "Test", "severity": "HIGH"}
        ]

        response = client.get("/search?query=test")
        assert response.status_code == 200

        data = response.json()
        assert data["query"] == "test"
        assert data["count"] == 1
        assert data["results"][0]["id"] == "CVE-2024-123"
