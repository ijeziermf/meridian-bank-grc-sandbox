"""
Qualys CSV parser for Qualys VMDR scanner output.

Parses Qualys CSV exports into normalized vulnerability dicts matching the
Nessus parser schema.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def parse_qualys(file_path: Path) -> List[Dict[str, Any]]:
    """Parse a Qualys CSV file and return normalized vulnerability records."""
    vulns = []
    scan_id = file_path.stem

    try:
        with open(file_path, newline="", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cve = row.get("CVE", "") or ""
                    cwe = row.get("CWE", "") or ""
                    cvss_str = row.get("CVSS Base", "") or row.get("CVSS", "") or "0"
                    try:
                        cvss_base = float(cvss_str)
                    except ValueError:
                        cvss_base = 0.0

                    severity_map = {
                        "Info": "0", "Low": "1", "Medium": "2", "High": "3", "Critical": "4",
                    }
                    severity = severity_map.get(row.get("Severity", ""), "0")

                    vulns.append({
                        "scanner": "qualys",
                        "scan_id": scan_id,
                        "plugin_id": row.get("QID", "") or row.get("Plugin", ""),
                        "cve": cve,
                        "cwe": cwe,
                        "cvss_base": cvss_base,
                        "severity": severity,
                        "host": row.get("IP", "") or row.get("Host", ""),
                        "asset_id": row.get("IP", "") or row.get("Host", ""),
                        "port": row.get("Port", "0"),
                        "protocol": row.get("Protocol", "tcp"),
                        "name": row.get("Title", ""),
                        "description": row.get("Description", ""),
                    })
                except Exception as e:
                    logger.warning(f"Failed to parse row in {file_path}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Failed to open {file_path}: {e}")

    logger.info(f"Parsed {len(vulns)} vulnerabilities from {file_path.name}")
    return vulns