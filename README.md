# Meridian Bank FFIEC + GLBA + SOX GRC Engagement Design

> **FFIEC Cybersecurity Assessment Tool (CAT) pre-assessment, Gramm-Leach-Bliley Act (GLBA) Safeguards program review, and Sarbanes-Oxley (SOX) IT General Controls (ITGC) posture for a publicly traded mid-size community bank, complete with framework mapping, perimeter design, and GRC platform readiness.**

---

## What This Demonstrates

| Capability | Details |
|---|---|
| **Engagement Type** | FFIEC CAT pre-assessment + GLBA Safeguards program review + SOX ITGC posture assessment for a publicly traded community bank |
| **Methodology** | Framework mapping across 8 regulatory frameworks, hybrid-hosting perimeter design, quantitative risk scoring |
| **Deliverables** | Engagement scope, 4 perimeters, 8 frameworks mapped, 12 pre-identified risk scenarios, 12 FFIEC-aligned policies, 5 validation flows, 1 closed incident |
| **Stakeholder Focus** | Office of the Comptroller of the Currency (OCC) examiners, Federal Deposit Insurance Corporation (FDIC), state banking regulators, PCAOB-registered SOX auditor, board audit committee |
| **Industry Relevance** | Mid-size regional banks ($10B to $100B in assets), publicly traded community banks, hybrid-hosting banking models, Bank Secrecy Act (BSA) programs |

---

## Overview

Meridian Bank, N.A. is a 3,200-employee community bank holding company chartered in 1962 and headquartered in Charlotte, North Carolina. The holding company (Meridian Bancshares, Inc., NYSE: MRDN) trades publicly on the New York Stock Exchange since the 2018 initial public offering. With 240 branches across North Carolina, South Carolina, Virginia, and Tennessee, $50.2 billion in total assets, and 2.4 million retail and commercial customers, Meridian sits in the segment where FFIEC scrutiny is sharpest: too large to operate as a community bank, too small to absorb a major regulatory enforcement action.

This engagement scoped the vCISO work needed to prepare Meridian for its 2026 OCC IT examination cycle, refresh the GLBA Safeguards program under the 2026 revisions, and complete the in-progress 2026 SOX ITGC audit. The framework landscape is dense and overlapping: FFIEC CAT as the primary regulator-driven assessment, FFIEC IT Examination Handbook as the day-to-day supervision lens, SOX ITGC for the PCAOB-registered auditor's annual cycle, GLBA Safeguards Rule for customer Nonpublic Personal Information (NPI), and PCI DSS 4.0 for the Fiserv-scope card services platform. The deliverable captured in this repository is the **engagement design** — the persona specification, perimeter scoping, framework mapping, risk register seed, policy set, validation flows, and incident analysis that a vCISO would produce in Phase 0 before a single record is loaded into the GRC platform.

Mid-engagement, the team migrated the underlying platform from an open-source GRC tool to CISO Assistant Community Edition v3.18.3 to gain API coverage, framework library depth, and audit-log forwarding suitable for FFIEC IT Examination Handbook retention. That tooling decision is documented in the lab/ folder and is the kind of mid-engagement platform swap that real consulting work requires.

This repository is **Phase 0 of the engagement**. Phase 1 — ingesting the persona spec into the live CISO Assistant instance, populating the 12 risk scenarios with inherent and residual scoring, building the 12-policy library with framework crosswalks, and standing up the audit-log forwarder to Datadog and Splunk Cloud — begins when the engagement starts.

---

## Deliverables

