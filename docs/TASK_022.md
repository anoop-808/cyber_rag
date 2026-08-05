# TASK_022.md

# Phase 9 – Frontend Project Setup

## Status

Planned

---

# Objective

Initialize the CyberRAG frontend application.

This task establishes the frontend foundation that will communicate with the existing FastAPI backend.

This task is frontend-only.

---

# Background

Phase 8 completed the production-ready backend API.

CyberRAG now exposes:

- POST /ask
- POST /search
- GET /cve/{id}

The frontend will consume these APIs.

No business logic should be duplicated.

---

# Scope

Implement:

- React project initialization
- Vite setup
- Project folder structure
- Routing
- API client
- Global styles
- Environment configuration

Do NOT implement:

- Search UI
- Ask UI
- Result rendering
- Authentication
- State management beyond basic app setup

---

# Functional Requirements

## Framework

Use:

- React
- Vite
- TypeScript
- React Router

---

## Folder Structure

Create:

frontend/

Inside:

```text
src/
    api/
    components/
    pages/
    hooks/
    assets/
    styles/
    types/
```

---

## Routing

Configure routes for future pages:

```text
/

/search

/ask

/cve/:id
```

Pages may contain placeholder content.

---

## API Client

Create reusable API client.

Support:

```text
POST /ask

POST /search

GET /cve/{id}
```

API base URL must come from environment variables.

---

## Environment

Support:

```text
VITE_API_URL
```

through:

```
.env
```

---

## Styling

Create:

- Global stylesheet
- Theme variables
- Responsive layout foundation

No final UI required.

---

## Error Handling

Gracefully handle:

- Missing API URL
- Invalid configuration

Do not implement runtime error pages.

---

## Logging

No logging required.

---

## Performance Requirements

- Fast startup
- Minimal dependencies
- Modular folder structure

---

# Folder Changes

Create:

```text
frontend/
```

---

# Tests

Verify:

- Project builds
- Routes load
- API client compiles
- Environment variables resolve

---

# Acceptance Criteria

The task is complete when:

✓ React initialized.

✓ Vite configured.

✓ Routing configured.

✓ API client created.

✓ Environment configuration working.

✓ Project builds successfully.

---

# Constraints

Do not implement:

- Search interface
- Ask interface
- Result pages
- Authentication

Only initialize the frontend.

---

# Out of Scope

Belongs to later tasks:

- Search UI
- Ask UI
- CVE Detail UI
- Styling
- Animations

---

# Definition of Done

- Frontend project created.
- Routing configured.
- API client implemented.
- Ready for TASK_023.

---

# Dependencies

Requires:

- Phase 8 completed.

Produces:

The frontend foundation for CyberRAG.
