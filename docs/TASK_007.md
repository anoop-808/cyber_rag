# TASK_007.md

# TASK 007: Embedding Pipeline & Vector Store Foundation

## Objective

Implement the embedding generation pipeline and vector store foundation for CyberRAG. This phase prepares the application for semantic retrieval by generating embeddings for the CVE database and storing them in a searchable vector index.

This task is **strictly backend-only**.

The frontend, API responses, and user interface must remain unchanged.

---

# Background

The current CyberRAG search relies entirely on SQLite Full-Text Search (FTS).

While fast, keyword search cannot understand semantic meaning.

Example:

Query:

```
Remote code execution vulnerabilities in OpenSSL
```

may fail to retrieve relevant CVEs if those exact keywords are absent.

The next phase will introduce semantic retrieval.

Before that can happen, every CVE must be converted into vector embeddings and indexed.

This task builds only that foundation.

---

# Scope

Implement:

- Embedding generation pipeline
- Vector store initialization
- Embedding persistence
- Index creation
- Configuration
- Documentation

Do NOT implement:

- Semantic search
- LLM integration
- RAG
- Prompt engineering
- UI changes
- API changes
- New endpoints

---

# Functional Requirements

## 1. Embedding Model

Select a sentence-transformer embedding model suitable for cybersecurity text.

The model should:

- run locally
- support CPU inference
- produce fixed-length embeddings
- work offline after download

Model choice should be configurable.

---

## 2. Embedding Pipeline

Implement a reusable pipeline that:

Loads all CVEs from SQLite

↓

Extracts relevant searchable text

↓

Generates embeddings

↓

Stores embeddings

The pipeline must be executable independently.

---

## 3. Searchable Content

Each embedding should include meaningful CVE context.

At minimum:

- CVE ID
- Description

Additional metadata may be included if appropriate.

---

## 4. Vector Store

Create the project's first vector database.

Responsibilities:

- initialize storage
- save embeddings
- load embeddings
- support nearest-neighbor search in future phases

This phase only requires storage.

Searching will be implemented later.

---

## 5. Configuration

Configuration values should be centralized.

Include:

- embedding model name
- vector storage location
- embedding dimension (if needed)

Avoid hard-coded values.

---

## 6. Project Structure

Introduce only the files necessary for embedding generation.

Example structure:

```
app/
    retrieval/
        embeddings.py
        vectorstore.py
```

Do not reorganize unrelated modules.

---

## 7. Documentation

Document:

- how embeddings are generated
- how to rebuild the vector index
- where embeddings are stored

---

# Acceptance Criteria

The following must be true:

✓ Embedding model loads successfully

✓ All CVEs are processed

✓ Embeddings are generated

✓ Embeddings are stored

✓ Vector store persists correctly

✓ Rebuilding the index works

✓ Existing backend tests continue to pass

✓ Existing frontend remains unaffected

✓ No API endpoints change

---

# Out of Scope

This task must NOT include:

- Natural language search
- Similarity search
- LLM integration
- AI-generated answers
- Prompt templates
- Chat interface
- React modifications
- Authentication
- Filters
- Pagination
- Database schema redesign

---

# Constraints

- Keep implementation minimal.
- Reuse the existing project architecture.
- Do not modify unrelated modules.
- Preserve existing functionality.
- Avoid premature optimization.
- No placeholder implementations.
- No mock embeddings.

---

# Deliverables

- Embedding generation pipeline
- Vector store implementation
- Configuration updates
- Documentation
- Passing backend tests

---

# Definition of Done

The task is complete when:

- embeddings can be generated for the complete CVE dataset
- embeddings are stored successfully
- the project builds without errors
- all existing tests pass
- no existing functionality regresses

Semantic retrieval will be implemented in the next task.
