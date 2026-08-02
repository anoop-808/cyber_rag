# TASK_018.md

# Phase 8 – Ask API Endpoint

## Status

Planned

---

# Objective

Implement the primary Ask API endpoint for CyberRAG.

This endpoint exposes the complete RAG pipeline through FastAPI, allowing clients to submit a natural language question and receive a grounded response.

This task is strictly backend-only.

---

# Background

TASK_017 introduced the API request and response models.

CyberRAG now contains:

- Unified Retrieval Pipeline
- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter
- RAG Pipeline

The Ask endpoint connects these components into a public HTTP API.

---

# Scope

Implement:

- POST /ask endpoint
- Request validation
- Response serialization
- Pipeline invocation
- HTTP error handling

Do NOT implement:

- Authentication
- Authorization
- Rate limiting
- Streaming
- Frontend
- Search endpoint
- Conversation history

---

# Functional Requirements

## Endpoint

Create:

```
POST /ask
```

Accept:

```json
{
  "query": "How does CVE-2024-1234 work?",
  "filters": {
    "severity": "CRITICAL"
  }
}
```

Return:

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

# Processing Flow

The endpoint should:

1. Validate request
2. Invoke the RAG Pipeline
3. Receive formatted response
4. Return JSON response

The endpoint must not implement business logic itself.

Business logic belongs to the RAG pipeline.

---

# Folder Changes

Create:

```
app/api/routes.py
```

If an API router already exists, extend it rather than creating duplicates.

---

# Public Interface

Expose:

```python
POST /ask
```

using:

```python
AskRequest

AskResponse
```

---

# Validation

Reject:

- Empty query
- Invalid JSON
- Invalid filters
- Invalid request body

Return appropriate HTTP status codes.

---

# Error Handling

Gracefully handle:

- Validation errors
- Pipeline failures
- LLM failures
- Unexpected exceptions

Return meaningful HTTP responses.

Do not expose stack traces.

---

# Logging

Log:

- Incoming request
- Processing duration
- Success/failure
- Response status

Do not log:

- API keys
- Prompt contents
- Full context
- Sensitive information

---

# Performance Requirements

- Minimal endpoint overhead
- Reuse existing pipeline
- No duplicate processing
- Async-compatible implementation

---

# Tests

Create endpoint tests covering:

- Successful request
- Empty query
- Invalid request body
- Validation failure
- Internal pipeline failure
- Response schema validation

---

# Acceptance Criteria

The task is complete when:

✓ POST /ask implemented.

✓ Request validation works.

✓ Response serialization works.

✓ Existing RAG pipeline reused.

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

Only expose them through FastAPI.

---

# Out of Scope

The following belong to later tasks:

- /search endpoint
- Authentication
- API versioning
- Rate limiting
- Streaming
- WebSocket support

---

# Definition of Done

- Ask endpoint implemented.
- Endpoint tests passing.
- Existing functionality preserved.
- Ready for TASK_019.

---

# Dependencies

Requires:

- TASK_017 completed.

Produces:

The first public API endpoint exposing CyberRAG's complete RAG pipeline.
