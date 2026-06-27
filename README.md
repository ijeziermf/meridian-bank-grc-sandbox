# Meridian Bank FFIEC + GLBA + SOX GRC Engagement

> FFIEC Cybersecurity Assessment Tool pre-assessment, Gramm-Leach-Bliley Act (GLBA) Safeguards program review, and Sarbanes-Oxley (SOX) IT General Controls posture for a publicly traded mid-size community bank. 8 stakeholder-ready PDFs plus a production-grade vulnerability management pipeline.

---

## At a Glance

| Dimension | Value |
|---|---|
| Persona | Meridian Bank, N.A. (NYSE: MRDN) |
| Industry | Commercial Banking, mid-size regional community bank |
| Total Assets | $50.2 billion |
| Employees | 3,200 (12 FTE security, 28 FTE compliance, 180 FTE engineering) |
| Customers | 2.4 million retail and commercial |
| Branches | 240 across NC, SC, VA, TN |
| Primary Federal Regulator | Office of the Comptroller of the Currency (OCC) |
| Hosting | Hybrid: FIS-hosted core banking (Profile platform), on-prem data center Charlotte NC, Azure AD for identity, AWS for digital channels |
| Frameworks in Scope | FFIEC CAT, FFIEC IT Examination Handbook, GLBA Safeguards Rule (16 CFR Part 314), SOX ITGC (PCAOB Section 404), PCI DSS 4.0 ROC, NYDFS 23 NYCRR 500 (adjacent) |
| Last IT Exam | 2025-Q3, six MRAs all closed 2026-Q1 |
| Deliverables | 8 stakeholder-ready PDFs + 1 production-grade vulnerability management pipeline + 7 evidence-quality visuals |
| Audience | OCC examiners, FDIC, state banking regulators, PCAOB-registered SOX auditor, Board Risk Committee, CISO, CIO, CRO |
| Industry Relevance | Mid-size regional banks ($10B to $100B in assets), publicly traded community banks, hybrid-hosting banking models, Bank Secrecy Act (BSA) programs |

## What This Demonstrates

A banking ISSO/CISO who can:

1. Prepare examiner-facing artifacts (FFIEC CAT, GLBA Safeguards Rule gap assessment, SOX ITGC posture) for a publicly traded community bank with $50B in assets, prior MRA history, and active SOX audit cycle.
2. Map controls across multiple overlapping frameworks (FFIEC CAT, GLBA, SOX, PCI DSS, NYDFS adjacent) and operate them efficiently as a single program rather than parallel compliance tracks.
3. Run a 30-vendor Third Party Risk Management (TPRM) program including critical vendor concentration analysis (FIS, Fiserv, ACI, Jack Henry at 60% of vendor spend) and fourth-party (subprocessor) risk visibility.
4. Operate a Business Continuity / Disaster Recovery (BCP/DR) program with tiered Recovery Time Objectives (RTO 1-72 hours) and Recovery Point Objectives (RPO 0-24 hours) calibrated to regulatory and settlement obligations.
5. Build and operate a production-grade vulnerability management pipeline (Nessus + Qualys ingestion, CVE to FFIEC domain mapping, Jira ticket generation, critical-CVE escalation) that satisfies FFIEC IT Examination Handbook continuous vulnerability identification expectations.
6. Communicate to the Board Risk Committee in writing and in person, with the discipline of quarterly cadence, top-5 risk prioritization, and the GLBA 314.4(e) annual written report requirement.
7. Track MRA remediation lifecycle end-to-end (from 2025-Q3 exam to 2026-Q1 closure) with forward-looking items, status reporting cadence, and examiner communication protocol.
8. Design a Breach Notification Playbook that navigates GLBA Interagency Guidance (30-day customer notification), state banking notification windows (NC, SC, VA, TN), NYDFS 23 NYCRR 500 72-hour (adjacent), and contractual notification obligations in MSAs.

## Deliverables

### Stakeholder-Facing PDFs (8 files, IJEZIE RISK ADVISORY branded)

