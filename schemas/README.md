# Log Schemas

Defines the **mandatory fields** that every audit-log entry must contain.
A log entry missing a mandatory field is a compliance failure — it cannot
satisfy PCI-DSS Req. 10.2 (audit logs capture all actions) if the entry
does not record who did what and when.

## Schemas

| Schema | Domain | Key PCI-DSS Req. |
|--------|--------|-----------------|
| `audit-log-schema.yml` | All domains (base schema) | 10.2 |
| `payment-log-schema.yml` | Payment processing | 10.2.1 |
| `kyc-aml-log-schema.yml` | KYC/AML identity verification | 10.2.1 + GDPR Art. 30 |

## Validation

`scripts/verify_completeness.py` validates that log entries conform to these
schemas by checking that all mandatory fields are present and non-null.
