# AGENTS.md

# CyberRAG Engineering Guide

This document defines the development rules for CyberRAG.

Every implementation must follow these rules.

---

# Project Vision

CyberRAG is an offline-first Cybersecurity Knowledge Platform.

The application is NOT an AI chatbot.

The SQLite database is the primary source of truth.

Artificial Intelligence is an optional explanation layer.

If every AI provider fails, the application must still function correctly.

---

# MVP Scope

Build only the following modules.

- CVE Database
- CWE Database
- CPE Database
- CVSS Parser
- SQLite Search
- SQLite FTS5
- FastAPI Backend
- Lightweight Frontend
- Optional AI Explanation

Anything outside this scope must NOT be implemented.

---

# Out of Scope

Do NOT implement:

- MITRE ATT&CK
- CAPEC
- CISA KEV
- Sigma Rules
- Threat Actors
- Malware Database
- IOC Database
- User Authentication
- User Accounts
- Admin Dashboard
- Notifications
- Analytics
- Comparison Dashboard

These belong to future versions.

---

# Technology Stack

Backend

- FastAPI

Database

- SQLite

Semantic Search

- ChromaDB

Frontend

- HTML
- CSS
- JavaScript

Language

- Python 3.13+

---

# Architecture Principles

SQLite is always the source of truth.

ChromaDB stores embeddings only.

Never store primary data inside ChromaDB.

Never duplicate business logic.

Prefer composition over duplication.

Keep modules small and reusable.

---

# Database Rules

Required tables:

- cves
- cwes
- cpes
- cve_cpes

Use SQLite foreign keys.

Create indexes where useful.

Store CVSS vector strings.

Parse vectors into readable fields.

Store references as JSON strings.

Never hardcode sample data into production code.

---

# API Rules

Keep APIs RESTful.

Implement only:

GET /

GET /search

GET /cve/{id}

POST /explain

GET /health

Do not create unnecessary endpoints.

---

# Search Rules

Use SQLite FTS5.

Support searching by:

- CVE ID
- Description
- Vendor
- Product
- Severity
- CWE

Use ChromaDB only for semantic search.

---

# AI Rules

AI is optional.

Only use AI when the user explicitly requests an explanation.

Preferred providers:

1. Gemini

Fallback:

2. Ollama

If no provider is available:

Return a friendly message.

The application must continue functioning.

---

# Frontend Rules

Keep UI clean.

Responsive.

Minimal.

Professional.

Avoid unnecessary animations.

Prioritize readability.

---

# Code Style

Follow PEP8.

Use:

- type hints
- dataclasses where appropriate
- docstrings
- meaningful variable names

Avoid magic numbers.

Avoid duplicate code.

Keep functions small.

Single responsibility principle.

---

# Error Handling

Never silently ignore exceptions.

Log meaningful errors.

Return useful API responses.

Fail gracefully.

---

# Logging

Use Python logging.

Avoid print() in production code.

---

# Documentation

Every public function should include:

- Purpose
- Parameters
- Returns

Document non-obvious logic.

---

# Performance

Prefer simplicity.

Optimize only when necessary.

Avoid premature optimization.

---

# Security

Never execute shell commands from user input.

Always validate API input.

Use parameterized SQL queries.

Never concatenate SQL strings.

---

# Git Rules

Make small focused commits.

One logical feature per commit.

Do not combine unrelated changes.

---

# Before Making Changes

Always inspect existing files.

Reuse existing code whenever possible.

Do not rewrite working modules.

Only modify what is required.

---

# Deliverables

Every completed task should:

- Compile successfully
- Pass linting
- Include documentation
- Be production quality
- Match the existing architecture

---

# Development Philosophy

Database first.

Search second.

API third.

Frontend fourth.

AI last.

The application should remain fully usable without any AI model.