| Deliverable | Purpose | Pages | Audience |
|---|---|---|---|
| [FFIEC CAT Maturity Pre-Assessment](deliverables/ffiec-cat-pre-assessment.pdf) | 5 domains x 5 maturity levels with current state (Intermittent) and target state (Intermediate). Inherent risk profile: High | 6 | OCC examiner, board Risk Committee, CISO |
| [GLBA Safeguards Rule Gap Assessment](deliverables/glba-safeguards-gap.pdf) | 15 substantive controls against 16 CFR Part 314. 12 Met, 3 Partial, 0 Missing. Includes 2026 revision coverage | 5 | CISO, CTO, examiner |
| [SOX ITGC Posture Review](deliverables/sox-itgc-posture.pdf) | 4 ITGC domains x 27 controls. No material weakness identified. PCAOB 2026 heightened focus areas covered | 7 | CFO, CIO, internal audit, PCAOB auditor |
| [BCP/DR Readiness Package](deliverables/bcp-dr-readiness.pdf) | Business Impact Analysis (BIA) with 3 tier RTO/RPO, recovery procedures for FIS Profile / ACI / FedLine, regional event scenarios | 5 | COO, IT operations, examiner |
| [Vendor Risk + MSA Inventory](deliverables/tprm-msa-inventory.pdf) | 30 vendors across 5 tiers. Critical vendor concentration (FIS + Fiserv + ACI + Jack Henry = 60% of vendor spend). Fourth-party risk coverage | 7 | Head of TPRM, procurement, examiner |
| [MRA Remediation Tracker](deliverables/mra-remediation-tracker.pdf) | 6 MRAs from 2025-Q3 exam (closed 2026-Q1) + 3 forward-looking open items with board reporting cadence | 5 | CISO, board Risk Committee |
| [Breach Notification Playbook](deliverables/breach-notification-playbook.pdf) | GLBA 30-day + state banking + NYDFS 72-hour (adjacent) + contractual notification. Worked example: MB-INC-2025-001 BEC ($2.3M wire, $1.8M recovered) | 6 | CISO, Legal, on-call team |
| [Board + Risk Committee Briefing](deliverables/board-risk-committee-briefing.pdf) | Quarterly briefing with cyber risk appetite, top 5 risks (INHERENT/RESIDUAL), FFIEC CAT maturity status, MRA status, GLBA 314.4(e) board reporting, SOX opinion | 5 | Board, Risk Committee, CEO |

**Total: 47 pages of examiner-defensible banking documentation across 8 stakeholder-ready PDFs.**

### Operational Artifact (Production-Grade Code)

[Vulnerability Management Pipeline](lab/ops/vuln-mgmt-pipeline/) at `lab/ops/vuln-mgmt-pipeline/`:
- `meridian_vuln_pipeline.py` - main daemon (stateful processing, never-fail contract, crash recovery)
- `parsers/` - Nessus XML parser + Qualys CSV parser
- `mappings/` - CVE to FFIEC domain mapper (curated lookup + keyword heuristics)
- `outputs/` - Jira ticket generator + email escalation template for critical CVEs (CVSS >= 9.0)
- `state/` - crash-recovery state manager (NDJSON append-only, idempotent)
- `com.meridian.vuln-pipeline.plist` - launchd daemon definition (auto-restart on crash)
- `README.md` - installation, configuration, verification
- `requirements.txt` - Python deps (PyYAML, defusedxml, requests, jinja2)

This pipeline satisfies the FFIEC IT Examination Handbook Information Security booklet expectation of continuous vulnerability identification, classification, and remediation tracking. Same operational credibility pattern as Helix's audit log forwarder, applied to a different control expectation.

### Evidence-Quality Visuals (7 PNGs in `assets/images/`)

Generated for the v3 stakeholder-facing PDFs (no UI screenshots, no platform captures - these show the analyst's output, not the platform's UI):

