# Changelog — jolarca-observability

All notable changes to this repository are recorded here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Initial repository structure: logging configs, alerting rules, audit-trail
  retention, log-integrity verification, compliance mappings
- PCI-DSS Req. 10 compliance mapping
- SOC 2 CC7.1–CC7.2 compliance mapping
- GDPR Art. 30/32 compliance mapping
- ISO 27001 A.5.24/A.5.25/A.8.15 compliance mapping
- Log schemas for audit, payment and KYC/AML domains
- Verification scripts: retention, integrity, completeness
- Incident response runbooks for logging failures
- Proprietary `LICENSE` (All Rights Reserved)
- `.github/CODEOWNERS` — owner review routing for compliance-sensitive paths
- `.pre-commit-config.yaml` — ruff, mypy, yamllint, gitleaks, detect-secrets
- `.github/dependabot.yml` — weekly grouped pip + github-actions updates
- `.secrets.baseline` — verified false-positive allowlist for detect-secrets
- `.gitleaks.toml` — extends the default gitleaks ruleset; allowlists only the
  `.secrets.baseline` path (hashed values, not plaintext)
- `runbooks/secret-exposure.md` — secret-exposure incident response
- `types-PyYAML` pinned in `requirements-dev.txt` (mypy `--strict` stubs)

### Fixed

- CI `lint` job now passes: cleared 25 `ruff` findings — `PTH123`
  (`open()` → `Path.open()`), `COM812` (trailing commas), and `S101`/`S603`
  scoped to `tests/` via `per-file-ignores`
- CI `lint` job now passes: cleared 15 `mypy --strict` findings — bare `dict`
  generics → `dict[str, Any]`, plus the missing `types-PyYAML` stubs
- Removed the invalid `shellcheck` run against Python files in `ci.yml`
- Corrected control claims in `CONTRIBUTING.md` / `README.md` to match the
  verified repository state (repository readiness audit, findings F-01..F-15)
