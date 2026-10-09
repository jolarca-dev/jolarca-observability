# jolarca-observability

**Centralized logging, alerting, audit-trail retention and log-integrity for the
`jolarca-dev` marketplace.**

> **Compliance:** SOC 2 Type II · GDPR · ISO 27001:2022 · PCI-DSS 4.0
> **Owner:** jolarca-dev organization owner (single operator)
> **Governed by:** [`jolarca-control`](https://github.com/jolarca-dev/jolarca-control)

## Purpose

This repository defines **what the marketplace logs, how it alerts on anomalies,
how long audit trails are retained, and how log integrity is verified**. It does
not run the logging infrastructure — that lives in `jolarca-infrastructure`.
This repo holds the configurations, schemas, alerting rules and verification
scripts that the infrastructure implements.

A marketplace that processes payments and collects KYC/AML identity documents
**without immutable audit logging is an automatic PCI-DSS finding**. This
repository exists to close that gap.

## Repository Structure

```
logging/           Centralized logging configurations
  configs/         Per-domain log configs (audit, payment, KYC/AML, app, system)
  transforms/      Log normalization and redaction transforms
alerting/          Alerting rules and escalation procedures
  rules/           Per-domain alert definitions
audit-trail/       Audit-trail retention, integrity and backup
  retention/       Retention policies (PCI DSS Req. 10.5)
  integrity/       Hash-chain verification and tamper detection
  backup/          Audit-log backup and restore procedures
schemas/           Mandatory log-field schemas
compliance/        Framework-specific compliance mappings
scripts/           Verification scripts (retention, integrity, completeness)
runbooks/          Incident response runbooks for logging failures
tests/             Regression tests for verification scripts
.github/workflows/ CI pipelines
```

## Compliance Scope

| Framework | Key Requirements Covered |
|-----------|--------------------------|
| PCI-DSS 4.0 | Req. 10 (log and monitor all access), Req. 10.5 (protect audit logs), Req. 10.5.1 (12-month retention) |
| SOC 2 Type II | CC7.1–CC7.2 (detection and response), CC8.1 (change management audit trail) |
| GDPR | Art. 30 (records of processing), Art. 32 (security of processing) |
| ISO 27001:2022 | A.5.24 (event logging), A.5.25 (clock synchronisation), A.8.15 (monitoring) |

## Verification

```bash
make setup         # one-time: create .venv with the pinned toolchain
make lint          # ruff + mypy --strict + yamllint
make test          # pytest — retention, integrity, schema tests
make verify-all    # full compliance verification suite
```

## Relationship to jolarca-control

This repository is declared in `jolarca-control/repos/jolarca-observability.yml`
and is intended to follow the same branch-protection, compliance-gate and
drift-detection regime as every other fleet repository. Changes arrive through a
PR; the `jolarca-control` CI pipeline validates the YAML and runs
fleet-separation guards.

> **Pending (audit findings F-01/F-02/F-03):** branch protection, secret-scanning
> push protection and code scanning require GitHub Team + Advanced Security and
> are **not yet enforceable** on this private repository. Local pre-commit hooks
> and CI act as compensating controls until the plan is upgraded.

## License

Proprietary — see [LICENSE](LICENSE). No OSS licence is granted; all content is
the confidential property of the jolarca-dev organization (All Rights Reserved).
