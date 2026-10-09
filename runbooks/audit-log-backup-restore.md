# Runbook: Audit Log Backup and Restore

**Purpose:** Restore audit logs from backup after data loss or corruption
**Related:** `audit-trail/backup/backup-policy.yml`

## Backup Verification

Before any restore, verify the backup integrity:

1. **Check backup manifest** — does the entry count match?
2. **Verify hash chain** — recompute hashes on the backup copy
3. **Check encryption** — can the backup be decrypted with the current key?

## Restore Procedure

1. **Identify the restore point** — which backup contains the needed logs?
2. **Create an isolated restore environment** — do NOT restore to production
3. **Restore the backup** to the isolated environment
4. **Verify the restored data**:
   - Hash chain integrity: `python scripts/verify_integrity.py`
   - Schema completeness: `python scripts/verify_completeness.py`
   - Entry count matches backup manifest
5. **Copy verified data** to production log storage
6. **Verify production data** — run verification scripts against production
7. **Document the restore** — record timestamps, entry counts, verification results

## Quarterly Restore Test

Per `audit-trail/backup/backup-policy.yml`, a test restore is performed quarterly:

1. Restore latest full backup to isolated environment
2. Run all verification scripts
3. Measure restore time (must be within RTO of 4 hours)
4. Record results as compliance evidence
