"""Tests for the standalone ChromaDB embedding build script."""

from unittest.mock import Mock

import pytest

import scripts.build_embeddings as build_embeddings


def test_build_embeddings_upserts_sqlite_rows(monkeypatch):
    """The build step should encode SQLite CVEs and upsert stable IDs."""
    rows = [
        {
            "id": "CVE-2024-0001",
            "description": "Buffer overflow in example service.",
            "published": "2024-01-01",
            "modified": "2024-01-02",
            "severity": "HIGH",
            "cvss_score": 8.8,
            "cwe_id": "CWE-120",
        }
    ]
    model = Mock()
    model.encode.return_value.tolist.return_value = [[0.1, 0.2]]
    collection = Mock()

    monkeypatch.setattr(build_embeddings, "iter_cves", Mock(return_value=rows))
    monkeypatch.setattr(build_embeddings, "get_embedding_model", Mock(return_value=model))
    monkeypatch.setattr(build_embeddings, "get_vector_store", Mock(return_value=collection))

    indexed_count = build_embeddings.build_embeddings(batch_size=100)

    assert indexed_count == 1
    collection.upsert.assert_called_once_with(
        ids=["CVE-2024-0001"],
        documents=["Buffer overflow in example service."],
        embeddings=[[0.1, 0.2]],
        metadatas=[
            {
                "published": "2024-01-01",
                "last_modified": "2024-01-02",
                "severity": "HIGH",
                "cvss_score": 8.8,
                "cwe_id": "CWE-120",
            }
        ],
    )


def test_build_embeddings_requires_sqlite_import(monkeypatch):
    """The build step should fail clearly when SQLite is empty."""
    monkeypatch.setattr(build_embeddings, "iter_cves", Mock(return_value=[]))

    with pytest.raises(RuntimeError, match="Run scripts.import_nvd first"):
        build_embeddings.build_embeddings()

import sqlite3

@pytest.fixture
def mock_db_connection():
    """Create an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE cves (
            id TEXT PRIMARY KEY,
            description TEXT,
            published TEXT,
            modified TEXT,
            severity TEXT,
            cvss_score REAL,
            cwe_id TEXT
        )
    ''')
    conn.commit()
    yield conn
    conn.close()

def test_iter_cves_subset_filter(mock_db_connection):
    """Ensure iter_cves filters for CRITICAL/HIGH severity and published >= 2026."""
    # Insert test data
    cursor = mock_db_connection.cursor()
    cursor.execute('''
        INSERT INTO cves (id, description, published, severity, cvss_score) VALUES
        ('CVE-2026-0001', 'Desc', '2026-01-02', 'CRITICAL', 9.8),
        ('CVE-2026-0002', 'Desc', '2026-02-01', 'HIGH', 7.5),
        ('CVE-2025-0001', 'Desc', '2025-12-31', 'CRITICAL', 9.8),
        ('CVE-2026-0003', 'Desc', '2026-03-01', 'MEDIUM', 5.0)
    ''')
    
    with pytest.MonkeyPatch().context() as m:
        mock_ctx = Mock()
        mock_ctx.__enter__ = Mock(return_value=mock_db_connection)
        mock_ctx.__exit__ = Mock(return_value=None)
        m.setattr(build_embeddings, "get_db_connection", Mock(return_value=mock_ctx))
        
        results = build_embeddings.iter_cves()
        
    assert len(results) == 2
    assert results[0]["id"] == "CVE-2026-0001"
    assert results[1]["id"] == "CVE-2026-0002"

def test_build_embeddings_idempotency(monkeypatch):
    """Ensure running build_embeddings twice doesn't duplicate vectors in ChromaDB."""
    rows = [
        {
            "id": "CVE-2025-0001",
            "description": "Buffer overflow",
            "published": "2025-01-01",
            "modified": None,
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "cwe_id": None,
        }
    ]
    model = Mock()
    model.encode.return_value.tolist.return_value = [[0.1, 0.2]]
    
    # Simple mock collection that tracks upserts
    class MockCollection:
        def __init__(self):
            self.data = {}
        def upsert(self, ids, documents, embeddings, metadatas):
            for i, cve_id in enumerate(ids):
                self.data[cve_id] = (documents[i], embeddings[i], metadatas[i])
        def count(self):
            return len(self.data)
            
    collection = MockCollection()
    
    monkeypatch.setattr(build_embeddings, "iter_cves", Mock(return_value=rows))
    monkeypatch.setattr(build_embeddings, "get_embedding_model", Mock(return_value=model))
    monkeypatch.setattr(build_embeddings, "get_vector_store", Mock(return_value=collection))
    
    # Run first time
    build_embeddings.build_embeddings(batch_size=100)
    assert collection.count() == 1
    
    # Run second time
    build_embeddings.build_embeddings(batch_size=100)
    
    # The count should remain 1, proving idempotency
    assert collection.count() == 1
