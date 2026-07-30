"""Unit tests for NVD CVE extractor."""

from app.ingestion.extractor import extract_cve_fields, extract_cvss_data, extract_cpes


def test_extract_cvss_v31():
    """Test extracting CVSS v3.1 data."""
    metrics = {
        "cvssMetricV31": [
            {
                "cvssData": {
                    "version": "3.1",
                    "vectorString": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                    "baseScore": 9.8,
                    "attackVector": "NETWORK",
                    "attackComplexity": "LOW",
                    "privilegesRequired": "NONE",
                    "userInteraction": "NONE",
                    "scope": "UNCHANGED",
                    "confidentialityImpact": "HIGH",
                    "integrityImpact": "HIGH",
                    "availabilityImpact": "HIGH"
                },
                "baseSeverity": "CRITICAL"
            }
        ],
        "cvssMetricV2": [
            {
                "cvssData": {
                    "version": "2.0",
                    "baseScore": 10.0
                }
            }
        ]
    }

    result = extract_cvss_data(metrics)

    assert result["cvss_version"] == "3.1"
    assert result["cvss_score"] == 9.8
    assert result["severity"] == "CRITICAL"
    assert result["attack_vector"] == "NETWORK"


def test_extract_cvss_v2():
    """Test extracting CVSS v2 data (fallback)."""
    metrics = {
        "cvssMetricV2": [
            {
                "cvssData": {
                    "version": "2.0",
                    "vectorString": "AV:N/AC:L/Au:N/C:C/I:C/A:C",
                    "baseScore": 10.0,
                    "accessVector": "NETWORK",
                    "accessComplexity": "LOW",
                    "authentication": "NONE",
                    "confidentialityImpact": "COMPLETE",
                    "integrityImpact": "COMPLETE",
                    "availabilityImpact": "COMPLETE"
                },
                "baseSeverity": "HIGH"
            }
        ]
    }

    result = extract_cvss_data(metrics)

    assert result["cvss_version"] == "2.0"
    assert result["cvss_score"] == 10.0
    assert result["severity"] == "HIGH"
    assert result["attack_vector"] == "NETWORK"
    assert result["privileges_required"] == "NONE"


def test_extract_cvss_empty():
    """Test extracting empty metrics."""
    result = extract_cvss_data(None)
    assert result["cvss_score"] is None

    result = extract_cvss_data({})
    assert result["cvss_score"] is None


def test_extract_cpes():
    """Test extracting CPE configurations."""
    configurations = [
        {
            "nodes": [
                {
                    "cpeMatch": [
                        {
                            "criteria": "cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*",
                            "matchCriteriaId": "uuid-1"
                        },
                        {
                            "criteria": "cpe:2.3:o:vendor:os:*:*:*:*:*:*:*:*"
                            # Missing matchCriteriaId to test fallback to criteria
                        }
                    ]
                }
            ]
        }
    ]

    cpes = extract_cpes(configurations)

    assert len(cpes) == 2
    assert cpes[0]["id"] == "uuid-1"
    assert cpes[0]["vendor"] == "vendor"
    assert cpes[0]["product"] == "product"
    assert cpes[0]["version"] == "1.0"

    assert cpes[1]["id"] == "cpe:2.3:o:vendor:os:*:*:*:*:*:*:*:*"
    assert cpes[1]["vendor"] == "vendor"
    assert cpes[1]["product"] == "os"
    assert cpes[1]["version"] is None


def test_extract_cve_fields():
    """Test full extraction of CVE fields."""
    cve = {
        "id": "CVE-2024-1234",
        "descriptions": [{"lang": "en", "value": "Test desc"}],
        "metrics": {
            "cvssMetricV31": [{"cvssData": {"baseScore": 9.8}}]
        },
        "weaknesses": [{"description": [{"lang": "en", "value": "CWE-79"}]}],
        "references": [{"url": "http://example.com"}],
        "configurations": [{"nodes": [{"cpeMatch": [{"criteria": "cpe:2.3:a:vendor:product:1.0"}]}]}]
    }

    result = extract_cve_fields(cve)

    assert result["id"] == "CVE-2024-1234"
    assert result["description"] == "Test desc"
    assert result["cvss_score"] == 9.8
    assert result["cwe"] == ["CWE-79"]
    assert result["references"] == ["http://example.com"]
    assert len(result["cpes"]) == 1
    assert result["cpes"][0]["vendor"] == "vendor"
