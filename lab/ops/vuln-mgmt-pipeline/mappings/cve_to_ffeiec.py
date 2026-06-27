"""
Map CVE/CWE to FFIEC IT Examination Handbook domain.

FFIEC domains:
- audit: Logging, monitoring, SIEM, log retention
- management: Governance, risk management, policy
- development: SDLC, secure coding, code review
- operations: Patching, configuration, vulnerability management
- infosec: Access control, encryption, network security
- bcp: Business continuity, disaster recovery, resilience
- outsourcing: Vendor, cloud, third-party
"""

import logging
import re
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
MAPPING_FILE = SCRIPT_DIR / "ffeiec_domains.yaml"

# Keyword heuristics for CVE/CWE classification
DOMAIN_KEYWORDS = {
    "audit": ["log", "siem", "monitor", "audit trail", "syslog", "event"],
    "management": ["policy", "governance", "risk management", "compliance"],
    "development": ["sdlc", "code injection", "deserialization", "xss", "cross-site",
                    "buffer overflow", "memory corruption", "race condition"],
    "operations": ["patch", "vulnerability", "cve", "configuration", "default password",
                   "weakness"],
    "infosec": ["access control", "authentication", "authorization", "encryption", "tls",
                "ssl", "ssh", "rce", "remote code execution", "privilege escalation",
                "sql injection", "csrf", "directory traversal", "xxe"],
    "bcp": ["backup", "recovery", "resilience", "failover", "redundancy"],
    "outsourcing": ["vendor", "third-party", "supply chain", "managed service"],
}

# Load curated mapping (curated for known critical CVEs that need explicit classification)
_CURATED_MAPPING: dict = {}


def _load_curated_mapping() -> None:
    """Load curated CVE-to-FFIEC-domain mapping from YAML."""
    global _CURATED_MAPPING
    if yaml is None:
        logger.warning("PyYAML not installed; curated mapping disabled")
        return
    if MAPPING_FILE.exists():
        try:
            with open(MAPPING_FILE) as f:
                _CURATED_MAPPING = yaml.safe_load(f) or {}
            logger.info(f"Loaded {len(_CURATED_MAPPING)} curated CVE mappings")
        except Exception as e:
            logger.warning(f"Failed to load curated mapping: {e}")


def map_cve_to_ffeiec_domain(cve: str, cwe: str = "") -> str:
    """Map a CVE (and optional CWE) to the most relevant FFIEC domain.

    Returns one of: audit, management, development, operations, infosec, bcp, outsourcing.
    Falls back to 'operations' as the default for vulnerability management.
    """
    if not _CURATED_MAPPING:
        _load_curated_mapping()

    if not cve:
        return "operations"

    # Check curated mapping first
    if cve in _CURATED_MAPPING:
        return _CURATED_MAPPING[cve]

    # Keyword heuristic (using CWE if available)
    combined = f"{cve} {cwe}".lower()
    domain_scores: dict = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined)
        if score > 0:
            domain_scores[domain] = score

    if not domain_scores:
        return "operations"  # Default for vulnerability management

    # Return highest-scoring domain
    return max(domain_scores, key=lambda d: domain_scores[d])


def map_cve(cve: str) -> str:
    """Public entry point - map a single CVE to FFIEC domain."""
    return map_cve_to_ffeiec_domain(cve)