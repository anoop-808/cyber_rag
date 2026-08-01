# TASK_010.md

# Phase 6B – Metadata Filtering Engine

## Status

Planned

---

# Objective

Implement a metadata filtering engine that refines retrieval results using structured CVE metadata.

This task enables CyberRAG to narrow search results based on user-specified constraints while preserving compatibility with the existing retrieval pipeline.

---

# Background

TASK_009 produces a high-quality ranked list of CVE documents.

However, analysts frequently need to limit results using structured attributes such as:

- Severity
- Vendor
- Product
- CWE
- Publication Year
- CVSS Score

Metadata filtering allows CyberRAG to satisfy these requirements before documents are returned to downstream components.

---

# Problem Statement

Keyword and semantic retrieval alone cannot satisfy highly constrained cybersecurity queries.

CyberRAG shall support structured filtering using document metadata.

---

# Scope

This task includes:

- Metadata extraction
- Structured filtering
- Multiple filter support
- Filter validation
- Filtered Top-K results

---

# Non Goals

This task SHALL NOT include:

- BM25 retrieval
- Vector retrieval
- Hybrid retrieval
- Re-ranking
- LLM answer generation
- Query rewriting
- API redesign
- UI changes

---

# Deliverables

## Metadata Filtering Engine

Implement a filtering module capable of narrowing retrieval results using structured metadata.

---

## Supported Filters

Support filtering by:

- CVSS Score
- Severity
- Vendor
- Product
- CWE
- Publication Year

Additional filters may be introduced in future phases.

---

## Multiple Filters

Support combining multiple filters simultaneously.

Example:

```text
Severity = Critical
Vendor = Microsoft
Year = 2024
```

Only documents satisfying every supplied filter should be returned.

---

## Filter Validation

Validate all filter inputs.

Reject unsupported or malformed filter values with meaningful exceptions.

---

# Folder Changes

New file:

```
app/retrieval/filters.py
```

---

# File Responsibilities

## filters.py

Responsible for:

- Applying metadata filters
- Validating filter values
- Returning filtered documents

No retrieval logic.

No ranking logic.

No LLM processing.

---

# Public Interface

Expose a stable API similar to:

```python
apply_filters(
    results,
    filters
)
```

Implementation details remain flexible.

---

# Input

Accept the ranked results produced by TASK_009.

---

# Output

Return filtered documents while preserving the existing CyberRAG document schema.

No schema modifications.

---

# Logging

Log:

- Filter execution
- Number of filters applied
- Input document count
- Output document count

Do not log document contents.

---

# Error Handling

Gracefully handle:

- Empty result list
- Unsupported filters
- Invalid filter values
- Missing metadata
- Empty filtered output

Return meaningful exceptions where appropriate.

---

# Performance Requirements

Filtering should execute efficiently over the ranked result set.

Avoid unnecessary iterations.

---

# Tests

Create unit tests covering:

- Single filter
- Multiple filters
- Invalid filter values
- Unsupported filters
- Empty result list
- No matching documents
- Metadata validation

---

# Acceptance Criteria

The task is complete when:

- Metadata filtering functions correctly.
- Multiple filters work together.
- Invalid filters are handled safely.
- Existing retrieval functionality remains unaffected.
- Unit tests pass.
- Existing tests continue to pass.

---

# Constraints

Do not modify:

- BM25 retrieval
- Hybrid retrieval
- Re-ranking
- Embedding pipeline
- Vector store
- Database schema
- API routes

Keep implementation isolated to metadata filtering.

---

# Out of Scope

The following belong to later tasks:

- Natural language filter extraction
- Query rewriting
- LLM reasoning
- Answer generation

---

# Definition of Done

- Metadata filtering implemented.
- Multiple filters supported.
- Validation completed.
- Unit tests passing.
- Ready for TASK_011.

---

# Dependencies

Requires:

- TASK_009 completed.

Produces:

A metadata-aware retrieval engine ready for integration into the unified CyberRAG retrieval pipeline.
