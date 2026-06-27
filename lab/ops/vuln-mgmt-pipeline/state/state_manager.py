"""
Crash-recovery state manager using NDJSON append-only file.

Same pattern as Helix's audit log forwarder: read on startup to determine
where to resume, append on every successful processing, periodic flush.

The state file is the source of truth for "which CVEs have already been
processed" (idempotency) and "where to resume after a crash".
"""

import json
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class StateManager:
    """NDJSON append-only state manager with idempotency tracking."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.processed: Dict[str, Dict[str, Any]] = {}
        self._dirty = False
        self._load()

    def _load(self) -> None:
        """Load existing state from NDJSON file."""
        if not self.state_file.exists():
            logger.info(f"State file {self.state_file} does not exist yet; starting fresh")
            return
        try:
            with open(self.state_file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        dedupe_key = record.get("dedupe_key")
                        if dedupe_key:
                            self.processed[dedupe_key] = record
                    except json.JSONDecodeError:
                        continue
            logger.info(f"Loaded {len(self.processed)} processed records from {self.state_file}")
        except OSError as e:
            logger.warning(f"Failed to load state file {self.state_file}: {e}")

    def has_processed(self, dedupe_key: str) -> bool:
        """Return True if this dedupe_key has already been processed."""
        return dedupe_key in self.processed

    def mark_processed(self, dedupe_key: str, vuln: Dict[str, Any]) -> None:
        """Mark a vulnerability as processed. Appends to in-memory state."""
        self.processed[dedupe_key] = {
            "dedupe_key": dedupe_key,
            "cve": vuln.get("cve"),
            "cvss_base": vuln.get("cvss_base"),
            "ffeiec_domain": vuln.get("ffeiec_domain"),
            "host": vuln.get("host"),
            "scanner": vuln.get("scanner"),
            "scan_id": vuln.get("scan_id"),
        }
        self._dirty = True

    def flush(self) -> None:
        """Flush in-memory state to disk. Stage to /tmp, atomic-rename.

        Never-fail contract: returns silently on failure.
        """
        if not self._dirty:
            return
        try:
            # Stage to /tmp
            fd, tmp_path = tempfile.mkstemp(suffix=".ndjson", dir="/tmp")
            try:
                for record in self.processed.values():
                    line = json.dumps(record) + "\n"
                    os.write(fd, line.encode())
            finally:
                os.close(fd)

            # Atomic rename
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            os.replace(tmp_path, self.state_file)

            # Verify write actually landed
            if os.stat(self.state_file).st_size > 0:
                self._dirty = False
                logger.info(f"Flushed {len(self.processed)} records to {self.state_file}")
            else:
                logger.error(f"Flush to {self.state_file} reported success but size is 0")
        except Exception as e:
            logger.error(f"Failed to flush state: {e}")
            # Final fallback: leave _dirty=True so next flush retries