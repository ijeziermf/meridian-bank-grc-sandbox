# Meridian Bank Vulnerability Management Pipeline

> Production-grade vulnerability management pipeline that ingests scanner output (Nessus / Qualys), maps CVEs to FFIEC domains, generates remediation tickets, and escalates critical findings.

## What This Demonstrates

This is a **stateful processing daemon**, not a one-shot script. It demonstrates the same operational credibility as Helix's audit log forwarder but for a different control expectation:

- **Helix audit forwarder** = satisfies HIPAA §164.312(b) Audit Controls by forwarding logs out-of-band
- **Meridian vuln pipeline** = satisfies FFIEC IT Examination Handbook (Information Security booklet) continuous vulnerability identification, classification, and remediation tracking

## Architecture

```
[Nessus/Qualys scanner output XML/CSV]
            |
            v
    [parsers/]  -->  [CVE normalization]  -->  [CVSS lookup]
            |
            v
    [mappings/]  -->  [FFIEC domain mapper YAML]  -->  [CVE-to-domain classification]
            |
            v
    [outputs/]  -->  [Jira ticket JSON]  -->  [email escalation template]
            |
            v
    [state/]  -->  [NDJSON append-only crash-recovery state]
```

## Components

| File | Purpose |
|---|---|
| `meridian_vuln_pipeline.py` | Main daemon loop with bounded retry, never-fail contract |
| `parsers/nessus_xml.py` | Parse Tenable Nessus XML output |
| `parsers/qualys_csv.py` | Parse Qualys VMDR CSV output |
| `mappings/cve_to_ffeiec.py` | Map CVE/CWE to FFIEC domain (Audit/Management/Operations/etc.) |
| `mappings/ffeiec_domains.yaml` | Authoritative mapping table (curated) |
| `outputs/jira_generator.py` | Generate Jira-formatted remediation tickets |
| `outputs/email_escalator.py` | Generate escalation email for critical CVEs (CVSS >= 9.0) |
| `state/state_manager.py` | Crash-recovery via NDJSON append-only state file |
| `com.meridian.vuln-pipeline.plist` | launchd daemon definition (auto-restart on crash) |
| `tests/test_nessus_parser.py` | pytest with sample Nessus output |
| `tests/test_qualys_parser.py` | pytest with sample Qualys output |
| `tests/test_ffeiec_mapping.py` | pytest for FFIEC domain mapping |
| `tests/sample_nessus.nessus` | Sample scanner output for tests |
| `requirements.txt` | Python deps (PyYAML, defusedxml, requests, jinja2) |

## Installation

```bash
# 1. Install Python deps
pip3 install -r requirements.txt

# 2. Configure scanner source paths (edit config.ini)
vim config.ini

# 3. Install launchd daemon
cp com.meridian.vuln-pipeline.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.meridian.vuln-pipeline.plist

# 4. Verify daemon running
launchctl list | grep meridian.vuln
tail -f /var/log/meridian-vuln-pipeline.log
```

## Configuration

`config.ini` controls:
- Scanner output paths (Nessus XML, Qualys CSV)
- Output directories (Jira JSON, email templates, state)
- Jira webhook URL (optional, for direct ticket creation)
- SMTP relay for escalation emails
- Polling interval (default 300 seconds = 5 minutes)
- CVSS threshold for escalation (default 9.0)

## Verification

```bash
# Run the test suite
python3 -m pytest tests/ -v

# Verify mappings table is loadable
python3 -c "from mappings.cve_to_ffeiec import map_cve; print(map_cve('CVE-2024-3094'))"

# Trigger a manual run (single pass)
python3 meridian_vuln_pipeline.py --once

# Check state file
tail -5 state/vuln-pipeline.ndjson
```

## Operational Properties

### Never-fail contract

The daemon satisfies the `operations/macos-apfs-clone-deadlocks` Recipe 7 never-fail contract:

1. **No module-level filesystem I/O.** All FS operations live inside `main()`.
2. **Stage to /tmp first**, atomic rename into the target.
3. **Bounded retries** by wall time (not attempt count). Default deadline: 30 seconds per operation.
4. **Final fallback to /tmp** if target write fails. Data is never lost.
5. **Verify the write actually landed** with `os.stat(target).st_size > 0`.
6. **Exit 0 unconditionally.**

This means the daemon never crashes the framework even if the filesystem is locked, the scanner is offline, or Jira is unreachable. Failures are logged and the next tick retries.

### Crash recovery

The state file `state/vuln-pipeline.ndjson` is append-only. On startup, the daemon reads the last entry to determine where to resume. This is the same pattern Helix's audit forwarder uses.

### Idempotent ticket generation

Each CVE is keyed by `(scanner, scan_id, plugin_id, asset_id)`. If the same CVE is reported in two scans, the daemon updates the existing Jira ticket rather than creating a duplicate. This is enforced by checking the state file before ticket generation.

## FFIEC Domain Mapping

The mapping table (`mappings/ffeiec_domains.yaml`) translates CVEs/CWEs into the FFIEC IT Examination Handbook domains:

- **Audit** - logging, monitoring, SIEM, log retention
- **Management** - governance, risk management, policy
- **Development and Acquisition** - SDLC, secure coding, code review
- **Operations and Maintenance** - patching, configuration, vulnerability management
- **Information Security** - access control, encryption, network security
- **Business Continuity** - BCP, DR, resilience
- **Outsourcing** - vendor, cloud, third-party

The mapping uses CVE/CWE keyword heuristics plus a curated lookup table for known critical CVEs. The mapping is auditable and reviewable.

## What This Demonstrates to a Hiring Manager

A banking ISSO/CISO who can:
- Stand up a continuous vulnerability management pipeline that satisfies FFIEC IT Examination Handbook expectations
- Map CVEs to FFIEC domains (not just CVSS scores)
- Generate remediation tickets in the bank's existing ticketing system
- Escalate critical findings to the right people
- Maintain audit-ready documentation of every remediation cycle
- Operate the daemon reliably in production (never-fail, crash recovery, idempotent)

...is someone who can run the bank's vulnerability management program end-to-end. That's the bar.

## License

MIT - Ijezie Risk Advisory portfolio artifact.