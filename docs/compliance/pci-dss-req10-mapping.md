# PCI-DSS 4.0 Requirement 10 — Compliance Mapping

## Overview

PCI-DSS Req. 10 requires organizations to **log and monitor all access to
system components and cardholder data**. For a marketplace processing payments
and collecting KYC/AML identity documents, this is not optional — the absence
of compliant audit logging is an **automatic PCI finding**.

## Control-by-Control Mapping

### Req. 10.1 — Audit trails are implemented and linked to individual users

| Control | Implementation |
|---|---|
| Every log entry identifies the actor | `schemas/audit-log-schema.yml` requires `actor_id`, `actor_type` |
| Audit trail covers all system components | `logging/configs/` covers audit, payment, KYC/AML, app, system |
| Linked to unique user | `actor_id` is the authenticated user identifier, never shared |

### Req. 10.2 — Audit logs capture all actions by individuals

| Control | Implementation |
|---|---|
| All admin actions logged | `logging/configs/audit-log.yml` — admin events are mandatory |
| All access to cardholder data logged | `logging/configs/payment-log.yml` — every CHD access event |
| All access to KYC data logged | `logging/configs/kyc-aml-log.yml` — identity data access events |
| Invalid logical access attempts logged | `logging/configs/system-access.yml` — auth failures |
| Changes to identification/auth mechanisms logged | `logging/configs/audit-log.yml` — auth config changes |

### Req. 10.3 — Audit logs are protected from modification

| Control | Implementation |
|---|---|
| Logs protected from unauthorized modification | `audit-trail/integrity/hash-chain.yml` — SHA-256 hash chain |
| Logs protected from unauthorized deletion | `audit-trail/retention/retention-policy.yml` — append-only storage, retention enforcement |
| Promptly backed up | `audit-trail/backup/backup-policy.yml` — daily incremental, weekly full |

### Req. 10.4 — Logs are reviewed regularly

| Control | Implementation |
|---|---|
| Automated log review | `alerting/rules/` — real-time alerting on anomalies |
| Review of payment access logs | `alerting/rules/payment-access-alerts.yml` |
| Review of audit-log integrity | `alerting/rules/audit-tampering-alerts.yml` |
| Exception and security event review | `alerting/rules/security-alerts.yml` |

### Req. 10.5 — Audit logs are retained

| Control | Implementation |
|---|---|
| History retained for 12 months minimum | `audit-trail/retention/retention-policy.yml` — `min_retention_months: 12` |
| At least 3 months immediately available | `audit-trail/retention/retention-policy.yml` — `hot_retention_months: 3` |
| Logs protected from modification | `audit-trail/integrity/hash-chain.yml` |

### Req. 10.5.1 — File integrity monitoring for logs

| Control | Implementation |
|---|---|
| FIM or change-detection on logs | `scripts/verify_integrity.py` — daily hash-chain verification |
| Alerts on integrity failures | `alerting/rules/audit-tampering-alerts.yml` — hash-chain break → CRITICAL |
| Alerts on log gaps | `alerting/rules/audit-gap-alerts.yml` — gap > 5 min → CRITICAL |

### Req. 10.6 — Security incidents identified

| Control | Implementation |
|---|---|
| Processes to identify security incidents | `alerting/rules/` — comprehensive alerting across all domains |
| Incident response procedures | `runbooks/` — gap, tampering, retention breach procedures |
| Escalation procedures | `alerting/escalation-policy.yml` — severity-based escalation |

## Verification

```bash
# Verify retention policy compliance
python scripts/verify_retention.py

# Verify hash-chain integrity
python scripts/verify_integrity.py

# Verify audit-log completeness (mandatory fields)
python scripts/verify_completeness.py
```

## Auditor Notes

- This mapping covers the governance-plane controls. Infrastructure-level
  controls (encryption at rest, network segmentation, access control on log
  storage) are in `jolarca-infrastructure`.
- The hash-chain mechanism provides cryptographic integrity but does not
  replace access control on the log storage itself — defense in depth.
- Retention is measured from the event timestamp, not the collection timestamp.
