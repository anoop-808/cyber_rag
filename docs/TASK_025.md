# TASK_025.md

# Phase 9 – AI Ask Interface

## Status

Planned

---

# Objective

Implement the AI Ask interface for CyberRAG.

This task provides a frontend interface for interacting with the CyberRAG Ask API, allowing users to submit cybersecurity questions and receive grounded AI-generated answers.

This task is frontend-only.

---

# Background

Previous tasks introduced:

- Frontend setup
- Search interface
- Search results

The backend now exposes:

POST /ask

which executes the complete RAG pipeline.

This task connects the frontend to that endpoint.

---

# Scope

Implement:

- Ask page
- Question input
- Submit button
- API integration
- Loading state
- Error handling
- Answer display
- Sources display
- Confidence display

Do NOT implement:

- Conversation history
- Chat memory
- Streaming responses
- Markdown rendering
- Authentication
- Citations popup

---

# Functional Requirements

## Ask Page

Create a page similar to:

```
/ask
```

---

## Input Area

Allow users to enter natural language questions.

Example:

```
How does CVE-2024-1234 work?
```

---

## Submit Button

Clicking Ask should call:

POST /ask

using:

```json
{
    "query": "...",
    "filters": {}
}
```

---

## Loading State

Disable the button while waiting.

Display:

```
Generating answer...
```

or a loading spinner.

---

## Success Response

Display:

Answer

```
Remote attackers can...
```

Sources

```
CVE-2024-1234

CVE-2024-5555
```

Confidence

```
Unknown
```

(if confidence is null)

---

## Error State

Gracefully display:

- Network errors
- Backend errors
- Validation errors

Do not expose stack traces.

---

## Empty State

Before asking:

```
Ask CyberRAG anything about CVEs.
```

---

## Multiple Questions

Allow users to submit multiple questions without refreshing the page.

Each submission replaces the previous answer.

Conversation history is not required.

---

# Folder Changes

Create or update:

```
frontend/src/pages/Ask.tsx

frontend/src/components/AskForm.tsx

frontend/src/components/AnswerCard.tsx
```

Reuse existing project structure.

---

# Public Interface

Expose:

```
/ask
```

---

# Performance Requirements

- Single API request per submission.
- Prevent duplicate submissions.
- Handle slow responses gracefully.

---

# Tests

Verify:

- Successful API request.
- Loading state.
- Error state.
- Empty state.
- Answer renders correctly.
- Sources render correctly.
- Confidence renders correctly.

---

# Acceptance Criteria

The task is complete when:

✓ Ask page implemented.

✓ Backend integration completed.

✓ AI answer displayed.

✓ Sources displayed.

✓ Confidence displayed.

✓ Existing frontend builds successfully.

---

# Constraints

Do not implement:

- Chat history
- Streaming
- Markdown rendering
- Authentication
- Conversation memory

Only implement the Ask interface.

---

# Out of Scope

Belongs to later tasks:

- CVE Detail View
- Responsive polish
- Chat history
- Streaming responses

---

# Definition of Done

- Ask interface completed.
- Connected to POST /ask.
- Frontend builds successfully.
- Ready for TASK_026.

---

# Dependencies

Requires:

- TASK_024 completed.

Produces:

A complete AI-powered Ask interface connected to the CyberRAG backend.
