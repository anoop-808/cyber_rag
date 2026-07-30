"""Service to fetch single CVE details from the SQLite database."""

import json
from typing import Any, Optional

from app.core.db import get_db_connection


def get_cve_by_id(cve_id: str) -> Optional[dict[str, Any]]:
    """Retrieve full details for a specific CVE.

    Parameters
    ----------
    cve_id : str
        The ID of the CVE to retrieve (e.g., "CVE-2024-1234").

    Returns
    -------
    dict or None
        A dictionary containing the CVE details, or None if not found.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Fetch main CVE record
        cursor.execute("SELECT * FROM cves WHERE id = ?", (cve_id,))
        cve_row = cursor.fetchone()

        if not cve_row:
            return None

        # Convert sqlite3.Row to dict
        cve_dict = dict(cve_row)

        # Parse references from JSON string
        if cve_dict.get("references"):
            try:
                cve_dict["references"] = json.loads(cve_dict["references"])
            except json.JSONDecodeError:
                cve_dict["references"] = []
        else:
            cve_dict["references"] = []

        # Fetch related CPEs
        cursor.execute(
            """
            SELECT cpes.*
            FROM cpes
            JOIN cve_cpes ON cpes.id = cve_cpes.cpe_id
            WHERE cve_cpes.cve_id = ?
            """,
            (cve_id,)
        )
        cpe_rows = cursor.fetchall()
        cve_dict["cpes"] = [dict(row) for row in cpe_rows]

        return cve_dict