| Artifact | Purpose | Audience |
|---|---|---|
| **Engagement Scope** | Frame the vCISO work against FFIEC + GLBA + SOX for a hybrid-hosting community bank | OCC examiners, board audit committee, CRO |
| **Persona Specification** | Authoritative source of truth for org structure, perimeters, frameworks, risks, policies, vendors, ROPA, validation flows, incidents | Internal consulting team, GRC platform engineers |
| **4 Perimeters** | FIS Profile core banking, Jack Henry trust operations, ACI wire processing, digital banking channels | CISO, CIO, vendor management |
| **8 Frameworks Mapped** | FFIEC CAT, FFIEC IT Exam Handbook, NYDFS 23 NYCRR 500 (adjacent), SOX ITGC, GLBA Safeguards, FFIEC BCP/DR, PCI DSS 4.0, NIST CSF 2.0 | Compliance, audit, regulators |
| **12 Risk Scenarios** | Pre-identified risk register covering wire fraud, ATM jackpotting, vendor concentration, ransomware, BCP failure | Board audit committee, CRO |
| **12 FFIEC-Aligned Policies** | Information Security Program, GLBA Safeguards, Wire Transfer Authentication, BCP/DR, Incident Response, CIP, AML/BSA, OFAC, Records Retention, Training | Operations, compliance, auditors |
| **5 Validation Flows** | Wire fraud response, OFAC match resolution, third-party breach notification, catastrophic BCP activation, GLBA exception | Risk owners, executives |
| **30 Vendors (tiered)** | 9 critical, 11 high, 7 medium, 2 low; Federal Reserve as critical-no-BAA-equivalent | Vendor Management Officer, OCC examiners |
| **15 ROPA Processing Activities** | GLBA Safeguards + state breach notification + CFPB Regulation P coverage | Privacy, legal, compliance |
| **1 Closed Incident** | October 2025 BEC attempt against commercial loan customer, $1.8M recovered | Board, customers, regulators |

---

## Key Features

- ✅ **FFIEC CAT inherent risk profile = High, maturity profile = Intermittent across all five domains**, with full annual re-assessment and quarterly refresh
- ✅ **GLBA Safeguards Rule 2026 revision incorporated** into the program design and policy set
- ✅ **SOX ITGC scope identified** for FIS Profile core banking, ACI wire processing, and Fiserv card services (in-scope since IPO 2018, 2025 audit clean)
- ✅ **PCI DSS 4.0 Report on Compliance (ROC) issued 2025-Q4** for Fiserv-scope card services, Attestation of Compliance (AOC) current through 2026-Q4
- ✅ **Hybrid hosting model mapped** to four perimeters: FIS-hosted core, on-premises Charlotte data center, Azure Active Directory for identity, Amazon Web Services for digital channels
- ✅ **Correspondent banking exposure** addressed through Pershing and downstream foreign bank AML/KYC controls (NYDFS 23 NYCRR Part 500 tracked as adjacent framework despite no New York operations)

---

## Engagement Scope: Perimeters

The engagement is structured around four operational perimeters, each with distinct threat models, vendor dependencies, and regulatory anchors.

```
1. FIS Profile Core Banking System (Tier 1)
   └─→ Hosted core banking, deposit accounts, loans, general ledger
   └─→ FIS-supervised service provider, FFIEC IT Handbook Outsourcing Booklet
   └─→ OCC primary exam scope, SOX ITGC in-scope

2. Jack Henry SilverLake Wealth Management and Trust Operations (Tier 2)
   └─→ Fiduciary accounts, wealth management customer records
   └─→ Jack Henry-supervised service provider
   └─→ FFIEC-supervised, trust examinations

3. Wire Transfer and Correspondent Banking (Tier 1)
   └─→ ACI Worldwide Posttrade/Wire, FedLine Advantage
   └─→ Federal Reserve-supervised, no BAA-equivalent
   └─→ SOX ITGC in-scope, BSA/AML transaction monitoring

4. Digital Banking Channels (Tier 2)
   └─→ Customer-facing web and mobile, Zelle P2P, online bill pay
   └─→ Azure AD for identity, AWS for hosting
   └─→ FFIEC-supervised, multifactor authentication requirements
```

---

## Pre-Identified Risk Scenarios

The Phase 0 risk register seeds twelve scenarios, scored on a 5x5 quantitative matrix with inherent and residual tracking. The seed identifies scenarios a vCISO would expect to scope on day one; Phase 1 ingestion expands each with control mapping, treatment plans, and residual scoring.

