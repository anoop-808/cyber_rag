# TASK 006 - React Frontend (Phase 5C)

## Objective

Improve the visual design and user experience of the existing React frontend.

This phase focuses entirely on UI polish.

No backend changes.

No new application features.

---

# Scope

This task includes:

- Improved layout
- Better typography
- Better spacing
- Improved CVE cards
- Better Detail View presentation
- Empty state
- Responsive layout improvements
- Visual consistency

---

# This phase does NOT include

- Semantic Search
- AI Explain
- Authentication
- Filters
- Pagination
- Dark Mode
- React Router
- Charts
- Dashboard

---

# Design Goals

The interface should feel:

- clean
- modern
- professional
- cybersecurity themed
- easy to scan

Avoid excessive colors.

Prefer neutral backgrounds with severity colors.

---

# Search Page

Improve:

- page spacing
- search bar alignment
- button sizing
- card spacing
- typography

Search should remain centered.

---

# CVE Cards

Improve readability.

Each card should clearly separate:

- CVE ID
- Severity
- CVSS
- Description

Cards should have:

- hover effect
- cursor pointer
- subtle elevation

---

# Detail View

Improve layout.

Display information using sections.

Example sections:

General Information

Risk

Description

Affected Products

References

Large descriptions should wrap cleanly.

---

# Severity Colors

LOW

Green

MEDIUM

Yellow

HIGH

Orange

CRITICAL

Red

UNKNOWN

Gray

Use colors consistently.

---

# Empty State

When no search has been performed:

Display a friendly message.

Example:

"Search for a CVE to begin."

When no results exist:

Display:

"No matching CVEs found."

---

# Responsive Design

Application should remain usable on:

Desktop

Tablet

Mobile

Use CSS only.

No CSS frameworks.

---

# Accessibility

Buttons must have clear focus styles.

Links should remain readable.

Use semantic HTML where practical.

---

# Constraints

Frontend only.

Do not modify:

- FastAPI
- SQLite
- Retrieval
- API
- Tests

---

# Testing

Verify:

Search still works.

Detail View still works.

Back navigation still works.

Responsive layout.

Frontend builds successfully.

Backend tests continue to pass.

---

# Acceptance Criteria

✓ Professional appearance

✓ Better typography

✓ Better spacing

✓ Responsive layout

✓ Hover effects

✓ Empty states

✓ Severity colors

✓ Existing functionality unchanged

✓ Frontend builds

✓ Backend tests pass

---

# Definition of Done

A first-time user should immediately understand how to search for and inspect a CVE without additional instructions.

---


# UX Principles

- Maintain visual hierarchy.
- Keep the search bar as the primary focal point.
- Ensure severity badges are immediately recognizable.
- Minimize unnecessary scrolling.
- Use whitespace to improve readability.
- Keep the interface simple and uncluttered.



# Files Allowed to Change

Frontend only.

Expected:

frontend/src/**

frontend/public/**

frontend/README.md (optional)

Do NOT modify:

app/**

storage/**

tests/**

docs/TASK_001.md

docs/TASK_002.md

docs/TASK_003.md

docs/TASK_004.md

docs/TASK_005.md
