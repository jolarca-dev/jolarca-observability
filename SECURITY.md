# Security Policy — jolarca-observability

## Scope

This repository holds logging configurations, alerting rules, audit-trail
retention policies and log-integrity verification scripts for the `jolarca-dev`
marketplace. It does **not** hold production log data, cardholder data, or
KYC/AML identity documents.

## Reporting a Vulnerability

| Severity | CVSS v3.1 | Response Time | Channel |
|----------|-----------|---------------|---------|
| Critical | 9.0–10.0 | 24 hours | `journey4oflife+jolarca.security@gmail.com` (interim) |
| High | 7.0–8.9 | 72 hours | `journey4oflife+jolarca.security@gmail.com` (interim) |
| Medium | 4.0–6.9 | 7 days | GitHub Security Advisory |
| Low | 0.1–3.9 | 30 days | GitHub Security Advisory |

## What to Report

- Alerting rules that could be evaded to avoid detection of cardholder-data
  access
- Integrity-verification bypasses in the hash-chain mechanism
- Retention-policy configurations that fail PCI-DSS Req. 10.5.1
- Log schemas that omit mandatory fields required for audit-trail completeness
- Any secret, token or credential found in this repository

## Do NOT

- Open a public issue for a security vulnerability
- Test vulnerabilities against production logging infrastructure without
  authorization
- Disclose vulnerabilities in third-party tools we use without coordinated
  disclosure
