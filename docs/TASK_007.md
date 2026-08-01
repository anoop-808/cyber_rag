# TASK_007.md

# Phase 6B – BM25 Retrieval Engine

## Status

Planned

---

# Objective

Implement a lexical retrieval engine using the BM25 ranking algorithm to enable keyword-based searching over the CyberRAG CVE database.

This task establishes the first retrieval component of the Hybrid Retrieval system that will later combine lexical retrieval with semantic vector search.

---

# Background

Phase 6A introduced semantic retrieval through SentenceTransformer embeddings and ChromaDB.

While semantic search performs well for conceptual similarity, it can miss exact technical terms such as:

- CVE IDs
- Product names
- Vendor names
- Attack technique names
- Version numbers
- Error codes

Lexical retrieval complements semantic retrieval by ranking documents according to keyword relevance.

---

# Problem Statement

CyberRAG currently relies only on semantic embeddings.

Users searching for exact terminology should receive highly relevant matches even when semantic similarity is weak.

A BM25 retrieval engine shall provide this capability.

---

# Scope

This task includes:

- Build BM25 index
- Load CVE documents
- Tokenize searchable fields
- Execute BM25 ranking
- Return Top-K results

---

# Non Goals

This task SHALL NOT include:

- Hybrid retrieval
- Score fusion
- Metadata filtering
- Reranking
- LLM integration
- API redesign
- UI changes

Those belong to later tasks.

---

# Deliverables

## BM25 Index

Create an index over the processed CVE dataset.

Searchable fields:

- CVE ID
- Title
- Description
- CWE
- Vendor
- Product

---

## BM25 Search

Implement keyword search using BM25.

Input:

```text
remote code execution
```

Output:

```text
Top K ranked CVEs
```

---

## Configurable Parameters

Support configurable:

```python
top_k

```

Future tuning parameters may be added later.

---

# Folder Changes

New file:

```
app/retrieval/bm25.py
```

No additional folders.

---

# File Responsibilities

## bm25.py

Responsible for:

- Loading searchable corpus
- Building BM25 index
- Performing keyword search
- Returning ranked documents

No vector search logic.

---

# Public Interface

The module should expose a clean API similar to:

```python
search_bm25(
    query: str,
    top_k: int = 10
)
```

Implementation details are left to the developer provided the interface remains stable.

---

# Data Source

Use the existing processed CVE dataset created during previous phases.

Do NOT duplicate datasets.

Do NOT create a second database.

---

# Result Format

Results should remain compatible with the retrieval pipeline.

Each returned document should preserve existing metadata already used by CyberRAG.

No schema changes.

---

# Logging

Log:

- Index creation
- Corpus size
- Query execution
- Returned result count

Do not log full document contents.

---

# Error Handling

Gracefully handle:

- Empty query
- Missing dataset
- Empty corpus
- Invalid top_k

Return meaningful exceptions.

---

# Performance Requirements

Index creation should occur once.

Repeated searches should reuse the existing index.

Avoid rebuilding the BM25 index for every query.

---

# Tests

Create unit tests covering:

- Index creation
- Empty corpus
- Empty query
- Single keyword search
- Multi-keyword search
- Top-K behavior
- Deterministic ranking

---

# Acceptance Criteria

The task is complete when:

- BM25 index builds successfully.
- Keyword search returns ranked CVEs.
- Existing retrieval code remains functional.
- Existing semantic search is unaffected.
- All new tests pass.
- Existing tests continue to pass.

---

# Constraints

Follow existing CyberRAG architecture.

Do not modify:

- Embedding pipeline
- Vector store
- API routes
- Database schema

Keep changes isolated to lexical retrieval.

---

# Out of Scope

The following belong to later tasks:

- Hybrid search
- Score fusion
- Metadata filters
- Re-ranking
- RAG generation

---

# Definition of Done

- BM25 retrieval implemented.
- Code documented.
- Unit tests passing.
- Existing functionality preserved.
- Ready for TASK_008.

---

# Dependencies

Requires:

- Phase 6A completed.
- ChromaDB already operational.
- Existing processed CVE dataset.

Produces:

A standalone BM25 retrieval engine to be consumed by TASK_008 Hybrid Retrieval.
