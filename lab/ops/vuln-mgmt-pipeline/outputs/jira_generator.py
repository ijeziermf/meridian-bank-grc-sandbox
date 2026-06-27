"""
Jira ticket JSON generator for vulnerability remediation.

Generates Jira-formatted JSON for each vulnerability, ready to POST to
the bank's Jira instance via webhook or manual upload.
"""

from typing import Dict, Any
from datetime import datetime, timezone


# FFIEC domain to Jira label mapping
FFIEC_TO_LABEL = {
    "audit": "ffeiec-audit",
    "management": "ffeiec-management",
    "development": "ffeiec-development",
    "operations": "ffeiec-operations",
    "infosec": "ffeiec-infosec",
    "bcp": "ffeiec-bcp",
    "outsourcing": "ffeiec-outsourcing",
}

# CVSS to Jira priority mapping
CVSS_TO_PRIORITY = {
    (9.0, 10.0): "Highest",
    (7.0, 8.99): "High",
    (4.0, 6.99): "Medium",
    (0.1, 3.99): "Low",
    (0.0, 0.0): "Lowest",
}


def _priority_from_cvss(cvss: float) -> str:
    for (low, high), priority in CVSS_TO_PRIORITY.items():
        if low <= cvss <= high:
            return priority
    return "Medium"


def generate_jira_ticket(vuln: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a Jira-formatted ticket for a vulnerability."""
    cvss = vuln.get("cvss_base", 0.0)
    priority = _priority_from_cvss(cvss)
    domain_label = FFIEC_TO_LABEL.get(vuln.get("ffeiec_domain", "operations"), "ffeiec-operations")
    timestamp = datetime.now(timezone.utc).isoformat()

    summary = f"[{vuln.get('scanner', '').upper()}] {vuln.get('cve', 'NOCVE') or 'NOCVE'} - {vuln.get('name', 'Vulnerability')[:100]}"
    if vuln.get("host"):
        summary += f" on {vuln['host']}"

    description_lines = [
        f"**Scanner**: {vuln.get('scanner', '')}",
        f"**Plugin/QID**: {vuln.get('plugin_id', '')}",
        f"**CVE**: {vuln.get('cve', 'N/A')}",
        f"**CWE**: {vuln.get('cwe', 'N/A')}",
        f"**CVSS Base**: {cvss}",
        f"**Severity**: {vuln.get('severity', '')}",
        f"**Asset (Host)**: {vuln.get('host', '')}",
        f"**Port/Protocol**: {vuln.get('port', '')}/{vuln.get('protocol', '')}",
        f"**FFIEC Domain**: {vuln.get('ffeiec_domain', '')}",
        "",
        "**Description**:",
        vuln.get("description", "(no description)"),
        "",
        f"**Ticket Created**: {timestamp}",
        "**Source**: Meridian Bank Vulnerability Management Pipeline",
    ]

    return {
        "fields": {
            "project": {"key": "VULN"},
            "summary": summary,
            "description": "\n".join(description_lines),
            "issuetype": {"name": "Bug"},
            "priority": {"name": priority},
            "labels": [
                "vulnerability-management",
                f"scanner-{vuln.get('scanner', '')}",
                domain_label,
            ],
        },
        "scanner_metadata": {
            "scanner": vuln.get("scanner"),
            "scan_id": vuln.get("scan_id"),
            "plugin_id": vuln.get("plugin_id"),
            "asset_id": vuln.get("asset_id"),
            "cvss_base": cvss,
            "ffeiec_domain": vuln.get("ffeiec_domain"),
            "created_at": timestamp,
        },
    }