| Risk ID | Category | Description | Inherent | Regulatory Anchor |
|---|---|---|---|---|
| **MB-R-01** | Physical Security | ATM jackpotting at regional branch fleet | 16 (High) | FFIEC IT Examination Handbook |
| **MB-R-02** | Wire Fraud | Business email compromise (BEC) on commercial wire initiation | 25 (Very High) | FFIEC Wholesale Payments Booklet |
| **MB-R-03** | Payments | ACH origination debiting or returns manipulation | 20 (High) | FFIEC Retail Payments Booklet |
| **MB-R-04** | Credit | Synthetic identity lending losses (auto loan, unsecured consumer) | 16 (High) | FFIEC Lending Booklet |
| **MB-R-05** | BSA/AML | Correspondent banking AML/KYC gap (Pershing or downstream foreign bank) | 20 (High) | FFIEC BSA/AML Examination Manual |
| **MB-R-06** | Vendor Concentration | Single point of failure on FIS Profile core banking | 16 (High) | FFIEC IT Handbook Outsourcing Booklet |
| **MB-R-07** | Ransomware | Ransomware on FIS-hosted core banking host (managed environment, shared responsibility) | 20 (High) | FFIEC CAT Cybersecurity Controls |
| **MB-R-08** | Third-Party Breach | Third-party core banking breach at FIS exposing customer NPI | 25 (Very High) | GLBA Safeguards Rule, state breach notification |
| **MB-R-09** | Destructive Malware | Wiper attack on internal branch network | 16 (High) | FFIEC CAT Cybersecurity Controls |
| **MB-R-10** | Insider Trading | Material non-public information (MNPI) accessed through trust operations | 12 (Medium) | SEC, FFIEC fiduciary supervision |
| **MB-R-11** | Vendor SLA | Critical vendor SLA breach during quarter-end close (FIS Profile or ACI) | 12 (Medium) | FFIEC IT Handbook Outsourcing Booklet |
| **MB-R-12** | BCP/DR | Inability to fail over from Charlotte primary data center during regional event | 16 (High) | FFIEC BCP/DR Handbook |

---

## Business Impact Analysis (BIA) Targets

The BIA establishes Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO) for each perimeter, aligned with the FFIEC BCP/DR Handbook and SOX ITGC requirements.

| Tier | Perimeter | RTO | RPO | Notes |
|---|---|---|---|---|
| **Tier 1 Critical** | FIS Profile core banking | 4 hours | 15 minutes | OCC primary scope, customer-facing deposit and loan servicing |
| **Tier 1 Critical** | Wire transfer processing (ACI) | 2 hours | Zero for in-flight wires | Regulator-mandated, FedLine dependency |
| **Tier 1 Critical** | FedLine Advantage access | 1 hour | Zero | Federal Reserve-supervised |
| **Tier 2 Essential** | Jack Henry trust operations | 24 hours | 4 hours | Fiduciary accounts, end-of-day processing |
| **Tier 2 Essential** | Fiserv card services authorization | 4 hours | 15 minutes | Card authorization, dispute workflow |
| **Tier 2 Essential** | Digital banking channels | 8 hours | 1 hour | Online and mobile banking, Zelle P2P |
| **Tier 2 Essential** | ATM driving platform | 8 hours | 1 hour | Own fleet and surcharge-free network |
| **Tier 3 Deferrable** | Marketing analytics, HR IT, wealth reporting, branch video | 72+ hours | 24 hours | Non-customer-facing or archival |

---

## Vendor Tiering (TPRM)

The Third-Party Risk Management (TPRM) program tiers thirty vendors across the four perimeters. The sample below shows the critical-tier providers that drive the engagement's regulatory exposure.

| Vendor | Tier | Service | Regulatory Dependency |
|---|---|---|---|
| **FIS (Fidelity National Information Services)** | Critical | Core banking platform (Profile), deposit and loan servicing | OCC-supervised service provider |
| **Jack Henry & Associates** | Critical | Trust operations platform (SilverLake), fiduciary accounts | FFIEC-supervised service provider |
| **Fiserv** | Critical | Card services issuer processor, debit/credit, ATM driving | PCI DSS 4.0 scope, annual ROC |
| **ACI Worldwide** | Critical | Wire transfer processing (Posttrade), AML transaction monitoring | SOX ITGC in-scope, wire room controls |
| **Federal Reserve FedLine Advantage** | Critical (no BAA equivalent) | Fedwire and FedACH access, primary federal settlement | Federal Reserve-supervised, Operating Circular 5 |
| **Pershing** | High | Correspondent banking, downstream foreign bank services | FFIEC BSA/AML Examination Manual |
| **Datadog** | High | SIEM for audit log forwarding (US region) | FFIEC IT Handbook retention requirements |
| **Splunk Cloud** | High | Secondary SIEM archival for FFIEC retention | FFIEC IT Handbook retention requirements |
| **Azure Active Directory** | High | Identity provider for digital banking | FFIEC-supervised, MFA requirements |
| **Amazon Web Services** | High | Digital banking hosting | FFIEC-supervised, third-party hosting |

Full vendor inventory targets thirty providers across critical, high, medium, and low tiers with corresponding due-diligence cadences.

---

## Sample Validation Flow: Wire Fraud Incident Response

