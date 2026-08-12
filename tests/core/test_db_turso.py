import os
import sqlite3
import pytest
from unittest.mock import patch
from typing import Generator
from app.core.db import get_db_connection, initialize_database, LibsqlConnectionWrapper

@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    # Remove Turso variables if they exist
    orig_url = os.environ.get("TURSO_DATABASE_URL")
    orig_token = os.environ.get("TURSO_AUTH_TOKEN")
    
    if "TURSO_DATABASE_URL" in os.environ:
        del os.environ["TURSO_DATABASE_URL"]
    if "TURSO_AUTH_TOKEN" in os.environ:
        del os.environ["TURSO_AUTH_TOKEN"]
        
    yield
    
    # Restore
    if orig_url is not None:
        os.environ["TURSO_DATABASE_URL"] = orig_url
    if orig_token is not None:
        os.environ["TURSO_AUTH_TOKEN"] = orig_token


def test_missing_turso_credentials_fallback(clean_env):
    """Test that missing Turso credentials fall back safely to local SQLite."""
    os.environ["TURSO_DATABASE_URL"] = "http://test-url"
    # TURSO_AUTH_TOKEN is missing
    with get_db_connection() as conn:
        assert isinstance(conn, sqlite3.Connection)


def test_local_sqlite_fallback(clean_env):
    """Test that local SQLite is used when no Turso credentials are provided."""
    with get_db_connection() as conn:
        assert isinstance(conn, sqlite3.Connection)


import sys
from unittest.mock import MagicMock

def test_turso_connection_configuration(clean_env):
    """Test that Turso connection is used when credentials are provided."""
    os.environ["TURSO_DATABASE_URL"] = "libsql://turso-test-url"
    os.environ["TURSO_AUTH_TOKEN"] = "test-token"
    
    mock_libsql = MagicMock()
    sys.modules["libsql_client"] = mock_libsql
    
    try:
        with get_db_connection() as conn:
            assert isinstance(conn, LibsqlConnectionWrapper)
            # Access _client to trigger lazy initialization
            _ = conn._client
            mock_libsql.create_client_sync.assert_called_once_with(url="https://turso-test-url", auth_token="test-token")
    finally:
        if "libsql_client" in sys.modules:
            del sys.modules["libsql_client"]


@patch("app.core.db.Path.is_file", return_value=True)
@patch("app.core.db.Path.open")
def test_production_startup_skips_schema_init(mock_open, mock_is_file, clean_env):
    """Test that production startup does not attempt local schema initialization when Turso is configured."""
    os.environ["TURSO_DATABASE_URL"] = "http://turso-test-url"
    os.environ["TURSO_AUTH_TOKEN"] = "test-token"
    
    initialize_database()
    mock_open.assert_not_called()


def test_turso_wrapper_row_access_and_select():
    """Test that the Turso wrapper allows row access by column name and SELECT query execution."""
    from app.core.db import LibsqlCursorWrapper

    class MockResultSet:
        def __init__(self):
            self.columns = ('id', 'description', 'severity', 'cwe_id')
            self.rows = [
                ('CVE-1999-0095', 'Test description', 'HIGH', 'NVD-CWE-Other'),
                ('CVE-1999-0096', 'Test description 2', 'MEDIUM', 'NVD-CWE-Other')
            ]

    class MockClient:
        def execute(self, sql, args):
            return MockResultSet()

    cursor = LibsqlCursorWrapper(MockClient())
    cursor.execute("SELECT * FROM t")
    
    # Test fetchone
    row = cursor.fetchone()
    assert row is not None
    # Access by column name
    assert row["id"] == "CVE-1999-0095"
    assert row["description"] == "Test description"
    assert row["severity"] == "HIGH"
    assert row["cwe_id"] == "NVD-CWE-Other"
    
    # Access by index
    assert row[0] == "CVE-1999-0095"
    assert row[1] == "Test description"

    # Test iteration
    row2 = next(cursor)
    assert row2["id"] == "CVE-1999-0096"
    assert row2["severity"] == "MEDIUM"

    # Test fetchall
    cursor.execute("SELECT * FROM t")
    rows = cursor.fetchall()
    assert len(rows) == 2
    assert rows[0]["id"] == "CVE-1999-0095"
    assert rows[1]["id"] == "CVE-1999-0096"
