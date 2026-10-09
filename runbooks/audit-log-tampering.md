# Runbook: Audit Log Tampering Response

**Severity:** CRITICAL
**Trigger:** `HASH_CHAIN_BREAK` alert — hash-chain integrity verification failed
**PCI-DSS:** Req. 10.5.5 (file-integrity monitoring)

## IMMEDIATE: Preserve Evidence (0–15 minutes)

1. **DO NOT restart, rotate, or modify log storage** — the current state is forensic evidence
2. **Acknowledge the alert** — log the acknowledgement timestamp
3. **Restrict access to log storage** — if possible, limit to read-only
4. **Notify the organization owner** — this is a potential security incident

## Investigation (15–60 minutes)

5. **Identify the affected entries** — which hash-chain position broke?
   ```bash
   python scripts/verify_integrity.py 2>&1 | tee /tmp/integrity-report.txt
   ```
6. **Determine the time window** — when was the last known-good hash? When is the first bad hash?
7. **Check access logs for the log storage system**:
   - Who accessed the storage in the time window?
   - Were there any write operations outside the collector pipeline?
   - Were there any backup/restore operations?
8. **Check system access logs** — who logged into the log storage host?
9. **Check for authorized changes** — was a backup restore or migration performed?

## Escalation Criteria

- **Confirmed unauthorized modification** → GDPR Art. 33 breach assessment
- **Cannot determine cause** → treat as potential compromise
- **Authorized change without documentation** → process failure, not security incident

## GDPR Art. 33 Assessment

If unauthorized modification is confirmed:
1. **Assess affected data subjects** — whose audit trail was modified?
2. **Assess likelihood of harm** — can the modified logs hide a data breach?
3. **72-hour notification clock** — if notifiable, the clock started at detection
4. **Document the assessment** — in `jolarca-compliance`

## Post-Incident

10. **Rebuild the hash chain** — from the last known-good entry forward
11. **Verify the rebuilt chain** — run `verify_integrity.py` again
12. **Document the root cause** — how was the modification possible?
13. **Strengthen controls** — what additional access control is needed?
14. **File a compliance event** — record in `jolarca-compliance`
