# TASK_017.md

# Phase 8 – API Request & Response Models

## Status

Planned

---

# Objective

Implement the API request and response models for CyberRAG.

This task defines the data contracts exchanged between clients and the backend using Pydantic models.

This task is strictly backend-only.

---

# Background

TASK_016 completed the end-to-end RAG pipeline.

The pipeline now accepts a query and produces a structured answer.

Before exposing this functionality through FastAPI endpoints, stable request and response schemas must be defined.

These models become the public API contract.

---

# Scope

Implement:

- Request models
- Response models
- Validation rules
- Serialization support
- API documentation metadata

Do NOT implement:

- API routes
- Endpoint logic
- Authentication
- Frontend
- Database changes
- RAG pipeline changes

---

# Functional Requirements

## Request Model

Create a request model similar to:

```python
AskRequest
```

Fields:

- query (required)
- filters (optional)

Example:

```json
{
  "query": "How does CVE-2024-1234 work?",
  "filters": {
    "severity": "CRITICAL"
  }
}
```

---

## Response Model

Create a response model similar to:

```python
AskResponse
```

Fields:

- answer
- sources
- metadata
- confidence

Example:

```json
{
  "answer": "...",
  "sources": [
    "CVE-2024-1234"
  ],
  "metadata": [
    {
      "id": "CVE-2024-1234",
      "severity": "CRITICAL",
      "cvss": 9.8
    }
  ],
  "confidence": null
}
```

---

## Search Models

Also define models for search-only operations.

Example:

```python
SearchRequest
SearchResponse
```

SearchResponse should contain retrieved documents without invoking the LLM.

---

## Validation

Validate:

- Empty query
- Missing required fields
- Invalid filter types
- Invalid metadata types

Reject malformed requests with meaningful validation errors.

---

## Serialization

Models must serialize cleanly using FastAPI/Pydantic defaults.

Support JSON encoding without custom serializers.

---

## Documentation

Provide:

- Field descriptions
- Examples
- Type hints

The models should automatically generate clean OpenAPI documentation.

---

# Folder Changes

Create:

```
app/api/models.py
```

---

# Public Interface

Expose:

```python
AskRequest

AskResponse

SearchRequest

SearchResponse
```

---

# Logging

No logging required.

These models should remain declarative.

---

# Error Handling

Rely on Pydantic validation.

Do not implement custom exception handlers.

---

# Performance Requirements

- Lightweight
- Immutable where appropriate
- Minimal validation overhead

---

# Tests

Create unit tests covering:

- Valid requests
- Invalid requests
- Empty query
- Serialization
- JSON encoding
- Validation errors

---

# Acceptance Criteria

The task is complete when:

✓ Request models implemented.

✓ Response models implemented.

✓ Validation works correctly.

✓ Serialization verified.

✓ Existing tests continue to pass.

✓ New tests pass.

---

# Constraints

Do not modify:

- Retrieval pipeline
- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter
- RAG Pipeline
- API routes
- Frontend

Only implement the API models.

---

# Out of Scope

The following belong to later tasks:

- /ask endpoint
- /search endpoint
- Dependency injection
- FastAPI wiring
- Authentication

---

# Definition of Done

- API models implemented.
- Unit tests passing.
- Existing functionality preserved.
- Ready for TASK_018.

---

# Dependencies

Requires:

- TASK_016 completed.

Produces:

Stable request and response schemas for all future API endpoints.
