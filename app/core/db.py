"""SQLite database connection and schema management."""

import os
import sqlite3
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Any

logger = logging.getLogger(__name__)

DB_PATH = Path("storage/database.sqlite")

class TursoRow:
    """A row object that supports accessing columns by name and index."""
    def __init__(self, columns, values):
        self._columns = columns
        self._values = values
        self._mapping = dict(zip(columns, values))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return self._mapping[key]

    def keys(self):
        return self._mapping.keys()

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)


class LibsqlCursorWrapper:
    """A minimal wrapper around libsql_client.ResultSet to mimic sqlite3.Cursor."""
    def __init__(self, client: Any):
        self._client = client
        self.rows = []
        self._idx = 0

    def execute(self, sql: str, parameters: tuple = ()) -> 'LibsqlCursorWrapper':
        args = list(parameters) if parameters else []
        rs = self._client.execute(sql, args)
        if rs:
            self.rows = [TursoRow(rs.columns, row) for row in rs.rows]
        else:
            self.rows = []
        self._idx = 0
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < len(self.rows):
            row = self.rows[self._idx]
            self._idx += 1
            return row
        raise StopIteration

    def fetchone(self):
        if self._idx < len(self.rows):
            row = self.rows[self._idx]
            self._idx += 1
            return row
        return None

    def fetchall(self):
        rows = self.rows[self._idx:]
        self._idx = len(self.rows)
        return rows


class LibsqlConnectionWrapper:
    """A minimal wrapper around libsql_client.ClientSync to mimic sqlite3.Connection."""
    def __init__(self, url: str, auth_token: str):
        if url.startswith("libsql://"):
            url = "https://" + url[9:]
        self._url = url
        self._auth_token = auth_token
        self._client_instance = None

    @property
    def _client(self):
        if self._client_instance is None:
            import libsql_client
            self._client_instance = libsql_client.create_client_sync(
                url=self._url, auth_token=self._auth_token
            )
        return self._client_instance

    def cursor(self) -> LibsqlCursorWrapper:
        return LibsqlCursorWrapper(self._client)

    def execute(self, sql: str, parameters: tuple = ()) -> LibsqlCursorWrapper:
        cursor = self.cursor()
        return cursor.execute(sql, parameters)

    def executescript(self, sql_script: str) -> None:
        pass

    def commit(self) -> None:
        pass

    def close(self) -> None:
        if self._client_instance is not None:
            self._client_instance.close()


@contextmanager
def get_db_connection() -> Generator[Any, None, None]:
    """Yield a database connection and ensure it is closed afterward.

    Yields
    ------
    sqlite3.Connection or LibsqlConnectionWrapper
        The active SQLite database connection or Turso wrapper.
    """
    turso_url = os.environ.get("TURSO_DATABASE_URL")
    turso_auth = os.environ.get("TURSO_AUTH_TOKEN")

    if turso_url and turso_auth:
        conn = LibsqlConnectionWrapper(turso_url, turso_auth)
        try:
            yield conn
        finally:
            conn.close()
    else:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()


def initialize_database() -> None:
    """Initialize the database schema if it does not already exist."""
    with get_db_connection() as conn:
        if isinstance(conn, LibsqlConnectionWrapper):
            logger.info("Turso configuration detected. Skipping local SQLite schema initialization.")
            return

        schema_path = Path("app/core/schema.sql")
        if not schema_path.is_file():
            raise FileNotFoundError(f"Schema file not found at {schema_path}")

        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()


def rebuild_fts_index() -> None:
    """Rebuild the FTS5 search index from existing tables."""
    with get_db_connection() as conn:
        if isinstance(conn, LibsqlConnectionWrapper):
            logger.info("Turso configuration detected. Skipping FTS index rebuild.")
            return

        conn.execute("DELETE FROM cves_fts;")
        conn.execute("""
            INSERT INTO cves_fts (id, description, severity, cwe_id, vendor, product)
            SELECT
                c.id,
                c.description,
                c.severity,
                c.cwe_id,
                GROUP_CONCAT(cp.vendor, ' '),
                GROUP_CONCAT(cp.product, ' ')
            FROM cves c
            LEFT JOIN cve_cpes cc ON c.id = cc.cve_id
            LEFT JOIN cpes cp ON cc.cpe_id = cp.id
            GROUP BY c.id
        """)
        conn.commit()