| Visual | What It Shows |
|---|---|
| `meridian-operational-risk-heatmap.png` | 5x5 OCC Operational Risk categories with 12 MB-R-01 through MB-R-12 risks plotted INHERENT vs RESIDUAL side-by-side |
| `meridian-ffiec-cat-maturity.png` | 5 FFIEC CAT domains with Current (Intermittent) vs Target (Intermediate+) maturity bars |
| `meridian-glba-coverage.png` | 15 GLBA Safeguards Rule controls stacked by Met/Partial/Missing status |
| `meridian-multi-framework-cross-walk.png` | 12 Meridian controls x 3 frameworks (FFIEC CAT + GLBA 314.4 + SOX ITGC) |
| `meridian-bcp-rto-rpo-timeline.png` | 10 critical systems x RTO/RPO by Tier 1 / Tier 2 / Tier 3 |
| `meridian-vendor-concentration.png` | 30 vendors across 5 tiers + top 8 critical vendors by annual contract value (60% spend concentration) |
| `meridian-mra-tracker-gantt.png` | 6 closed MRAs + 3 forward-looking open items on a 22-month timeline |

All visuals:
- Brand compliant (IJEZIE RISK ADVISORY footer, no emojis, no em-dashes)
- LAB-SYNTHETIC tag on each
- Verified by visual QA against specific criteria

## Risk Register Summary

| ID | Title | Inherent | Residual | Owner |
|---|---|---|---|---|
| MB-R-01 | ATM jackpotting at regional branch fleet | 16 | 9 | Head of Physical Security / CISO |
| MB-R-02 | Wire fraud via business email compromise (BEC) targeting commercial customers | 25 | 12 | BSA Officer / CISO |
| MB-R-03 | ACH fraud (origination debiting or returns manipulation) | 20 | 12 | BSA Officer |
| MB-R-04 | Synthetic identity lending losses (auto loan and unsecured consumer) | 16 | 9 | Chief Credit Officer |
| MB-R-05 | Correspondent banking AML/KYC gap (Pershing or downstream foreign bank) | 20 | 12 | BSA Officer |
| MB-R-06 | Core banking vendor concentration on FIS Profile (single point of failure) | 16 | 16 | CIO |
| MB-R-07 | Ransomware on FIS-hosted core banking host (managed environment, shared responsibility) | 20 | 12 | CISO |
| MB-R-08 | Third-party core banking breach at FIS exposing customer NPI | 25 | 16 | CISO |
| MB-R-09 | Destructive malware / wiper attack on internal branch network | 16 | 9 | CISO |
| MB-R-10 | Insider trading via material non-public information (MNPI) accessed through trust operations | 12 | 6 | CCO / Head of Wealth |
| MB-R-11 | Critical vendor SLA breach during quarter-end close (FIS Profile or ACI) | 12 | 9 | CIO |
| MB-R-12 | Disaster recovery failure - inability to fail over from Charlotte primary data center during regional event | 16 | 9 | Head of Business Continuity |

**Total risks: 12. Inherent sum: 196. Residual sum: 130. Net reduction: 66 (34%).**

Note that MB-R-06 (FIS concentration) and MB-R-08 (third-party breach at FIS) residuals cannot be reduced below inherent through Meridian controls alone - these are addressed via vendor contractual protections, SLAs, and exit planning rather than internal control investment.

## Vendor Risk Snapshot (30 Vendors)

| Tier | Count | Examples |
|---|---|---|
| Critical (OCC-supervised service provider) | 9 | FIS (Profile core banking), Jack Henry (SilverLake trust), Fiserv (card services), ACI Worldwide (wires), Pershing (correspondent) |
| Critical (no BAA-equivalent) | 1 | Federal Reserve FedLine Advantage (governed by Operating Circular 5) |
| High (Cloud/Infrastructure) | 11 | AWS, Azure AD, Datadog, Splunk Cloud |
| Medium (Operational) | 7 | Vanta (internal efficiency), Workday, Coupa |
| Low (Internal Tools) | 2 | Office productivity, HR |

