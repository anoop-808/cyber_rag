"""Unit tests for SQLite FTS5 search."""

import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from app.search.sqlite_search import search_cves_fts
from app.core.db import rebuild_fts_index


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
        INSERT INTO cves (id, description, severity, cwe_id) VALUES
        ('CVE-1', 'buffer overflow in parser', 'HIGH', 'CWE-119'),
        ('CVE-2', 'sql injection in login page', 'CRITICAL', 'CWE-89'),
        ('CVE-3', 'cross site scripting in comment section', 'MEDIUM', 'CWE-79');

        INSERT INTO cpes (id, uri, vendor, product) VALUES
        ('CPE-1', 'uri-1', 'microsoft', 'windows'),
        ('CPE-2', 'uri-2', 'apache', 'http_server');

        INSERT INTO cve_cpes (cve_id, cpe_id) VALUES
        ('CVE-1', 'CPE-1'),
        ('CVE-2', 'CPE-2');
    """)

    yield conn
    conn.close()


def test_search_cves_fts_basic(mock_db_connection):
    """Test basic keyword search."""
    with patch('app.core.db.get_db_connection') as mock_get_db:
        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db.return_value = mock_ctx

        # We also need to patch get_db_connection in the module where search_cves_fts is imported,
        # but since we're using get_db_connection via from app.core.db import ..., we should patch
        # app.search.sqlite_search.get_db_connection
        with patch('app.search.sqlite_search.get_db_connection', return_value=mock_ctx):
            # First rebuild the FTS index
            with patch('app.core.db.get_db_connection', return_value=mock_ctx):
                rebuild_fts_index()

            # Test search
            results = search_cves_fts(query="overflow")
            assert len(results) == 1
            assert results[0]["id"] == "CVE-1"
            assert "buffer overflow" in results[0]["description"]

            # Test another search
            results = search_cves_fts(query="injection")
            assert len(results) == 1
            assert results[0]["id"] == "CVE-2"

def test_search_cves_fts_filters(mock_db_connection):
    """Test keyword search with filters."""
    with patch('app.search.sqlite_search.get_db_connection') as mock_get_db_search, \
         patch('app.core.db.get_db_connection') as mock_get_db_core:

        mock_ctx = MagicMock()
        mock_ctx.__enter__.return_value = mock_db_connection
        mock_get_db_search.return_value = mock_ctx
        mock_get_db_core.return_value = mock_ctx

        # Rebuild index
        rebuild_fts_index()

        # Test severity filter
        results = search_cves_fts(query="login", severity="CRITICAL")
        assert len(results) == 1
        assert results[0]["id"] == "CVE-2"

        # Test vendor filter
        results = search_cves_fts(query="overflow", vendor="microsoft")
        assert len(results) == 1
        assert results[0]["id"] == "CVE-1"

        # Test non-matching filter
        results = search_cves_fts(query="overflow", vendor="apache")
        assert len(results) == 0

def test_search_cves_fts_empty_query():
    """Test search with empty query raises ValueError."""
    with pytest.raises(ValueError, match="Query must not be empty"):
        search_cves_fts(query="   ")
