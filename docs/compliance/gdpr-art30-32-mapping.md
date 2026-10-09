# GDPR — Articles 30 & 32 Compliance Mapping

## Art. 30 — Records of Processing Activities

| Requirement | Implementation | Evidence |
|---|---|---|
| Records of processing maintained | Access logging enables reconstruction of processing activities | `logging/configs/audit-log.yml` |
| Records available on request | 12-month retention (hot + warm) ensures availability | `audit-trail/retention/retention-policy.yml` |
| Records include purposes and categories | Log events include `event_type`, `data_categories` | `schemas/audit-log-schema.yml` |

## Art. 32 — Security of Processing

| Requirement | Implementation | Evidence |
|---|---|---|
| Ability to ensure confidentiality | Log redaction prevents PII leakage | `logging/transforms/redaction.yml` |
| Ability to ensure integrity | Hash-chain verification detects tampering | `audit-trail/integrity/hash-chain.yml` |
| Ability to ensure availability | Backup policy ensures log availability | `audit-trail/backup/backup-policy.yml` |
| Ability to ensure resilience | Alerting detects failures in real-time | `alerting/rules/` |
| Regular testing of measures | Verification scripts test continuously | `scripts/verify_*.py` |
| Access logging for personal data | All access to KYC/identity data logged | `logging/configs/kyc-aml-log.yml` |

## Data Minimization in Logs

Logs must not contain more personal data than necessary for the audit purpose:

- PAN is masked to last 4 digits (PCI-DSS Req. 3.3)
- KYC document numbers are hashed, not stored in plaintext
- Authentication tokens are never logged
- IP addresses are logged for security purposes (legitimate interest, Art. 6(1)(f))
- Session identifiers are logged but must not be usable to reconstruct sessions
