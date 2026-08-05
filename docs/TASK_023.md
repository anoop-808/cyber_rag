# TASK_023.md

# Phase 9 – Search Interface

## Status

Planned

---

# Objective

Implement the CyberRAG Search Interface.

This task creates the first functional frontend page that communicates with the existing `/search` API endpoint.

This task is frontend-only.

---

# Background

TASK_022 initialized the frontend project.

CyberRAG already exposes:

- POST /search

The Search Interface allows users to search the vulnerability database using natural language without invoking the language model.

---

# Scope

Implement:

- Search page
- Search input
- Filter controls
- Search button
- Loading state
- Error state
- API integration

Do NOT implement:

- AI answer generation
- CVE detail page
- Authentication
- Chat interface
- Advanced styling

---

# Functional Requirements

## Search Page

Create:

```text
/search
```

The page should contain:

- Search input
- Search button
- Severity filter
- Loading indicator
- Error message area

---

## Search Input

Allow users to enter queries such as:

```text
openssl remote code execution

apache privilege escalation

windows smb vulnerability
```

The input must validate empty submissions.

---

## Filters

Support optional filters.

Initially:

- Severity

Possible values:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

---

## Search Request

Call:

```text
POST /search
```

using:

```json
{
  "query": "...",
  "filters": {
    "severity": "HIGH"
  }
}
```

Reuse the API client created in TASK_022.

---

## Loading State

Display a loading indicator while waiting for the backend.

Disable repeated submissions until the request completes.

---

## Error Handling

Display friendly errors for:

- Empty query
- Network failure
- API failure
- Invalid response

Do not expose raw backend exceptions.

---

## Navigation

Successful searches should remain on:

```text
/search
```

Results will be implemented in TASK_024.

---

# Folder Changes

Create or update:

```text
frontend/src/pages/SearchPage.tsx

frontend/src/components/SearchBar.tsx

frontend/src/components/SeverityFilter.tsx
```

Reuse existing project structure.

---

# Public Interface

Expose:

```text
/search
```

through React Router.

---

# Performance Requirements

- Debounce unnecessary requests.
- Avoid duplicate API calls.
- Keep rendering responsive.

---

# Tests

Verify:

- Empty query validation
- Successful request
- Failed request
- Loading state
- Filter selection
- API invocation

---

# Acceptance Criteria

The task is complete when:

✓ Search page implemented.

✓ Search input works.

✓ Filters work.

✓ Requests reach POST /search.

✓ Loading state implemented.

✓ Existing frontend builds successfully.

---

# Constraints

Do not implement:

- Search results
- AI responses
- CVE detail page
- UI animations

Only implement the search interface.

---

# Out of Scope

Belongs to later tasks:

- Search Results
- Ask AI
- CVE Detail View
- UI Polish

---

# Definition of Done

- Search interface implemented.
- API integration working.
- Frontend builds successfully.
- Ready for TASK_024.

---

# Dependencies

Requires:

- TASK_022 completed.

Produces:

A functional frontend search interface connected to the CyberRAG backend.
