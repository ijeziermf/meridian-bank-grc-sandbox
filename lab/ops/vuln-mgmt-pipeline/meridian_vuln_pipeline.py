"""
Meridian Bank Vulnerability Management Pipeline - Main Daemon

Ingests scanner output (Nessus/Qualys), maps CVEs to FFIEC domains, generates
remediation tickets, escalates critical findings. Stateful processing with
crash recovery via NDJSON append-only state file.

Satisfies the never-fail contract: stage to /tmp, atomic rename, bounded retry,
verify the write, exit 0 unconditionally.
"""

import argparse
import json
import logging
import os
import signal
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Third-party (configured in requirements.txt)
try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

# Local imports (absolute paths so launchd daemon can find them)
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from parsers.nessus_xml import parse_nessus  # noqa: E402
from parsers.qualys_csv import parse_qualys  # noqa: E402
from mappings.cve_to_ffeiec import map_cve_to_ffeiec_domain  # noqa: E402
from outputs.jira_generator import generate_jira_ticket  # noqa: E402
from outputs.email_escalator import generate_escalation_email  # noqa: E402
from state.state_manager import StateManager  # noqa: E402


# Logging setup - write to /var/log/meridian-vuln-pipeline.log if writable, else /tmp
LOG_PATH = "/var/log/meridian-vuln-pipeline.log"
try:
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
except PermissionError:
    LOG_PATH = "/tmp/meridian-vuln-pipeline.log"
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

logger = logging.getLogger(__name__)


# Config defaults
DEFAULT_CONFIG = {
    "nessus_input_dir": "/var/scanner/nessus/incoming",
    "qualys_input_dir": "/var/scanner/qualys/incoming",
    "jira_output_dir": "/var/scanner/jira-outgoing",
    "escalation_output_dir": "/var/scanner/escalation-outgoing",
    "state_file": "/var/lib/meridian-vuln/state.ndjson",
    "polling_interval_seconds": 300,
    "cvss_escalation_threshold": 9.0,
    "max_retry_seconds": 30,
}


def load_config(config_path: Path) -> dict:
    """Load config from YAML file with fallback to defaults."""
    config = dict(DEFAULT_CONFIG)
    if config_path.exists():
        try:
            with open(config_path) as f:
                user_config = yaml.safe_load(f) or {}
            config.update(user_config)
        except Exception as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
    return config


def discover_inputs(input_dir: str) -> list:
    """Discover scanner output files in the input directory."""
    input_path = Path(input_dir)
    if not input_path.exists():
        return []
    return sorted(input_path.glob("*.nessus")) + sorted(input_path.glob("*.csv"))


def stage_to_tmp(content: bytes, suffix: str) -> Path:
    """Stage content to /tmp before atomic rename into target."""
    fd, tmp_path = tempfile.mkstemp(suffix=suffix, dir="/tmp")
    try:
        os.write(fd, content)
    finally:
        os.close(fd)
    return Path(tmp_path)


def safe_write_bytes(target_path: Path, content: bytes, max_retry_seconds: int = 30) -> bool:
    """Stage to /tmp, then atomic-rename into target. Bounded retry by wall time.

    Returns True if write succeeded, False if it failed (logged but does not raise).
    """
    deadline = time.monotonic() + max_retry_seconds
    target_parent = target_path.parent
    target_parent.mkdir(parents=True, exist_ok=True)

    while time.monotonic() < deadline:
        try:
            staged = stage_to_tmp(content, target_path.suffix)
            os.replace(staged, target_path)
            # Verify write actually landed
            if os.stat(target_path).st_size == len(content):
                return True
            logger.warning(f"Write to {target_path} reported success but size mismatch")
        except OSError as e:
            logger.warning(f"OSError writing {target_path}: {e}")
            time.sleep(0.5)
        except Exception as e:
            logger.warning(f"Unexpected error writing {target_path}: {e}")
            time.sleep(0.5)

    # Final fallback: write to /tmp/<name>.last_good
    fallback = Path("/tmp") / f"{target_path.name}.last_good"
    try:
        fallback.write_bytes(content)
        logger.error(f"All writes to {target_path} failed. Wrote to fallback {fallback}.")
    except Exception as e:
        logger.error(f"Even /tmp fallback failed for {target_path}: {e}")
    return False


