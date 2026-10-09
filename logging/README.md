# Centralized Logging Configuration

Defines **what** the marketplace logs, **how** log entries are structured, and
**where** they flow through the pipeline.

## Directory Structure

```
configs/           Per-domain log source configurations
  audit-log.yml    Administrative and privileged access events
  payment-log.yml  Payment processing and cardholder-data access
  kyc-aml-log.yml  KYC/AML identity verification events
  application-log.yml  Application-level events and errors
  system-access.yml    OS and infrastructure access events
transforms/        Log normalization and redaction rules
  redaction.yml    PAN/PII masking rules (PCI-DSS Req. 3.3)
  normalization.yml  Timestamp and field normalization
```

## Compliance Coverage

| Domain | PCI-DSS Req. 10 | SOC 2 CC7 | ISO A.5.25 |
|--------|-----------------|-----------|------------|
| Audit log | 10.2 (all admin actions) | CC7.1 (change detection) | Operator activities |
| Payment log | 10.2 (CHD access) | CC7.1 (anomaly detection) | Security events |
| KYC/AML log | 10.2 (identity data access) | CC7.2 (incident detection) | Exception events |
| Application log | 10.2 (invalid access) | CC7.1 (vulnerability detection) | Error events |
| System access | 10.2 (system access) | CC7.1 (unauthorized activity) | System events |

## Key Principle

**Every log domain must produce entries conforming to the schemas in
`schemas/`.** A log entry missing mandatory fields is a compliance failure —
`scripts/verify_completeness.py` detects this.
