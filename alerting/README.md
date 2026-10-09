# Alerting Rules

Defines **when and how the marketplace alerts on logging anomalies, security
events, and compliance failures**.

## Directory Structure

```
rules/
  audit-gap-alerts.yml        Audit log gap detection (Req. 10.5.5)
  audit-tampering-alerts.yml  Hash-chain break / log tampering (Req. 10.5.5)
  payment-access-alerts.yml   Unusual payment system access patterns
  retention-breach-alerts.yml Retention policy violation detection
  security-alerts.yml         Security event alerting (auth failures, privilege escalation)
escalation-policy.yml         Severity-based escalation procedures
```

## Alert Severity Levels

| Severity | Response Time | Escalation | Example |
|----------|---------------|------------|---------|
| CRITICAL | Immediate | Org owner, on-call | Audit log gap, hash-chain break |
| HIGH | 1 hour | Org owner | Unusual payment access, retention breach |
| MEDIUM | 4 hours | Review in next business day | Elevated auth failures |
| LOW | 24 hours | Weekly review | Informational security events |
