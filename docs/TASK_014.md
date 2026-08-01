# TASK_014.md

# Phase 7 – LLM Interface

## Status

Planned

---

# Objective

Implement the LLM Interface for CyberRAG.

The LLM Interface is responsible for communicating with a configured language model provider while remaining independent from retrieval, prompt construction, and response formatting.

This task introduces AI inference into CyberRAG.

This task is strictly backend-only.

---

# Background

TASK_013 introduced the Prompt Builder.

The Prompt Builder creates deterministic prompts suitable for language model inference.

The LLM Interface executes those prompts against the configured provider and returns the raw response.

---

# Scope

Implement:

- LLM client
- Provider abstraction
- Request execution
- Response handling
- Timeout handling
- Retry mechanism
- Configuration support

Do NOT implement:

- Response formatting
- Conversation memory
- Streaming responses
- API changes
- Frontend changes

---

# Functional Requirements

## Input

Accept:

- System Prompt
- User Prompt

Example:

```python
generate_response(
    system_prompt,
    user_prompt
)
```

---

## Output

Return the raw language model response.

Do not perform formatting.

Do not modify model output.

---

## Supported Providers

The interface should support configurable providers.

Initially support one provider while keeping the architecture extensible.

Examples include:

- Ollama
- OpenRouter

Future providers should require minimal code changes.

---

## Configuration

Configuration should include:

- Provider
- Model name
- Base URL
- Temperature
- Maximum tokens
- Timeout

Avoid hard-coded values.

---

## Retry Policy

Support configurable retries for transient failures.

Do not retry invalid requests.

---

## Timeout Handling

Requests should terminate cleanly after the configured timeout.

Return meaningful exceptions.

---

## Logging

Log:

- Request start
- Request completion
- Model used
- Response time

Do not log prompt contents.

---

## Error Handling

Gracefully handle:

- Connection failures
- Timeouts
- Invalid configuration
- Empty responses
- Provider errors

Return meaningful exceptions.

---

# Folder Changes

New file:

```
app/llm/client.py
```

Configuration updates may be added to:

```
app/core/config.py
```

---

# Public Interface

Expose a stable API similar to:

```python
generate_response(
    system_prompt: str,
    user_prompt: str
)
```

---

# Performance Requirements

- Reuse HTTP clients where appropriate.
- Avoid unnecessary allocations.
- Keep latency low.
- Support future asynchronous execution.

---

# Tests

Create unit tests covering:

- Successful inference
- Timeout handling
- Retry logic
- Invalid configuration
- Empty response
- Provider failures

Mock provider responses where appropriate.

---

# Acceptance Criteria

The task is complete when:

✓ LLM Interface implemented.

✓ Provider configuration supported.

✓ Retry policy implemented.

✓ Timeout handling implemented.

✓ Existing retrieval functionality unaffected.

✓ Existing backend tests continue to pass.

✓ New tests pass.

---

# Constraints

Do not modify:

- Retrieval pipeline
- Context Builder
- Prompt Builder
- Database schema
- API routes
- Frontend

Only implement the LLM Interface.

---

# Out of Scope

The following belong to later tasks:

- Response formatting
- Streaming
- Conversation memory
- Multi-turn chat
- UI integration

---

# Definition of Done

- LLM Interface implemented.
- Unit tests passing.
- Existing functionality preserved.
- Ready for TASK_015.

---

# Dependencies

Requires:

- TASK_013 completed.

Produces:

A configurable language model interface capable of generating raw responses from prompts.
