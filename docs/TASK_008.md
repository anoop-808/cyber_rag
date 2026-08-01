# TASK_008.md

# Phase 6B – Hybrid Retrieval Engine

## Status

Planned

---

# Objective

Implement a Hybrid Retrieval Engine that combines lexical retrieval (BM25) and semantic vector retrieval into a unified ranked result set.

This task builds directly on TASK_007 by integrating both retrieval strategies while keeping them independently maintainable.

---

# Background

CyberRAG currently supports semantic retrieval through SentenceTransformer embeddings and ChromaDB.

TASK_007 introduces BM25 lexical retrieval.

Each retrieval strategy has different strengths.

Semantic retrieval excels at conceptual similarity.

Lexical retrieval excels at exact terminology such as:

- CVE IDs
- Product names
- Vendor names
- Versions
- Error codes
- Technical keywords

Combining both provides significantly better retrieval quality.

---

# Problem Statement

Neither semantic retrieval nor lexical retrieval alone consistently returns the best results for cybersecurity queries.

CyberRAG shall combine both retrieval methods into a single retrieval engine.

---

# Scope

This task includes:

- Execute BM25 retrieval
- Execute vector retrieval
- Normalize retrieval scores
- Merge duplicate documents
- Produce a unified ranked result list

---

# Non Goals

This task SHALL NOT include:

- Score weighting optimization
- Metadata filtering
- LLM answer generation
- API redesign
- UI changes
- Prompt engineering

---

# Deliverables

## Hybrid Retriever

Implement a retrieval engine that queries:

- BM25
- Vector Search

for every user query.

---

## Duplicate Resolution

When both retrieval engines return the same document:

- Preserve one copy only.
- Combine ranking information.

No duplicate documents shall appear in the final output.

---

## Normalized Scores

Normalize scores from both retrieval engines before ranking.

Do not directly compare raw BM25 scores with cosine similarity scores.

---

## Configurable Parameters

Support configurable:

```python
top_k
bm25_weight
vector_weight
```

Default values should remain configurable through project configuration.

---

# Folder Changes

New file:

```
app/retrieval/hybrid.py
```

---

# File Responsibilities

## hybrid.py

Responsible for:

- Calling BM25 retrieval
- Calling vector retrieval
- Combining results
- Removing duplicates
- Returning ranked documents

No reranking logic.

No metadata filtering.

---

# Public Interface

Expose a stable API similar to:

```python
search_hybrid(
    query: str,
    top_k: int = 10
)
```

Implementation details remain flexible.

---

# Data Sources

Use:

- Existing BM25 index
- Existing Chroma vector store

Do not duplicate indexes.

---

# Result Format

Output should remain compatible with the existing retrieval pipeline.

Each result must preserve all existing metadata.

No schema changes.

---

# Logging

Log:

- BM25 result count
- Vector result count
- Duplicate count
- Final merged count

Do not log document contents.

---

# Error Handling

Gracefully handle:

- Empty query
- Missing BM25 index
- Missing vector index
- Empty result sets

The system should still return results if only one retrieval engine succeeds.

---

# Performance Requirements

BM25 and vector retrieval should execute independently.

Avoid rebuilding indexes.

Avoid unnecessary duplicate processing.

---

# Tests

Create unit tests covering:

- BM25 only results
- Vector only results
- Combined retrieval
- Duplicate removal
- Score normalization
- Top-K ranking
- Empty result handling

---

# Acceptance Criteria

The task is complete when:

- Both retrieval engines execute successfully.
- Results are merged correctly.
- Duplicate documents are removed.
- Final ranking is deterministic.
- Existing retrieval functionality remains unaffected.
- All tests pass.

---

# Constraints

Do not modify:

- BM25 implementation
- Embedding pipeline
- Vector store
- API routes
- Database schema

Keep implementation isolated to hybrid retrieval.

---

# Out of Scope

The following belong to later tasks:

- Score fusion optimization
- Re-ranking
- Metadata filtering
- RAG generation

---

# Definition of Done

- Hybrid retrieval implemented.
- Duplicate handling complete.
- Score normalization implemented.
- Unit tests passing.
- Ready for TASK_009.

---

# Dependencies

Requires:

- TASK_007 completed.
- Existing semantic retrieval.
- Existing vector store.

Produces:

A unified retrieval engine for CyberRAG that combines lexical and semantic search.
