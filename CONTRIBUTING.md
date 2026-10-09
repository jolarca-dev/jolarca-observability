# Contributing — jolarca-observability

## Before You Start

This is a **PCI-DSS-scoped governance repository** in the `jolarca-dev`
marketplace fleet.

**Target controls** (required before production sign-off):

- Branch protection on `main` — require PR, ≥1 approval, squash-only, linear
  history, block force-push and deletion
- Required status checks: `Lint & Type Check` and `Tests` (from `ci.yml`) plus
  the `compliance-scan` verification jobs
- Fleet separation guard (ADR-0004 — no mission-platform references)
- Secret scanning with push protection

> **Current state (repository readiness audit).** Branch protection, secret-
> scanning push protection and code scanning require GitHub Team + GitHub
> Advanced Security, which are **not enabled** on this private repository
> (findings F-01/F-02/F-03). Org-wide 2FA is also **not yet enforced** (F-04).
> Until these are enabled, the compensating controls below are mandatory.

**Compensating controls in force now:**

- Local **pre-commit** hooks (`.pre-commit-config.yaml`): ruff, `mypy --strict`,
  yamllint, **gitleaks** and **detect-secrets** run before every commit. Install
  with `make setup && pip install pre-commit && pre-commit install --install-hooks`.
- **Signed commits**, pushed to a **feature branch only** — never to `main`.
- Repository stays **private**; least-privilege access; no write deploy keys.

## Code Standards

- **Python:** `ruff` linter, `mypy --strict`; pytest regression tests cover
  every verification script (a coverage threshold is a target, not yet enforced
  in CI)
- **Shell:** `shellcheck -x` on any shell scripts (none present today —
  `scripts/` is Python)
- **YAML:** `yamllint` with the project `.yamllint` configuration
- **Actions:** pinned to full 40-character commit SHAs, never tags

## Commit Messages

Conventional commit format: `type(scope): description`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

## What Requires Extra Care

Changes to the following have compliance impact and must be reviewed against
the framework mappings in `compliance/`:

- `schemas/` — removing a mandatory field may break PCI-DSS Req. 10.2
- `audit-trail/retention/` — shortening retention violates Req. 10.5.1
- `audit-trail/integrity/` — weakening hash-chain verification undermines
  Req. 10.5.5
- `alerting/rules/` — removing an alert may create a detection gap
- `logging/configs/` — disabling a log source reduces audit coverage

## No Secrets in Git

See `policy/repo-defaults.yml` in `jolarca-control`. Required `.gitignore`
patterns are enforced. A secret found in git is an incident — see
`runbooks/secret-exposure.md`.
