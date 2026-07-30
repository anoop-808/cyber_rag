"""CVE Detail retrieval service."""

import json
from typing import Any, Optional
from app.core.db import get_db_connection

def get_cve_detail(cve_id: str) -> Optional[dict[str, Any]]:
    """Retrieve complete CVE details by ID.

    Parameters
    ----------
    cve_id : str
        The ID of the CVE to retrieve.

    Returns
    -------
    dict or None
        A dictionary containing the CVE details, or None if not found.
    """
    sql_cve = """
        SELECT
            cves.id,
            cves.description,
            cves.published,
            cves.modified,
            cves.severity,
            cves.cvss_version,
            cves.cvss_score,
            cves.cvss_vector,
            cves.attack_vector,
            cves.attack_complexity,
            cves.privileges_required,
            cves.user_interaction,
            cves.scope,
            cves.confidentiality,
            cves.integrity,
            cves.availability,
            cves.cwe_id,
            cves."references",
            cwes.name AS cwe_name,
            cwes.description AS cwe_description
        FROM cves
        LEFT JOIN cwes ON cves.cwe_id = cwes.id
        WHERE cves.id = ?
    """

    sql_cpes = """
        SELECT cpes.id, cpes.uri, cpes.vendor, cpes.product, cpes.version
        FROM cves
        JOIN cve_cpes ON cves.id = cve_cpes.cve_id
        JOIN cpes ON cve_cpes.cpe_id = cpes.id
        WHERE cves.id = ?
    """

    with get_db_connection() as conn:
        cursor = conn.execute(sql_cve, (cve_id,))
        cve_row = cursor.fetchone()

        if not cve_row:
            return None

        # Fetch CPEs
        cursor_cpes = conn.execute(sql_cpes, (cve_id,))
        cpes = []
        for row in cursor_cpes:
            cpes.append({
                "id": row["id"],
                "uri": row["uri"],
                "vendor": row["vendor"],
                "product": row["product"],
                "version": row["version"],
            })

    # Parse references JSON
    references_json = cve_row["references"]
    references = []
    if references_json:
        try:
            references = json.loads(references_json)
        except json.JSONDecodeError:
            pass

    return {
        "id": cve_row["id"],
        "description": cve_row["description"],
        "published": cve_row["published"],
        "modified": cve_row["modified"],
        "severity": cve_row["severity"],
        "cvss": {
            "version": cve_row["cvss_version"],
            "score": cve_row["cvss_score"],
            "vector": cve_row["cvss_vector"],
            "metrics": {
                "attack_vector": cve_row["attack_vector"],
                "attack_complexity": cve_row["attack_complexity"],
                "privileges_required": cve_row["privileges_required"],
                "user_interaction": cve_row["user_interaction"],
                "scope": cve_row["scope"],
                "confidentiality": cve_row["confidentiality"],
                "integrity": cve_row["integrity"],
                "availability": cve_row["availability"],
            }
        },
        "cwe": {
            "id": cve_row["cwe_id"],
            "name": cve_row["cwe_name"],
            "description": cve_row["cwe_description"],
        } if cve_row["cwe_id"] else None,
        "cpes": cpes,
        "references": references,
    }