**Critical vendor concentration: 4 vendors (FIS, Fiserv, ACI, Jack Henry) = 60% of vendor spend.**

## Banking-Specific Dimensions (Different from AtlasPay and Helix)

### 1. Examiner-facing, not auditor-facing

The deliverables are designed for OCC examiners, not PCAOB auditors. This is a fundamentally different communication style:
- Auditors want sampling, evidence, control assertions
- Examiners want maturity narratives, threat-informed risk assessments, comprehensive coverage
- The FFIEC CAT maturity assessment (Current vs Target by domain) is the artifact examiners expect to see in the opening meeting of an IT exam

### 2. OCC Operational Risk Categories, not arbitrary risk buckets

The Risk Register uses the OCC Operational Risk taxonomy (Internal Fraud, External Fraud, Employment Practices, Clients/Business Practices, Business Disruption, Damage to Physical Assets, Execution/Delivery/Process Management) as the risk-scenario framework. This is what examiners look for, not generic risk categories.

### 3. MRA lifecycle management

MRAs (Matters Requiring Attention) are the OCC's primary supervisory tool. Tracking MRA closure, documenting remediation evidence, and reporting progress to the Board Risk Committee is a recurring cycle that banking ISSOs live with. The MRA Remediation Tracker is the artifact that demonstrates this discipline.

### 4. Correspondent banking and wire transfer risk

Wire fraud via BEC targeting commercial customers is the #1 loss event for community banks. The MB-INC-2025-001 worked example ($2.3M wire attempt, $1.8M recovered) demonstrates the playbook for high-value wire controls (call-back verification, beneficiary bank change controls, dual approval).

### 5. FFIEC CAT vs SOX ITGC vs GLBA Safeguards Rule

Three overlapping frameworks that operate in genuinely different regulatory registers:
- FFIEC CAT = voluntary maturity model used by examiners as reference
- GLBA Safeguards Rule = mandatory under 16 CFR Part 314 (FTC) and interagency guidance (OCC/FDIC/Fed)
- SOX ITGC = mandatory for public companies; PCAOB-audited annually

The multi-framework cross-walk (12 controls x 3 frameworks) shows how single-control-multiple-framework satisfaction works.

### 6. TPRM with fourth-party visibility

Third Party Risk Management (TPRM) at a $50B bank includes not just direct vendor risk but fourth-party (subprocessor) risk: who does FIS sub-contract to? Who does ACI sub-contract to? Fourth-party visibility is the discipline that distinguishes a mature TPRM program from a checkbox one.

### 7. Breach notification under GLBA + state + contract

Unlike AtlasPay (72-hour GDPR + contract) or Helix (HIPAA 60-day + state overlays FL/NY/CA), the Meridian breach notification regime operates under:
- GLBA Interagency Guidance on Response Programs (2005) - customer notification within 30 days if misuse is reasonably possible
- State banking notification - varies by state (NC, SC, VA, TN)
- NYDFS 23 NYCRR 500 - 72-hour notification (adjacent; Meridian is exempt because no NY operations but tracks it)
- Contractual - vendor MSAs may have shorter windows

The Breach Notification Playbook navigates all four regimes plus federal regulator coordination (the unwritten norm is to call the primary federal regulator within 24-48 hours of a significant incident).

## Key Findings

1. **MB-R-08 (third-party breach at FIS) is the highest residual risk** at score 16. Meridian cannot reduce this through internal controls - the mitigation is contractual protections in the FIS MSA, fourth-party visibility into FIS subprocessors, and exit planning for the 24-month replacement horizon if FIS is breached.

2. **MB-R-06 (FIS vendor concentration) is structurally irreducible** at residual 16. There is no commercially viable alternative to FIS Profile in Meridian's timeframe. The mitigation is long-term contract renewal visibility, joint DR exercise participation, and the documented exit playbook.

3. **FFIEC CAT maturity is Intermittent across all 5 domains**, target Intermediate. Closing the gap requires investment in independent assessment, threat hunting capability, continuous vulnerability management, branch network segmentation, fourth-party risk program, and tabletop cadence improvements. Estimated investment: $770K capex + $540K annually.

