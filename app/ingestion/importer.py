"""Database importer for NVD CVE dataset."""

import json
import logging
from typing import Any

from app.core.db import get_db_connection

logger = logging.getLogger(__name__)


def import_cve_data(cve_records: list[dict[str, Any]]) -> None:
    """Import a list of cleaned CVE records into the SQLite database.

    Parameters
    ----------
    cve_records : list of dict
        A list of cleaned CVE dictionaries containing fields to insert.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # We start a transaction (get_db_connection already operates in a transaction)

        for cve in cve_records:
            try:
                _insert_single_cve(cursor, cve)
            except Exception as e:
                logger.error(f"Failed to import CVE {cve.get('id', 'UNKNOWN')}: {e}")

        conn.commit()


def _insert_single_cve(cursor: Any, cve: dict[str, Any]) -> None:
    """Insert a single CVE record and its related entities into the database.

    Parameters
    ----------
    cursor : sqlite3.Cursor
        The active database cursor.
    cve : dict
        A cleaned CVE dictionary.
    """
    cve_id = cve.get("id")
    if not cve_id:
        raise ValueError("CVE ID is missing.")

    references_json = json.dumps(cve.get("references", []))

    # We might have multiple CWE IDs but schema supports one or we take the first
    cwe_list = cve.get("cwe", [])
    cwe_id_val = cwe_list[0] if cwe_list else None

    cursor.execute(
        """
        INSERT OR REPLACE INTO cves (
            id, description, published, modified, severity, cvss_version,
            cvss_score, cvss_vector, attack_vector, attack_complexity,
            privileges_required, user_interaction, scope, confidentiality,
            integrity, availability, cwe_id, "references"
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            cve_id,
            cve.get("description"),
            cve.get("published"),
            cve.get("last_modified"),
            cve.get("severity"),
            cve.get("cvss_version"),
            cve.get("cvss_score"),
            cve.get("cvss_vector"),
            cve.get("attack_vector"),
            cve.get("attack_complexity"),
            cve.get("privileges_required"),
            cve.get("user_interaction"),
            cve.get("scope"),
            cve.get("confidentiality"),
            cve.get("integrity"),
            cve.get("availability"),
            cwe_id_val,
            references_json,
        )
    )

    cpes = cve.get("cpes", [])
    for cpe in cpes:
        cpe_id = cpe.get("id")
        uri = cpe.get("uri")
        if not cpe_id or not uri:
            continue

        cursor.execute(
            """
            INSERT OR IGNORE INTO cpes (id, uri, vendor, product, version)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                cpe_id,
                uri,
                cpe.get("vendor"),
                cpe.get("product"),
                cpe.get("version")
            )
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO cve_cpes (cve_id, cpe_id)
            VALUES (?, ?)
            """,
            (cve_id, cpe_id)
        )