The five Phase 0 validation flows define approver workflows for the highest-risk operational events. The wire fraud response flow illustrates the pattern.

| Field | Detail |
|---|---|
| **Flow Name** | Wire fraud incident response (BEC on commercial customer) |
| **Trigger** | Suspected or confirmed wire fraud, including BEC, account takeover, or social engineering |
| **SLA** | 4 hours from detection to containment decision |
| **Approvers** | BSA Officer, CISO, Fraud Operations Director, General Counsel, CIO |
| **Inputs** | Wire detail, customer call-back verification status, correspondent bank notification, Federal Reserve recall eligibility |
| **Outputs** | Containment decision (recall initiated, loss accepted, customer notification), SAR filing determination, OCC notification if material |
| **Linked Risk** | MB-R-02 (Wire fraud via BEC targeting commercial customers) |
| **Linked Framework** | FFIEC Wholesale Payments Booklet, BSA/AML Examination Manual |

The other four validation flows follow the same pattern with different approver chains: OFAC match resolution (24-hour SLA), third-party vendor breach notification (72-hour SLA), catastrophic BCP activation (2-hour SLA, includes external OCC notification), and GLBA Safeguards exception (48-hour SLA, includes Board Risk Committee and Internal Audit sign-off).

---

## Closed Incident: BEC on Commercial Loan Customer (October 2025)

The persona includes one closed historical incident to support tabletop exercises and lessons-learned training.

| Field | Detail |
|---|---|
| **Incident ID** | MB-INC-2025-001 |
| **Date** | October 2025 |
| **Type** | Business email compromise (BEC) targeting commercial loan customer |
| **Severity** | High |
| **Status** | Closed |
| **Summary** | Spoofed CFO email instructed a regional construction firm (commercial loan customer) to redirect a $2.3M wire. Meridian call-back verification caught the request 38 minutes after wire release; recall initiated within 2 hours. $1.8M recovered via correspondent bank and Federal Reserve recall window. |
| **Lessons Learned** | Lowered mandatory call-back threshold from $500K to $250K for first-time beneficiary changes. Required dual approval for any wire where beneficiary bank changed within 14 days. Quarterly BEC tabletop with top 50 commercial customers. |
| **Linked Risk** | MB-R-02 (Wire fraud via BEC targeting commercial customers) |
| **Tabletop Candidate** | Yes — included in the validation flows for FY 2026 |

---

## Why FFIEC + GLBA + SOX Matter for This Engagement

A publicly traded mid-size community bank operates under a regulatory regime that is denser and more overlapping than what a FinTech or HealthTech faces. FFIEC is the dominant framework because OCC examiners assess against the FFIEC Cybersecurity Assessment Tool (CAT) and the FFIEC IT Examination Handbook booklets (Wholesale Payments, Retail Payments, Outsourcing, BSA/AML, BCP/DR). SOC 2 is not pursued — banking regulators prefer FFIEC, and pursuing both creates audit fatigue without regulatory value. SOX is mandatory because Meridian has been publicly traded since 2018; the PCAOB-registered auditor tests IT general controls annually across in-scope systems. GLBA Safeguards Rule governs customer NPI handling and was tightened in 2026; the program redesign was already underway when the engagement started.

The hybrid hosting model adds another layer: FIS Profile is hosted core banking, but Charlotte NC houses an on-premises data center for internal systems, Azure Active Directory handles identity for digital banking, and Amazon Web Services hosts the customer-facing digital channels. Each perimeter has different threat models, different vendor dependencies, and different regulatory anchors. A vCISO engagement that maps this cleanly is the kind of work OCC examiners reward at exam time and that the board audit committee can use for governance decisions.

---

## Value to GRC Consulting

| Service | Application |
|---|---|
| **FFIEC Pre-Assessment** | Demonstrates end-to-end FFIEC CAT + IT Examination Handbook scoping for a hybrid-hosting community bank |
| **GLBA Program Review** | Shows how to operationalize the 2026 GLBA Safeguards Rule revision into policies, ROPA, and validation flows |
| **SOX ITGC Posture Assessment** | Maps IT general controls scope across core banking, wire processing, and card services for a public company |
| **Hybrid Hosting Risk** | Demonstrates perimeter design and risk scoring for banks with mixed FIS-hosted, on-premises, and cloud-hosted infrastructure |
| **Third-Party Risk Management** | Shows tiering and due-diligence approach for thirty vendors across FFIEC-supervised, OCC-supervised, and Federal Reserve-supervised providers |
| **Incident Response Design** | Captures the wire fraud BEC pattern (spoofed CFO, callback catch, recall recovery) as a tabletop exercise template |
| **BIA / BCP/DR Design** | Tiered RTO/RPO targets aligned with FFIEC BCP/DR Handbook and SOX retention requirements |
| **Audit Log Forwarding** | Targets the SIEM pattern (Datadog primary, Splunk Cloud secondary) for FFIEC IT Examination Handbook 7-year retention |

