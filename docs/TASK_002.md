# TASK 002 - SQLite FTS5 Search Engine

## Objective

Implement a fast offline keyword search system using SQLite FTS5.

---

## Scope

Implement:

- FTS5 virtual table
- Index builder
- Search service
- BM25 ranking
- Keyword search API

Support filters:

- Severity
- Vendor
- Product
- CWE

---

## Out of Scope

Do NOT implement:

- Gemini
- Ollama
- ChromaDB
- Semantic search
- Frontend

---

## Requirements

- FastAPI endpoint
- Parameter validation
- SQL parameterization
- Unit tests
- Logging

---

## Definition of Done

- Search returns ranked CVEs
- Filters work
- Tests pass
- Documentation updated
