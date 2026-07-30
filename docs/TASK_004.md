# TASK 004 - React Frontend (Phase 5A)

## Objective

Build the initial React frontend for CyberRAG that connects to the existing FastAPI backend.

This phase establishes the frontend foundation and implements CVE keyword search only.

---

# Scope

This task only includes:

- React application setup
- Vite project
- Search page
- Backend API integration
- Display search results

This phase does NOT include:

- CVE Detail View
- AI Explain
- Semantic Search
- Authentication
- User Accounts
- Dashboard
- Charts
- Dark Mode
- Pagination
- Filters

Those belong to later phases.

---

# Architecture

Frontend must be a completely separate application.

Repository structure:

```
cyber-rag/

app/
storage/
tests/

frontend/
```

Do NOT place React code inside the Python application.

---

# Technology Stack

Framework:
- React

Build Tool:
- Vite

HTTP Client:
- Axios

Styling:
- Plain CSS

State Management:
- React Hooks only

Do NOT use:

- Redux
- TailwindCSS
- Material UI
- Bootstrap
- Next.js
- Zustand
- React Query

Keep the frontend lightweight.

---

# Functional Requirements

## Home Page

Display:

- Project title
- Search input
- Search button

Example:

--------------------------------------------------

CyberRAG

[ Search vulnerabilities........ ]

        Search

--------------------------------------------------

---

## Search

When the user submits a keyword:

Call:

GET /search

Example:

/search?query=openssl

---

## Search Results

Display a list of CVEs.

Each result should display:

- CVE ID
- Severity
- Short Description
- CWE ID (if available)

Each result should appear as a clickable card.

Example:

--------------------------------

CVE-1999-0428

HIGH

OpenSSL allows...

CWE-384

--------------------------------

---

# API Integration

Use the existing backend.

Do NOT modify any backend endpoint.

Expected backend endpoints:

GET /

GET /search

POST /ask

GET /cve/{id}

Only GET /search is used in this phase.

---

# Folder Structure

Frontend should follow this structure.

frontend/

src/

components/

SearchBar.jsx

SearchResults.jsx

CVECard.jsx

pages/

Home.jsx

services/

api.js

App.jsx

main.jsx

styles/

App.css

---

# Error Handling

Display a user-friendly message when:

- Backend is unavailable
- Search returns zero results

Do not display raw exceptions.

---

# Loading State

Display a loading indicator while waiting for the backend response.

---

# Constraints

Do NOT modify:

- FastAPI backend
- SQLite database
- Search implementation
- Retrieval logic
- Existing API routes
- Existing tests

Frontend only.

---

# Testing

Verify:

- React application builds successfully.
- Search input works.
- Results render correctly.
- Existing backend tests continue to pass.

---

# Acceptance Criteria

The implementation is complete when:

- React frontend runs successfully.
- Search page loads.
- User can search CVEs.
- Results are displayed.
- Clicking a result is not required in this phase.
- Backend remains unchanged.
- Existing backend tests pass.
- Frontend builds successfully.

---

# Out of Scope

The following belong to future phases.

Phase 5B

- CVE Detail Page

Phase 5C

- UI Improvements
- Better Layout

Phase 5D

- Loading Improvements
- Error Improvements
- Responsive Polish

Phase 6

- Semantic Search

Phase 7

- AI Explain

---

# Definition of Done

✓ React application created

✓ Vite configured

✓ Axios configured

✓ Search page implemented

✓ Backend integration working

✓ Search results displayed

✓ Existing backend functionality unchanged

✓ Backend tests continue to pass

# Files Allowed to Change

Frontend only.

Expected new/modified paths:

- frontend/**
- package.json (inside frontend only)
- vite.config.*
- README.md (only if frontend setup instructions are added)

Do NOT modify:

- app/**
- storage/**
- tests/**
- docs/TASK_001.md
- docs/TASK_002.md
- docs/TASK_003.md

