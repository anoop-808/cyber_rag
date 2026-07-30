# TASK 002 - SQLite Full Text Search (FTS5)

## Objective

Implement a fast offline keyword search engine using SQLite FTS5.

SQLite remains the source of truth.

## Scope

Implement:

- FTS5 virtual table
- Index creation
- Index refresh command
- Search service
- Search API

Support searching by:

- CVE ID
- Description
- Vendor
- Product
- Severity
- CWE

## API

Create:

GET /search

Query parameters:

- q
- severity
- vendor
- product
- cwe
- limit

Return JSON.

## Ranking

Use SQLite BM25 ranking.

Sort by relevance.

## Requirements

- Parameterized SQL
- Type hints
- Logging
- Unit tests
- Docstrings

## Out of Scope

Do NOT implement:

- ChromaDB
- Semantic search
- Gemini
- Ollama
- Frontend

## Definition of Done

- Search returns ranked CVEs
- Filters work
- Tests pass
- API documented