4. **GLBA Safeguards Rule 2026 revision gaps are addressable** in 2026-Q3-Q4: SSDLC standards extension to vendor development, VPN MFA migration completion, endpoint DLP deployment, cloud DAP deployment, GLBA 314.4(e) annual written report to board.

5. **SOX 2026 audit cycle is on track.** No material weakness identified. The heightened PCAOB focus areas (third-party ITGCs, privileged access, change management for digital banking) have mitigation workpapers in place.

6. **MRA lifecycle discipline is mature.** The 6 MRAs from 2025-Q3 were all closed in the 2026-Q1 remediation cycle. The forward-looking tracker addresses continuous vulnerability management, branch network segmentation, and fourth-party risk visibility.

7. **Breach Notification Playbook worked example: MB-INC-2025-001 BEC** demonstrated effective controls (38-minute detection via call-back verification, $1.8M recovered via correspondent bank and Federal Reserve recall window). Lessons learned drove procedural changes: lowered high-value wire dollar threshold from $500K to $250K for mandatory call-back, dual approval for beneficiary bank changes within 14 days, quarterly BEC tabletop with top 50 commercial customers.

8. **Critical vendor concentration is the structural risk.** 4 vendors at 60% of vendor spend. The mitigation is not diversification (no commercially viable alternatives) but contractual protections, joint DR exercises, and exit playbooks.

## What This Demonstrates for a vCISO Engagement

This engagement demonstrates the vCISO discipline of working a regulator's framework backward from the examiner's perspective, not from the auditor's perspective. The FFIEC CAT is voluntary but examiners use it as the primary lens; producing this artifact before the examiner arrives (rather than after they ask) is the difference between a clean exam cycle and an MRA.

The 8 deliverables + 1 operational artifact demonstrate:

- **Examiner readiness** - FFIEC CAT pre-assessment, MRA remediation tracker, breach notification playbook
- **Auditor readiness** - SOX ITGC posture, GLBA Safeguards gap assessment
- **Board communication** - quarterly cadence, written reporting per GLBA 314.4(e), top-5 risk prioritization
- **Operational credibility** - production-grade vulnerability management pipeline
- **Cross-framework discipline** - single-control-multiple-framework mapping across 3 overlapping banking frameworks
- **TPRM maturity** - 30 vendors, fourth-party visibility, critical concentration analysis

## Process and Methodology

This engagement used the following workflow:

1. **Persona specification** - read `lab/source-data/meridian_persona_spec.json` for scope, risk count, vendor count, framework stack
2. **Source markdown generation** - 8 deliverable source markdowns in `deliverables/source-data/` per the Ijezie Risk Advisory template
3. **Evidence-quality visual generation** - 7 PNGs generated with matplotlib per the `grc-evidence-visual-pipeline` skill recipe, verified by visual QA
4. **PDF generation with embedded visuals** - per the IJZ PDF template skill, dynamic cover/title metadata per doc type, dynamic page headers, embedded visuals via `![Figure N](../../assets/images/...)` syntax
5. **Operational artifact coding** - vulnerability management pipeline in `lab/ops/vuln-mgmt-pipeline/` with production-grade code quality (type hints, docstrings, never-fail contract, crash recovery)
6. **Brand compliance sweep** - 0 brand contamination, 0 em-dashes, 0 emojis across all deliverables
7. **Voice rules** - past tense for completed work, no first person, expanded acronyms on first use
8. **GitHub publish** - via Recipe 10 (fresh clone to `/tmp` to work around macOS APFS compressed-dataless clones)

## Repository Structure

