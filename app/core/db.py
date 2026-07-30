"""SQLite database connection and schema management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

DB_PATH = Path("storage/database.sqlite")


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a database connection and ensure it is closed afterward.

    Yields
    ------
    sqlite3.Connection
        The active SQLite database connection.
    """
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
    schema_path = Path("app/core/schema.sql")
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    with get_db_connection() as conn:
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