---

## Tools & Frameworks

| Tool / Framework | Use |
|---|---|
| **CISO Assistant Community Edition v3.18.3** | GRC platform of record for framework library, risk register, policy library, validation flows |
| **FFIEC Cybersecurity Assessment Tool (CAT)** | Primary regulator-driven assessment framework |
| **FFIEC IT Examination Handbook** | Day-to-day supervision lens across all FFIEC booklets |
| **SOX ITGC** | Annual PCAOB-registered auditor testing of in-scope IT general controls |
| **GLBA Safeguards Rule (16 CFR Part 314)** | Customer NPI program design, 2026 revision incorporated |
| **PCI DSS 4.0** | Fiserv-scope card services ROC and AOC |
| **NYDFS 23 NYCRR 500** | Adjacent framework tracked despite no New York operations |
| **NIST Cybersecurity Framework (CSF) 2.0** | Cross-reference taxonomy |
| **Datadog (US region)** | Primary SIEM for audit log forwarding |
| **Splunk Cloud** | Secondary archival for FFIEC 7-year retention |

---

## Key Takeaways

1. **FFIEC dominates banking GRC work.** Pursuing SOC 2 alongside FFIEC creates audit fatigue without regulatory value. Banking regulators reward clean FFIEC CAT scoring and IT Examination Handbook alignment.

2. **Hybrid hosting requires perimeter-by-perimeter design.** FIS Profile, Jack Henry SilverLake, ACI, Azure AD, and AWS each have different threat models, different vendor dependencies, and different regulatory anchors. A vCISO who maps this cleanly is the kind of resource OCC examiners trust.

3. **Wire fraud response is a tabletop discipline, not a checklist.** The October 2025 BEC incident shows the value of mandatory call-back verification, dual approval for beneficiary bank changes, and quarterly tabletop exercises with the top commercial customers. The $1.8M recovery was policy-driven, not luck.

4. **Public-company status adds SOX ITGC to the engagement.** FIS Profile, ACI wire processing, and Fiserv card services are all in-scope for the PCAOB-registered auditor's annual cycle. The framework mapping must distinguish between what OCC examiners care about and what the SOX auditor tests.

---

## Related Projects

| Repo | Purpose |
|---|---|
| [AtlasPay FinTech SOC 2 Risk Assessment](https://github.com/ijeziermf/AtlasPay-Risk-Assessment) | Companion SOC 2 readiness engagement for a FinTech payment processor |
| [AtlasPay Business Continuity Plan & Risk Profile](https://github.com/ijeziermf/AtlasPay-Risk-Profile-BCP) | Companion BCP and risk profile for the same FinTech persona |
| [helix-health-grc-sandbox](https://github.com/ijeziermf/helix-health-grc-sandbox) | HIPAA + SOC 2 readiness for a HealthTech SaaS provider |
| [ciso-assistant-community](https://github.com/intuitem/ciso-assistant-community) | The open-source GRC platform of record (v3.18.3) |

---

## Phase 0 vs Phase 1

This repository is **Phase 0**: the engagement design. The persona specification, framework mapping, perimeter scoping, risk register seed, policy set, validation flows, and incident analysis are the work product. They are sufficient to start a Phase 1 engagement.

**Phase 1** ingests this specification into a live CISO Assistant Community Edition instance: 12 risk scenarios with inherent and residual scoring, 12 policies with framework crosswalks, 30 vendors with tier-appropriate due-diligence cadences, 15 ROPA processing activities, 5 validation flows with approver chains, and the audit-log forwarder from CISO Assistant to Datadog and Splunk Cloud. The lab/ folder in this repository contains the schema, scripts, and operational notes that an engineer would use to execute Phase 1.

---

## License

Educational and portfolio use. The Meridian Bank persona is a simulated engagement, not a real client. The work product is structured to demonstrate vCISO / Risk Manager competencies for hiring-manager evaluation.