```
meridian-bank-grc-sandbox/
  README.md                                          (this file)
  LICENSE
  lab/
    source-data/
      meridian_persona_spec.json                     (engagement scope definition)
    ops/
      vuln-mgmt-pipeline/                           (production-grade operational artifact)
        meridian_vuln_pipeline.py                   (main daemon)
        parsers/nessus_xml.py                       (Tenable Nessus XML parser)
        parsers/qualys_csv.py                       (Qualys VMDR CSV parser)
        mappings/cve_to_ffeiec.py                   (CVE-to-FFIEC domain mapper)
        mappings/ffeiec_domains.yaml                (curated mapping table)
        outputs/jira_generator.py                   (Jira ticket generator)
        outputs/email_escalator.py                  (critical CVE escalation template)
        state/state_manager.py                      (NDJSON append-only state)
        com.meridian.vuln-pipeline.plist            (launchd daemon)
        config.ini                                  (configuration)
        requirements.txt                            (Python deps)
        README.md                                   (operational artifact README)
  deliverables/
    ffiec-cat-pre-assessment.pdf                    (FFIEC CAT)
    glba-safeguards-gap.pdf                         (GLBA Safeguards Rule)
    sox-itgc-posture.pdf                            (SOX ITGC)
    bcp-dr-readiness.pdf                            (BCP/DR)
    tprm-msa-inventory.pdf                          (TPRM)
    mra-remediation-tracker.pdf                     (MRA Tracker)
    breach-notification-playbook.pdf                (Breach Notification)
    board-risk-committee-briefing.pdf               (Board Briefing)
    source-data/
      fffiec-cat-pre-assessment-2026-06-27.md
      glba-safeguards-gap-2026-06-27.md
      sox-itgc-posture-2026-06-27.md
      bcp-dr-readiness-2026-06-27.md
      tprm-msa-inventory-2026-06-27.md
      mra-remediation-tracker-2026-06-27.md
      breach-notification-playbook-2026-06-27.md
      board-risk-committee-briefing-2026-06-27.md
      assets/images/                               (visual sources for PDF embedding)
  assets/
    images/
      meridian-operational-risk-heatmap.png
      meridian-ffiec-cat-maturity.png
      meridian-glba-coverage.png
      meridian-multi-framework-cross-walk.png
      meridian-bcp-rto-rpo-timeline.png
      meridian-vendor-concentration.png
      meridian-mra-tracker-gantt.png
```

## Tools and Frameworks

- **FFIEC Cybersecurity Assessment Tool (CAT)** - primary federal cybersecurity framework
- **FFIEC IT Examination Handbook** - reference handbook covering IT audit, BCP, development/acquisition, infosec, management, operations, outsourcing, retail payments, wholesale payments, supervision of technology service providers
- **GLBA Safeguards Rule** - 16 CFR Part 314 (FTC) and interagency guidance (OCC/FDIC/Fed)
- **SOX Section 404** - PCAOB-registered auditor annual cycle
- **PCI DSS 4.0** - annual Report on Compliance (ROC) for Fiserv-scope card services
- **NIST CSF 2.0** - reference framework
- **CISO Assistant Community Edition v3.18.3** - GRC platform (engagement-level, not committed to this repo)
- **matplotlib** - chart generation
- **PyYAML + defusedxml + requests + jinja2** - vulnerability pipeline dependencies

## Related Projects

- [AtlasPay](https://github.com/ijeziermf/atlaspay-grc-sandbox) - SOC 2 Type 1 Readiness for a FinTech (Y Combinator W23 portfolio company)
- [Helix Health](https://github.com/ijeziermf/helix-health-grc-sandbox) - HIPAA + SOC 2 + HITRUST + HDS readiness for a HealthTech

Together, these three projects demonstrate breadth across FinTech (SOC 2), HealthTech (HIPAA), and Banking (FFIEC + GLBA + SOX), with operational credibility demonstrated by both Helix's audit log forwarder and Meridian's vulnerability management pipeline.

## License

MIT - Ijezie Risk Advisory portfolio artifact.

All artifacts in this repository are LAB-SYNTHETIC. No real bank data. No real customer data. No real vendor data. The persona (Meridian Bank, N.A.) is fictional; the framework citations and control mappings are real.