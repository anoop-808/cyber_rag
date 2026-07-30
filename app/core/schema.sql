-- SQLite Database Schema for CyberRAG

CREATE TABLE IF NOT EXISTS cves (
    id TEXT PRIMARY KEY,
    description TEXT,
    published TEXT,
    modified TEXT,
    severity TEXT,
    cvss_version TEXT,
    cvss_score REAL,
    cvss_vector TEXT,
    attack_vector TEXT,
    attack_complexity TEXT,
    privileges_required TEXT,
    user_interaction TEXT,
    scope TEXT,
    confidentiality TEXT,
    integrity TEXT,
    availability TEXT,
    cwe_id TEXT,
    "references" TEXT -- JSON array of strings
);

CREATE TABLE IF NOT EXISTS cwes (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS cpes (
    id TEXT PRIMARY KEY,
    uri TEXT UNIQUE NOT NULL,
    vendor TEXT,
    product TEXT,
    version TEXT
);

CREATE TABLE IF NOT EXISTS cve_cpes (
    cve_id TEXT NOT NULL,
    cpe_id TEXT NOT NULL,
    PRIMARY KEY (cve_id, cpe_id),
    FOREIGN KEY (cve_id) REFERENCES cves (id) ON DELETE CASCADE,
    FOREIGN KEY (cpe_id) REFERENCES cpes (id) ON DELETE CASCADE
);
