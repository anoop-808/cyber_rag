# TASK 001 - SQLite Database Layer & NVD Importer

## Objective

Implement the foundational data layer for CyberRAG.

This task focuses only on creating the SQLite database schema and importing NVD CVE data.

## Scope

Implement the following:

- SQLite connection module
- Database schema creation
- NVD JSON parser
- NVD importer
- Data validation
- Basic logging
- Unit tests

## Database Schema

### cves

Fields:

- id
- description
- published
- modified
- severity
- cvss_version
- cvss_score
- cvss_vector
- attack_vector
- attack_complexity
- privileges_required
- user_interaction
- scope
- confidentiality
- integrity
- availability
- cwe_id
- references (stored as JSON)

### cwes

- id
- name
- description

### cpes

- id
- uri
- vendor
- product
- version

### cve_cpes

- cve_id
- cpe_id

## Requirements

- Use Python standard library where possible.
- Use SQLite as the primary datastore.
- Handle malformed NVD entries gracefully.
- Use transactions for bulk imports.
- Log meaningful errors.
- Write clean, modular code.

## Out of Scope

Do NOT implement:

- FastAPI endpoints
- Frontend
- ChromaDB
- Embeddings
- Gemini
- Ollama
- Semantic search
- Explain feature

## Definition of Done

- Database schema created
- Importer successfully loads NVD JSON
- Tables populated correctly
- Unit tests pass
- Code follows AGENTS.md