def process_single_file(file_path: Path, config: dict, state: StateManager) -> dict:
    """Process a single scanner output file end-to-end.

    Returns a stats dict. Never raises (never-fail contract).
    """
    stats = {"file": str(file_path), "vulns_parsed": 0, "tickets_generated": 0,
             "escalations_sent": 0, "errors": []}

    try:
        # Determine scanner type by extension
        if file_path.suffix == ".nessus":
            vulns = parse_nessus(file_path)
        elif file_path.suffix == ".csv":
            vulns = parse_qualys(file_path)
        else:
            stats["errors"].append(f"Unknown file type: {file_path}")
            return stats

        stats["vulns_parsed"] = len(vulns)

        for vuln in vulns:
            # Check state for idempotency (skip if already processed)
            dedupe_key = f"{vuln['scanner']}:{vuln['scan_id']}:{vuln['plugin_id']}:{vuln['asset_id']}"
            if state.has_processed(dedupe_key):
                continue

            # Map to FFIEC domain
            vuln["ffeiec_domain"] = map_cve_to_ffeiec_domain(vuln.get("cve"), vuln.get("cwe"))

            # Generate Jira ticket (always, regardless of CVSS)
            ticket = generate_jira_ticket(vuln)
            ticket_path = Path(config["jira_output_dir"]) / f"{dedupe_key.replace(':', '_')}.json"
            if safe_write_bytes(ticket_path, json.dumps(ticket, indent=2).encode()):
                stats["tickets_generated"] += 1

            # Escalate if CVSS >= threshold
            cvss = vuln.get("cvss_base", 0.0)
            if cvss >= config["cvss_escalation_threshold"]:
                email = generate_escalation_email(vuln)
                email_path = Path(config["escalation_output_dir"]) / f"{dedupe_key.replace(':', '_')}.eml"
                if safe_write_bytes(email_path, email.encode()):
                    stats["escalations_sent"] += 1

            # Mark as processed in state
            state.mark_processed(dedupe_key, vuln)

    except Exception as e:
        logger.exception(f"Error processing {file_path}")
        stats["errors"].append(str(e))

    return stats


def run_once(config: dict) -> list:
    """Run a single pass over all discovered input files."""
    state = StateManager(Path(config["state_file"]))
    all_stats = []

    nessus_files = discover_inputs(config["nessus_input_dir"])
    qualys_files = discover_inputs(config["qualys_input_dir"])
    all_files = nessus_files + qualys_files

    logger.info(f"Discovered {len(nessus_files)} Nessus + {len(qualys_files)} Qualys files")
    for file_path in all_files:
        stats = process_single_file(file_path, config, state)
        all_stats.append(stats)
        logger.info(f"Processed {file_path.name}: {stats}")

    # Flush state to disk
    state.flush()
    return all_stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Meridian Vulnerability Management Pipeline")
    parser.add_argument("--config", type=Path, default=SCRIPT_DIR / "config.ini",
                        help="Path to config.ini (YAML format)")
    parser.add_argument("--once", action="store_true",
                        help="Run a single pass and exit (useful for testing/manual runs)")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.once:
        run_once(config)
        return 0

    # Daemon mode: poll continuously
    logger.info(f"Starting daemon, polling every {config['polling_interval_seconds']}s")
    running = True

    def handle_signal(signum, frame):
        nonlocal running
        logger.info(f"Received signal {signum}, shutting down gracefully")
        running = False

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    while running:
        try:
            run_once(config)
        except Exception as e:
            logger.exception(f"Unhandled error in main loop: {e}")
        time.sleep(config["polling_interval_seconds"])

    return 0


if __name__ == "__main__":
    sys.exit(main())