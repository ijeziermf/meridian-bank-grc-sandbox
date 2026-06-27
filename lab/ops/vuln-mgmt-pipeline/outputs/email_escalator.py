"""
Email escalation template generator for critical CVEs (CVSS >= 9.0).

Generates RFC 5322-compliant email text ready for delivery via SMTP.
"""

from typing import Dict, Any
from datetime import datetime, timezone


def generate_escalation_email(vuln: Dict[str, Any]) -> str:
    """Generate an escalation email for a critical-severity vulnerability."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    cvss = vuln.get("cvss_base", 0.0)
    cve = vuln.get("cve", "N/A")
    host = vuln.get("host", "unknown")
    name = vuln.get("name", "Vulnerability")
    domain = vuln.get("ffeiec_domain", "operations")

    subject = f"[CRITICAL CVE ESCALATION] {cve} CVSS {cvss} on {host}"

    body = f"""From: vuln-pipeline@meridianbank.example
To: ciso@meridianbank.example; cio@meridianbank.example; soc@meridianbank.example
Subject: {subject}
Date: {datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}

CRITICAL VULNERABILITY DETECTED
==============================

CVE:                 {cve}
CVSS Base Score:     {cvss}  (threshold for escalation: 9.0)
Asset (Host):        {host}
Port/Protocol:       {vuln.get('port', '')}/{vuln.get('protocol', '')}
Scanner:             {vuln.get('scanner', '')} (plugin {vuln.get('plugin_id', '')})
FFIEC Domain:        {domain}

VULNERABILITY TITLE
-------------------
{name}

DESCRIPTION
-----------
{vuln.get('description', '(no description)')}

REQUIRED ACTIONS
----------------
1. Validate this finding against the affected asset within 24 hours.
2. Apply mitigation per the bank's vulnerability management policy:
   - Patch if available and within change window
   - Compensating control if patch not available
   - Vendor engagement if critical vendor (FIS, ACI, Fiserv, Jack Henry)
3. Update the Jira ticket with remediation status.
4. Notify the OCC primary regulator within 48 hours if this is a
   material operational risk per FFIEC IT Examination Handbook.
5. Close the Jira ticket only after remediation verification.

ESCALATION CONTACTS
-------------------
- CISO: ciso@meridianbank.example
- CIO: cio@meridianbank.example
- SOC: soc@meridianbank.example
- BSA Officer (if fraud/AML related): bsa-officer@meridianbank.example

TIMESTAMP
---------
Detected: {timestamp}
Source: Meridian Bank Vulnerability Management Pipeline
Scan ID: {vuln.get('scan_id', '')}

--
This email was generated automatically by the Meridian Vulnerability
Management Pipeline. Do not reply. Update the Jira ticket for status.
"""

    return body