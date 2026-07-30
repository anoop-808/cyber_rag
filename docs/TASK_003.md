# TASK 003 - CVE Detail API

## Objective

Implement a FastAPI endpoint that returns complete information for a single CVE stored in the SQLite database.

---

## Endpoint

GET /cve/{id}

Example:

GET /cve/CVE-2024-3094

---

## Requirements

- Fetch a single CVE by ID from SQLite.
- Return HTTP 200 for existing CVEs.
- Return HTTP 404 if the CVE does not exist.
- Keep implementation consistent with existing project architecture.

---

## Response

The response should include:

- CVE ID
- Description
- Published Date
- Last Modified Date
- Severity
- CVSS Information
- CWE Information
- Related CPE Products
- References

---

## Constraints

Do NOT implement:

- AI
- Semantic Search
- React UI
- Ollama
- Gemini
- ChromaDB

Only implement the backend endpoint.

---

## Testing

Add unit tests for:

- Existing CVE
- Non-existing CVE

All existing tests must continue to pass.

---

## Acceptance Criteria

- GET /cve/{id} works.
- Swagger documentation displays the endpoint.
- Tests pass.
- Existing functionality remains unchanged.
