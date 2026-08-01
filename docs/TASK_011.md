# TASK_011.md

# Phase 6B – Unified Retrieval Pipeline

## Status

Planned

---

# Objective

Integrate all retrieval components into a single retrieval pipeline that serves as the sole entry point for CyberRAG document retrieval.

This pipeline shall orchestrate lexical retrieval, semantic retrieval, hybrid ranking, re-ranking, and metadata filtering while exposing a clean public interface for downstream components.

---

# Background

Previous tasks implemented individual retrieval components:

- TASK_007 — Embedding Pipeline & Vector Store Foundation
- TASK_008 — Hybrid Retrieval Engine
- TASK_009 — Result Re-ranking Engine
- TASK_010 — Metadata Filtering Engine

These components currently exist independently.

CyberRAG now requires a unified orchestration layer so future phases can retrieve documents through a single interface.

---

# Problem Statement

Future RAG generation should not need to understand:

- BM25 retrieval
- Vector retrieval
- Score normalization
- Re-ranking
- Metadata filtering

Instead, it should call one retrieval function.

---

# Scope

Implement:

- Unified retrieval pipeline
- Retrieval orchestration
- Configuration integration
- Logging
- Error handling

---

# Non Goals

This task SHALL NOT include:

- LLM integration
- Prompt construction
- Answer generation
- Streaming responses
- UI changes
- API redesign
- Authentication

---

# Deliverables

## Unified Retrieval Pipeline

Create a single retrieval module responsible for executing the complete retrieval workflow.

Workflow:

User Query

↓

Hybrid Retrieval

↓

Result Re-ranking

↓

Metadata Filtering

↓

Top-K Results

---

## Public Interface

Expose a single API similar to:

```python
retrieve(
    query: str,
    top_k: int = 10,
    filters: dict | None = None
)
```

Future phases should use only this interface.

---

## Configuration

Centralize retrieval configuration including:

- Default Top-K
- BM25 weight
- Vector weight
- Retrieval limits

Avoid hard-coded values.

---

## Logging

Log:

- Query received
- Hybrid retrieval execution
- Re-ranking execution
- Metadata filtering execution
- Final result count
- Pipeline completion

Do not log document contents.

---

## Error Handling

Gracefully handle:

- Empty query
- Missing indexes
- Retrieval failures
- Empty result sets
- Invalid filters

Failures in one component should generate meaningful exceptions.

---

# Folder Changes

New file:

```
app/retrieval/pipeline.py
```

If a pipeline file already exists, extend it instead of creating a duplicate.

Do not reorganize unrelated modules.

---

# File Responsibilities

The unified pipeline should coordinate existing retrieval components only.

It should NOT implement:

- BM25
- Vector search
- Re-ranking
- Metadata filtering

Those remain isolated within their respective modules.

---

# Performance Requirements

- Avoid duplicate retrieval calls.
- Reuse initialized indexes.
- Keep retrieval latency low.
- Minimize unnecessary allocations.

---

# Tests

Create tests covering:

- End-to-end retrieval pipeline
- Empty query
- Empty results
- Retrieval failures
- Metadata filtering integration
- Stable output
- Top-K behavior

---

# Acceptance Criteria

The task is complete when:

✓ A single retrieval interface exists.

✓ Hybrid retrieval executes correctly.

✓ Re-ranking executes correctly.

✓ Metadata filtering executes correctly.

✓ Existing functionality remains unaffected.

✓ Existing backend tests continue to pass.

✓ New pipeline tests pass.

---

# Constraints

Do not modify:

- API endpoints
- Frontend
- SQLite schema
- Embedding generation
- BM25 implementation
- Hybrid retrieval logic
- Re-ranking implementation
- Metadata filtering implementation

Only integrate them.

---

# Out of Scope

The following belong to Phase 7:

- Prompt engineering
- RAG generation
- LLM orchestration
- Streaming responses
- AI explanations

---

# Definition of Done

- Unified retrieval pipeline implemented.
- All retrieval components integrated.
- Clean public API available.
- Unit tests passing.
- Existing functionality preserved.

---

# Dependencies

Requires:

- TASK_007 completed.
- TASK_008 completed.
- TASK_009 completed.
- TASK_010 completed.

Produces:

A production-ready retrieval layer that becomes the foundation for Phase 7 (RAG Answer Generation).
