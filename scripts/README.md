# Verification Scripts

Automated verification scripts that validate the logging, alerting, and
audit-trail configurations comply with PCI-DSS Req. 10 and other framework
requirements.

## Scripts

| Script | Purpose | PCI-DSS Req. |
|--------|---------|-------------|
| `verify_retention.py` | Validates retention policy compliance | 10.5.1 |
| `verify_integrity.py` | Verifies hash-chain integrity | 10.5.5 |
| `verify_completeness.py` | Checks mandatory field presence in log schemas | 10.2 |

## Usage

```bash
# Run all verification scripts
make verify-all

# Run individual scripts
python scripts/verify_retention.py
python scripts/verify_integrity.py
python scripts/verify_completeness.py
```

## Exit Codes

All scripts use consistent exit codes:

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Verification failed — compliance issue detected |
| 2 | Could not verify — infrastructure error (treat as failure) |

Exit code 2 follows the D-23 principle from jolarca-control: **unverifiable
state must fail loudly, never silently pass**.
