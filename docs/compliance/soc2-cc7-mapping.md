# SOC 2 Type II — CC7 (System Operations) Compliance Mapping

## CC7.1 — Detection of Configuration Changes and Vulnerabilities

| Control | Implementation | Evidence |
|---|---|---|
| Log monitoring for unauthorized activity | `alerting/rules/` — real-time alerting | Alert rule definitions |
| Anomaly detection | `alerting/rules/security-alerts.yml` | Unusual access patterns |
| Configuration change detection | `alerting/rules/audit-gap-alerts.yml` | Log gap = potential config change |
| Vulnerability detection | Delegated to `jolarca-control` compliance gates | CI pipeline |

## CC7.2 — Incident Response

| Control | Implementation | Evidence |
|---|---|---|
| Incident detection procedures | `alerting/escalation-policy.yml` | Severity-based escalation |
| Incident response procedures | `runbooks/` | Gap, tampering, retention procedures |
| Incident logging | `logging/configs/audit-log.yml` | All incidents logged as security events |
| Retrospective analysis | `audit-trail/retention/retention-policy.yml` | 12-month retention enables post-incident review |

## CC7.3 — Communication of Security Events

| Control | Implementation | Evidence |
|---|---|---|
| Security events communicated to management | `alerting/escalation-policy.yml` | CRITICAL → immediate, HIGH → 1h |
| Security events communicated to affected parties | Delegated to `jolarca-compliance` breach procedures | DPA obligations |

## CC7.4 — Security Event Analysis

| Control | Implementation | Evidence |
|---|---|---|
| Root cause analysis supported by logs | `schemas/audit-log-schema.yml` | Complete audit trail with actor, action, resource |
| Trend analysis | `audit-trail/retention/retention-policy.yml` | 12-month retention enables trend analysis |
| Correlation across systems | `logging/configs/` | Unified schema across all log domains |
