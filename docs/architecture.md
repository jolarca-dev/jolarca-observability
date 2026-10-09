# Architecture — jolarca-observability

## Overview

`jolarca-observability` defines the **logging, alerting, audit-trail retention
and log-integrity** configurations for the `jolarca-dev` marketplace. It is a
governance repository: it holds configurations, schemas and verification
scripts — not runtime code. The actual logging infrastructure is implemented in
`jolarca-infrastructure`.

This repository exists because a marketplace that processes payments and
collects KYC/AML identity documents **without immutable, integrity-verified
audit logging** incurs an automatic PCI-DSS finding under Req. 10. The
configurations here are the control plane's answer to that requirement.

## Compliance Drivers

| Requirement | What It Demands | Where It Is Met |
|---|---|---|
| PCI-DSS 10.2 | Audit logs capture all actions by individuals with admin/critical privileges | `logging/configs/audit-log.yml`, `schemas/audit-log-schema.yml` |
| PCI-DSS 10.5 | Audit logs protected from modification | `audit-trail/integrity/hash-chain.yml` |
| PCI-DSS 10.5.1 | Audit log history retained for 12 months, 3 immediately available | `audit-trail/retention/retention-policy.yml` |
| PCI-DSS 10.5.5 | Use file-integrity monitoring or change-detection to detect log tampering | `audit-trail/integrity/hash-chain.yml`, `scripts/verify_integrity.py` |
| SOC 2 CC7.1 | Detection of configuration changes and vulnerabilities | `alerting/rules/` |
| SOC 2 CC8.1 | Changes recorded with an audit trail | `logging/configs/audit-log.yml` |
| GDPR Art. 30 | Records of processing activities | `logging/configs/audit-log.yml` (access-logging for processing records) |
| GDPR Art. 32 | Security of processing including audit capability | All configs |
| ISO 27001 A.5.24 | Event logging — operator activities, exceptions, security events | `logging/configs/` (all domains) |
| ISO 27001 A.5.25 | Clock synchronisation — timestamps from synchronised sources | `logging/configs/system-access.yml` |
| ISO 27001 A.8.15 | Monitoring — systems monitored for unauthorized activity | `alerting/rules/` |

## Logging Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Layer (jolarca)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Payment  │  │ KYC/AML  │  │  User    │  │  Admin   │           │
│  │  Events  │  │  Events  │  │  Events  │  │  Events  │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       │              │              │              │                 │
│  ┌────▼──────────────▼──────────────▼──────────────▼─────┐          │
│  │              Structured Log Emitters                   │          │
│  │  (JSON, mandatory fields per schemas/*.yml)            │          │
│  └────────────────────┬───────────────────────────────────┘          │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────────┐
│              Logging Infrastructure (jolarca-infra)                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Log Collector (OpenTelemetry / Fluent Bit)       │   │
│  │  • Validates mandatory fields against schemas                │   │
│  │  • Applies redaction transforms (PAN, PII)                   │   │
│  │  • Computes hash-chain entry (SHA-256, previous hash)        │   │
│  └────────────────────────┬─────────────────────────────────────┘   │
│                           │                                         │
│  ┌────────────────────────▼─────────────────────────────────────┐   │
│  │              Log Storage (Append-Only, Encrypted)             │   │
│  │  • Hot: 3 months immediately available (Req. 10.5.1)         │   │
│  │  • Warm: 9 months archived, 48h retrieval                    │   │
│  │  • Hash chain verified daily by scripts/verify_integrity.py  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Alerting Engine                                  │   │
│  │  • Gap detection: audit log gap > 5 minutes → CRITICAL       │   │
│  │  • Tamper detection: hash-chain break → CRITICAL              │   │
│  │  • Access anomaly: unusual payment admin access → HIGH        │   │
│  │  • Retention breach: deletion before retention expires → HIGH │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────────────┐
│              Verification Layer (this repository)                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  scripts/verify_retention.py   — retention policy checks     │   │
│  │  scripts/verify_integrity.py   — hash-chain verification     │   │
│  │  scripts/verify_completeness.py — mandatory-field checks     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Log Redaction

Payment card data (PAN) and KYC identity documents are **Restricted**
classification (see `docs/data-classification.md` in `jolarca-control`). They
must never appear in log output. `logging/transforms/redaction.yml` defines the
redaction rules:

- PAN: masked to last 4 digits per PCI-DSS Req. 3.3
- KYC document numbers: hashed with SHA-256, original not logged
- Authentication tokens: never logged, even partial
- Session IDs: permitted, but must not be usable to reconstruct sessions

## Hash-Chain Integrity Model

Each audit-log entry includes a `hash_chain` field:

```
hash_chain = SHA-256(
    timestamp || event_id || actor_id || event_type || previous_hash
)
```

- `previous_hash` for the first entry in a day is the last hash of the
  previous day (or a genesis hash for the first entry ever)
- `scripts/verify_integrity.py` recomputes every hash and reports breaks
- A hash-chain break is a **CRITICAL** alert (potential log tampering)
- This satisfies PCI-DSS Req. 10.5.5 (file-integrity monitoring for logs)

## Data Flow

1. **Emit** — application emits structured JSON log events with all mandatory
   fields from `schemas/`
2. **Collect** — OpenTelemetry collector validates schema, applies redaction
3. **Chain** — collector appends hash-chain entry
4. **Store** — append-only write to encrypted log storage
5. **Alert** — alerting engine evaluates rules from `alerting/rules/`
6. **Verify** — daily integrity check; weekly retention audit; monthly
   completeness report

## Relationship to Other Repositories

| Repository | Relationship |
|---|---|
| `jolarca-control` | Governs this repo: branch protection, compliance gates, drift detection |
| `jolarca-infrastructure` | Implements the logging infrastructure defined by this repo's configs |
| `jolarca` | Application that emits the log events consumed by the pipeline |
| `jolarca-security` | Security policies and threat models that inform alerting rules |
| `jolarca-compliance` | Holds DPIAs and audit evidence; receives compliance reports |
