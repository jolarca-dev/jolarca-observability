# Runbook: Audit Log Gap Investigation

**Severity:** CRITICAL
**Trigger:** `AUDIT_GAP_5MIN` alert — no audit entries for 5+ minutes
**PCI-DSS:** Req. 10.5.5 (log integrity)

## Immediate Actions (0–15 minutes)

1. **Acknowledge the alert** — log the acknowledgement timestamp
2. **Check log collector health** — is the OpenTelemetry collector running?
   ```bash
   systemctl status otel-collector
   journalctl -u otel-collector --since "10 minutes ago"
   ```
3. **Check log source connectivity** — are application components emitting events?
   ```bash
   # Check if the application is running
   systemctl status jolarca-app
   # Check network connectivity to the collector
   curl -s http://localhost:4318/v1/logs  # OTLP HTTP endpoint
   ```
4. **Check log storage** — is the storage system accepting writes?
   ```bash
   # Check storage health
   curl -s https://log-storage.internal/health
   ```

## Investigation (15–60 minutes)

5. **Determine the gap window** — when did entries stop? When did they resume (if at all)?
6. **Check for deployments or changes** — was anything deployed during the gap?
   ```bash
   # Check recent deployments
   gh api repos/jolarca-dev/jolarca/deployments --jq '.[0:5]'
   ```
7. **Check system access logs** — did anyone access the log infrastructure?
8. **Check for infrastructure failures** — network partition, disk full, OOM?

## Escalation

- If the gap cannot be explained within 1 hour → escalate to org owner
- If the gap exceeds 30 minutes with no explanation → treat as potential tampering
- If evidence of unauthorized access → initiate incident response per `jolarca-security`

## Post-Incident

9. **Document the root cause** — what caused the gap?
10. **Document the duration** — how long was logging interrupted?
11. **Assess compliance impact** — were any events lost permanently?
12. **File a compliance event** — record in `jolarca-compliance`
13. **Update alerting rules** — if the gap was a false positive, adjust thresholds

## Evidence to Retain

- Collector logs for the gap window
- System metrics (CPU, memory, disk, network) for the gap window
- Deployment records for the gap window
- This completed runbook with timestamps
