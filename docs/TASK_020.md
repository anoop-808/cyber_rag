# TASK_020.md

# Phase 8 – Dependency Injection & Application Wiring

## Status

Planned

---

# Objective

Implement dependency injection and application wiring for CyberRAG.

This task centralizes the creation and lifecycle management of shared services used throughout the application.

This task is strictly backend-only.

---

# Background

Previous tasks introduced:

- API Models
- Ask Endpoint
- Search Endpoint
- Retrieval Pipeline
- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter

Currently these components may be instantiated directly.

Dependency Injection ensures services are initialized once and reused consistently across requests.

---

# Scope

Implement:

- Dependency providers
- Shared service initialization
- Application lifecycle management
- FastAPI dependency injection
- Configuration reuse

Do NOT implement:

- Authentication
- Authorization
- Rate limiting
- Frontend
- Database migrations
- Business logic changes

---

# Functional Requirements

## Dependency Providers

Create dependency providers for:

- Retrieval Pipeline
- LLM Client
- Vector Store
- Configuration

Each dependency should be reusable across requests.

---

## Application Lifecycle

Use FastAPI lifespan events or equivalent startup/shutdown mechanisms.

Initialize long-lived resources only once.

Release resources cleanly during shutdown.

---

## Endpoint Integration

Update existing API endpoints to receive services through dependency injection.

Avoid direct object creation inside route handlers.

---

## Configuration

Configuration should be loaded once and shared across all components.

Avoid duplicate configuration parsing.

---

## Folder Changes

Create:

```
app/api/dependencies.py
```

Update existing API initialization files only if required.

---

# Public Interface

Expose dependency provider functions similar to:

```python
get_retrieval_pipeline()

get_llm_client()

get_vector_store()

get_settings()
```

---

# Logging

Log:

- Application startup
- Resource initialization
- Resource shutdown

Do not log:

- API keys
- Secrets
- User queries

---

# Error Handling

Gracefully handle:

- Failed initialization
- Missing configuration
- Resource creation failures

Fail fast during startup when critical dependencies cannot be initialized.

---

# Performance Requirements

- Initialize expensive resources only once.
- Reuse dependencies across requests.
- Avoid duplicate model loading.
- Minimize startup overhead.

---

# Tests

Create tests covering:

- Dependency creation
- Dependency reuse
- Startup lifecycle
- Shutdown lifecycle
- Configuration loading
- Failure during initialization

---

# Acceptance Criteria

The task is complete when:

✓ Dependency providers implemented.

✓ Shared services initialized correctly.

✓ Existing endpoints use dependency injection.

✓ Existing functionality preserved.

✓ Existing tests continue to pass.

✓ New tests pass.

---

# Constraints

Do not modify:

- Retrieval logic
- Context Builder
- Prompt Builder
- LLM Interface
- Response Formatter
- RAG Pipeline algorithms

Only improve application wiring.

---

# Out of Scope

The following belong to later tasks:

- Authentication
- Authorization
- Rate limiting
- Metrics
- Monitoring
- Distributed deployment

---

# Definition of Done

- Dependency injection implemented.
- Startup and shutdown lifecycle managed.
- Shared services reused.
- Existing functionality preserved.
- Ready for TASK_021.

---

# Dependencies

Requires:

- TASK_018 completed.
- TASK_019 completed.

Produces:

A production-ready dependency injection layer for the CyberRAG API.
