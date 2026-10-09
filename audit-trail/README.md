# Audit Trail

Defines **how audit logs are retained, protected, and backed up** to satisfy
PCI-DSS Req. 10.5 and equivalent requirements across all compliance frameworks.

## Directory Structure

```
retention/
  retention-policy.yml    Retention periods per log domain
integrity/
  hash-chain.yml          Hash-chain integrity mechanism specification
  verification-config.yml Configuration for integrity verification scripts
backup/
  backup-policy.yml       Audit-log backup schedule and restore procedures
```

## Key Requirements

| Requirement | Source | Implementation |
|---|---|---|
| 12-month minimum retention | PCI-DSS 10.5.1 | `retention/retention-policy.yml` |
| 3 months immediately available | PCI-DSS 10.5.1 | `retention/retention-policy.yml` (hot tier) |
| Logs protected from modification | PCI-DSS 10.5 | `integrity/hash-chain.yml` |
| File-integrity monitoring | PCI-DSS 10.5.5 | `integrity/verification-config.yml` |
| Promptly backed up | PCI-DSS 10.5.3 | `backup/backup-policy.yml` |
