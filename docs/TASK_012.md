# TASK_012.md

# Phase 7 – Context Builder

## Status

Planned

---

# Objective

Implement the Context Builder for CyberRAG.

The Context Builder transforms the retrieved CVE documents into a clean, deterministic context block suitable for LLM consumption.

This task prepares the evidence that will later be provided to the language model.

This task is strictly backend-only.

---

# Background

TASK_011 introduced the Unified Retrieval Pipeline.

The retrieval pipeline now returns the most relevant CVE documents.

Large Language Models perform best when given structured, concise, and relevant context rather than raw database records.

The Context Builder is responsible for converting retrieval results into that format.

---

# Scope

Implement:

- Context Builder
- Context formatting
- Document ordering
- Context size limiting
- Metadata preservation
- Citation preparation

Do NOT implement:

- Prompt engineering
- LLM calls
- Answer generation
- Streaming
- Frontend changes
- API changes

---

# Functional Requirements

## Input

Accept the retrieved documents returned by the Unified Retrieval Pipeline.

Example:

```python
retrieve(query)
```

---

## Output

Produce a deterministic context block.

Example:

```text
[CVE-2024-1234]

Description:
...

Severity:
Critical

CVSS:
9.8

Published:
2024

------------------

[CVE-2024-5678]

...
```

---

## Included Fields

Each context entry should include:

- CVE ID
- Description
- Severity
- CVSS Score
- Published Date
- CWE (if available)

Do not include unnecessary fields.

---

## Ordering

Preserve the ranking order returned by the retrieval pipeline.

Do not reorder documents.

---

## Context Limits

Support configurable:

- Maximum documents
- Maximum characters
- Maximum context size

Stop cleanly when limits are reached.

Do not truncate individual metadata fields.

---

## Formatting

The generated context should:

- be deterministic
- be human-readable
- be LLM-friendly
- use consistent spacing
- clearly separate documents

---

## Metadata Preservation

Preserve all metadata required for future source attribution.

The Context Builder must not discard information needed for citations.

---

## Folder Changes

New file:

```
app/rag/context_builder.py
```

---

# Public Interface

Expose a stable API similar to:

```python
build_context(
    retrieved_documents
)
```

---

# Logging

Log:

- Number of retrieved documents
- Number of documents included
- Final context size

Do not log document contents.

---

# Error Handling

Gracefully handle:

- Empty retrieval results
- Missing metadata
- Invalid document format
- Context size exceeded

Return meaningful exceptions where appropriate.

---

# Performance Requirements

- Avoid unnecessary string copying.
- Preserve retrieval order.
- Build context efficiently.

---

# Tests

Create unit tests covering:

- Empty input
- Single document
- Multiple documents
- Missing metadata
- Context size limiting
- Deterministic formatting
- Ordering preservation

---

# Acceptance Criteria

The task is complete when:

✓ Context Builder implemented.

✓ Retrieval order preserved.

✓ Context formatting deterministic.

✓ Context size limits respected.

✓ Existing retrieval pipeline unaffected.

✓ Existing backend tests continue to pass.

✓ New tests pass.

---

# Constraints

Do not modify:

- Retrieval pipeline
- Hybrid retrieval
- Reranker
- Metadata filtering
- Database schema
- API routes
- Frontend

Only implement the Context Builder.

---

# Out of Scope

The following belong to later tasks:

- Prompt construction
- LLM inference
- Response generation
- Streaming
- Conversation memory

---

# Definition of Done

- Context Builder implemented.
- Unit tests passing.
- Existing functionality preserved.
- Ready for TASK_013.

---

# Dependencies

Requires:

- TASK_011 completed.

Produces:

A deterministic context block ready for Prompt Builder integration.
