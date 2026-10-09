# ISO 27001:2022 — Annex A Controls Compliance Mapping

## A.5.24 — Use of Cryptography

| Control | Implementation | Evidence |
|---|---|---|
| Hash-chain integrity for audit logs | SHA-256 hash chain links every audit entry | `audit-trail/integrity/hash-chain.yml` |
| Encryption in transit for log shipping | TLS 1.3 between collector and storage | Defined in `jolarca-infrastructure` |
| Encryption at rest for log storage | AES-256-GCM with CMEK | Defined in `jolarca-infrastructure` |

## A.5.25 — Event Logging

| Control | Implementation | Evidence |
|---|---|---|
| Operator activities logged | `logging/configs/audit-log.yml` | All operator actions logged |
| Exception and error events logged | `logging/configs/application-log.yml` | Errors and exceptions captured |
| Security events logged | `logging/configs/audit-log.yml` | Auth failures, privilege changes |
| Information on systems and services logged | `logging/configs/system-access.yml` | System-level access events |
| Logs synchronized across systems | NTP synchronization required | `logging/configs/system-access.yml` |

## A.8.15 — Monitoring

| Control | Implementation | Evidence |
|---|---|---|
| Systems monitored continuously | `alerting/rules/` — real-time alerting | Alert rule definitions |
| Monitoring covers all critical systems | `logging/configs/` — payment, KYC, audit, system | Config coverage |
| Monitoring results reviewed regularly | Automated analysis + alerting | `alerting/escalation-policy.yml` |
| Results retained as evidence | 12-month retention policy | `audit-trail/retention/retention-policy.yml` |
