# TASK_019.md

# Phase 8 – Search API Endpoint

## Status

Planned

---

# Objective

Implement the Search API endpoint for CyberRAG.

This endpoint exposes the retrieval pipeline without invoking the language model.

It enables clients to retrieve relevant CVE documents directly for search, inspection, and debugging.

This task is strictly backend-only.

---

# Background

TASK_018 introduced the Ask endpoint, which executes the complete RAG pipeline.

Many clients require retrieval results without answer generation.

The Search endpoint provides direct access to the retrieval layer.

---

# Scope

Implement:

- POST /search endpoint
- Request validation
- Retrieval pipeline invocation
- Response serialization
- HTTP error handling

Do NOT implement:

- LLM inference
- Prompt Builder
- Context Builder
- Response Formatter
- Authentication
- Streaming
- Frontend

---

# Functional Requirements

## Endpoint

Create:

```
POST /search
```

Accept:

```json
{
  "query": "openssl remote code execution",
  "filters": {
    "severity": "HIGH"
  }
}
```

Return:

```json
{
  "documents": [
    {
      "id": "CVE-2024-1234",
      "description": "...",
      "metadata": {
        "severity": "HIGH",
        "cvss_score": 9.8
      }
    }
  ]
}
```

---

# Processing Flow

The endpoint should:

1. Validate request
2. Invoke the Retrieval Pipeline
3. Return retrieved documents

Do not invoke:

- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter

---

# Folder Changes

Update:

```
app/api/routes.py
```

Do not create duplicate routers.

---

# Public Interface

Expose:

```python
POST /search
```

using:

```python
SearchRequest

SearchResponse
```

---

# Validation

Reject:

- Empty query
- Invalid JSON
- Invalid filters
- Malformed request body

Return appropriate HTTP status codes.

---

# Error Handling

Gracefully handle:

- Validation failures
- Retrieval failures
- Internal exceptions

Do not expose stack traces.

---

# Logging

Log:

- Incoming search request
- Processing duration
- Number of retrieved documents
- Response status

Do not log:

- Query embeddings
- Internal scores
- Sensitive configuration

---

# Performance Requirements

- Reuse Retrieval Pipeline
- No duplicate retrieval
- Async-compatible implementation
- Low endpoint overhead

---

# Tests

Create endpoint tests covering:

- Successful search
- Empty query
- Invalid request
- Invalid filters
- Retrieval failure
- Response schema validation

---

# Acceptance Criteria

The task is complete when:

✓ POST /search implemented.

✓ Retrieval Pipeline reused.

✓ Response serialization works.

✓ Existing tests continue to pass.

✓ New endpoint tests pass.

---

# Constraints

Do not modify:

- Retrieval Pipeline
- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter
- RAG Pipeline

Only expose retrieval through FastAPI.

---

# Out of Scope

The following belong to later tasks:

- Authentication
- Pagination
- Sorting
- Rate limiting
- Streaming
- Frontend integration

---

# Definition of Done

- Search endpoint implemented.
- Endpoint tests passing.
- Existing functionality preserved.
- Ready for TASK_020.

---

# Dependencies

Requires:

- TASK_017 completed.

Produces:

A public retrieval API for CyberRAG without LLM inference.
