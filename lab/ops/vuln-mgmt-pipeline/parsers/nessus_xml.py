"""
Nessus XML parser for Tenable Nessus scanner output.

Parses .nessus XML files into a normalized list of vulnerability dicts.
Each dict has: scanner, scan_id, plugin_id, cve, cwe, cvss_base, severity,
host (asset_id), port, protocol, name, description.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

try:
    from defusedxml import ElementTree as ET
except ImportError:
    # Fallback to stdlib if defusedxml not installed (less safe, but functional)
    from xml.etree import ElementTree as ET  # type: ignore

logger = logging.getLogger(__name__)


def parse_nessus(file_path: Path) -> List[Dict[str, Any]]:
    """Parse a Nessus XML file and return normalized vulnerability records."""
    try:
        tree = ET.parse(str(file_path))
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        return []

    root = tree.getroot()
    vulns = []

    # Get scan metadata
    scan_name_elem = root.find(".//Report/@name")
    scan_name = scan_name_elem if scan_name_elem is not None else "unknown"
    scan_id = file_path.stem

    # Iterate over each ReportItem (vulnerability finding)
    for report_item in root.iter("ReportItem"):
        try:
            port = report_item.get("port", "0")
            protocol = report_item.get("protocol", "tcp")
            plugin_id = report_item.get("pluginID", "0")
            plugin_name = report_item.get("pluginName", "")
            severity = report_item.get("severity", "0")  # 0=Info, 1=Low, 2=Med, 3=High, 4=Critical

            # Host (asset_id)
            host_elem = report_item.find("host")
            host = host_elem.text if host_elem is not None else "unknown"

            # CVE(s)
            cve_elems = report_item.findall("cve")
            cves = [c.text for c in cve_elems if c.text]

            # CWE
            cwe_elem = report_item.find("cwe")
            cwe = cwe_elem.text if cwe_elem is not None else ""

            # CVSS base score
            cvss_elem = report_item.find("cvss_base_score")
            try:
                cvss_base = float(cvss_elem.text) if cvss_elem is not None and cvss_elem.text else 0.0
            except ValueError:
                cvss_base = 0.0

            # Description
            desc_elem = report_item.find("description")
            description = desc_elem.text if desc_elem is not None else ""

            # One vulnerability record per CVE (one Nessus finding can have multiple CVEs)
            if not cves:
                cves = [""]  # Nessus findings without CVE still need processing

            for cve in cves:
                vulns.append({
                    "scanner": "nessus",
                    "scan_id": scan_id,
                    "plugin_id": plugin_id,
                    "cve": cve,
                    "cwe": cwe,
                    "cvss_base": cvss_base,
                    "severity": severity,
                    "host": host,
                    "asset_id": host,
                    "port": port,
                    "protocol": protocol,
                    "name": plugin_name,
                    "description": description,
                })
        except Exception as e:
            logger.warning(f"Failed to parse ReportItem in {file_path}: {e}")
            continue

    logger.info(f"Parsed {len(vulns)} vulnerabilities from {file_path.name}")
    return vulns