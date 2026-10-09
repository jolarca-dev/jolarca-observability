# Runbook: Retention Policy Breach Response

**Severity:** HIGH
**Trigger:** `RETENTION_PREMATURE_DELETE` or `RETENTION_HOT_EXPIRED` alert
**PCI-DSS:** Req. 10.5.1 (retention)

## Immediate Actions (0–1 hour)

1. **Acknowledge the alert** — log the acknowledgement timestamp
2. **Determine the scope**:
   - Which log domain is affected?
   - What time range of logs is missing or inaccessible?
   - Was the deletion authorized?
3. **Check backup availability**:
   ```bash
   # List recent backups
   # (command depends on backup infrastructure — see jolarca-infrastructure)
   ```
4. **If logs can be restored from backup** → restore immediately
5. **If logs cannot be restored** → escalate to org owner

## Investigation (1–4 hours)

6. **Determine the cause**:
   - Was a retention policy misconfigured?
   - Was a storage system failure responsible?
   - Was the deletion deliberate and unauthorized?
7. **Check for correlated events** — does the loss coincide with any other incident?
8. **Assess compliance impact**:
   - Are the missing logs within the 12-month retention window?
   - Are they needed for any ongoing investigation?
   - Are they needed for any regulatory filing?

## Post-Incident

9. **Restore from backup** if possible
10. **Document the root cause** — what failed?
11. **Document the data loss** — what logs are permanently lost?
12. **Assess regulatory impact** — is this notifiable?
13. **Strengthen controls** — prevent recurrence
14. **File a compliance event** — record in `jolarca-compliance`
