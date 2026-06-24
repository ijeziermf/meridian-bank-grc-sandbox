# meridian-bank-grc-sandbox

> A **persona spec only** for the **Meridian Bank** community bank scenario,
> intended to be ingested into the same CISO Assistant v3.18.3 Community
> Edition instance as
> [atlaspay-grc-sandbox](https://github.com/ijeziermf/atlaspay-grc-sandbox)
> and
> [helix-health-grc-sandbox](https://github.com/ijeziermf/helix-health-grc-sandbox).

## Status

**Phase 0 — persona spec authored. Ingestion not yet run.**

This repo currently contains only the persona definition. The Helix and
AtlasPay repos document the full Phase 1 ingestion pattern; Meridian will
follow the same playbook when Ifeanyi schedules it.

## Persona overview

- **Name:** Meridian Bank, National Association
- **Ticker:** NYSE: MRDN (parent: Meridian Bancshares, Inc.)
- **Industry:** Commercial banking, mid-size regional / community
- **Founded:** 1962
- **HQ:** Charlotte, NC
- **Footprint:** 240 branches across NC, SC, VA, TN
- **Scale:** ~3,200 employees, 2.4M retail + commercial customers,
  $50.2B total assets
- **Hosting model:** Hybrid (FIS-hosted core banking + on-prem data
  center + Azure AD identity + AWS digital channels)

## Regulatory landscape

| Framework | Status |
|---|---|
| FFIEC CAT (Cybersecurity Assessment Tool) | Primary federal cybersecurity framework, annual full assessment + quarterly refresh; inherent risk = High, maturity = Intermittent |
| FFIEC IT Examination Handbook | Last IT exam 2025-Q3, MRA closed 2026-Q1 |
| NYDFS 23 NYCRR Part 500 | Exempt (no NY operations), tracked as adjacent for correspondent banking exposure |
| SOX ITGC | Active since 2018 IPO, 2025 audit clean, 2026 cycle in progress |
| GLBA Safeguards Rule (16 CFR Part 314) | Program current, 2026 revision incorporated |
| PCI DSS 4.0 | ROC issued 2025-Q4 (Fiserv card services), AOC current through 2026-Q4 |
| SOC 1 Type 2 | Annual, for core banking services supporting correspondent customers |
| SOC 2 Type 2 | Not pursued (regulators prefer FFIEC over SOC 2 in banking) |

## Tech stack

| Layer | Vendor / Product |
|---|---|
| Core banking | FIS Profile |
| Trust operations | Jack Henry SilverLake |
| Card services | Fiserv |
| Wires | ACI Worldwide |
| Federal Reserve access | FedLine Advantage |
| Correspondent clearing | Pershing (BNY Mellon subsidiary) |
| Identity | Microsoft Azure AD |
| Cloud (digital channels) | AWS |
| Monitoring | Datadog |
| Compliance tooling | Vanta |

## Spec contents

`source-data/meridian_persona_spec.json` contains:

- **persona** — company, scale, geography, regulators, hosting model
- **perimeters** — 4 (FIS Profile, Jack Henry trust, ACI wires, digital channels)
- **frameworks_to_load** — 8 frameworks with URNs for CISO Assistant catalog
- **audit_scope** — annual audit calendar + cycle boundaries
- **risk_register_seed** — 12 risks (cyber + compliance + operational)
- **policy_set** — 12 policies (FFIEC-aligned)
- **tprm** — vendor tiers and sample vendors (FIS, Jack Henry, Fiserv, ACI, FedLine, AWS, Azure AD, Datadog, Vanta, Pershing)
- **ropa** — 7 categories, 15 processing activities (CIP/KYC, wires, lending, AML, OFAC, etc.)
- **bia_target** — Tier 1 critical, Tier 2 essential, Tier 3 deferrable
- **validation_flows** — 5 (wire fraud response, OFAC match resolution, third-party breach notification, catastrophic BCP, GLBA exception)
- **audit_log_forwarding** — 16 event types (wire.origination, ach.origination, atm.transaction, customer.ofac_hit, customer.sar_filed, bcp.dr_failover_test, etc.)
- **incidents_for_demo** — 1 historical (BEC on commercial loan customer, Oct 2025, $1.8M recovered)
- **key_personnel** — 9 (CEO, CIO, CISO, CRO, COO, BSA Officer, Compliance Manager, Head of Risk, Head of IT)

## Planned ingestion phases

When Ifeanyi schedules this sandbox, the same playbook as Helix will apply:

### Phase 1 — Core portfolio
- Create Meridian Bank folder
- Load the 8 frameworks above (FFIEC CAT, FFIEC IT Exam Handbook, NYDFS 500, SOX ITGC, GLBA Safeguards, FFIEC BCP/DR, PCI DSS 4.0, NIST CSF 2.0)
- Create 4 perimeters (FIS Profile, Jack Henry trust, ACI wires, digital channels)
- Create 5x5 banking-sector risk matrix
- Create risk assessment
- Create 12 risk scenarios with inherent/current/residual
- Create 12 policies
- Create 10 vendors with vendor contracts
- Create 15 ROPA processing activities
- Create 5 validation flows

### Phase 2 — Wire-specific integrations
- Wire transfer authentication controls (FFIEC-required)
- ACH fraud detection
- ATM jackpotting tabletop exercise (using the historical incident pattern)

### Phase 3 — Audit log forwarding
- Same forwarder pattern as Helix, but configured for bank events:
  wire.origination, ach.origination, atm.transaction, customer.ofac_hit,
  customer.sar_filed, bcp.dr_failover_test
- Forward to Splunk HEC (banking-sector standard, not Datadog)

## Repository structure

```
meridian-bank-grc-sandbox/
├── README.md                                ← you are here
└── source-data/
    └── meridian_persona_spec.json           ← full persona spec (20 KB, 13 sections)
```

## Reference: how Helix was done

For the full ingestion pattern that Meridian will follow, see the sibling
[helix-health-grc-sandbox](https://github.com/ijeziermf/helix-health-grc-sandbox) repo:

- `scripts/ingest_helix.py` — main Phase 1 ingestion (25 KB)
- `scripts/ingest_helix_phase1b.py` — ROPA + validation flows
- `scripts/risk_matrix_and_assessment_create.py` — ORM helper for matrix + assessment
- `ops/audit-forwarder/helix_audit_forwarder.py` — audit log forwarder with 4 pluggable SIEM sinks
- `deliverables/Helix_Health_Portfolio_v2.pdf` — 8-page portfolio PDF

The Meridian equivalents will be adapted for the bank sector: replace
HIPAA controls with FFIEC/SOX/GLBA, replace Datadog with Splunk HEC,
replace provider-portal contracts with correspondent banking contracts.

## Privacy

- No real PII anywhere in this repo
- Meridian Bank is a **simulated community bank persona** with realistic
  but fictional regulators, vendors, and historical incidents
- All credentials are local-only

## License

MIT — same as the related AtlasPay and Helix repos.