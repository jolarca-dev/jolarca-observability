# Runbook: Secret Exposure Response

**Severity:** CRITICAL
**Trigger:** A secret, token, key or credential is found in this repository —
via gitleaks / detect-secrets, a GitHub secret-scanning alert, or manual
discovery — or a pattern that `.gitignore` should have excluded is committed.
**PCI-DSS:** Req. 3 (protect stored data), Req. 10 (log and monitor access)
**Compliance:** SOC 2 CC6.1 · ISO 27001 A.5.17 · GDPR Art. 33 (72-hour notice)

## Immediate Actions (0–1 hour)

1. **STOP all pushes** to the affected branch — do not add more commits.
2. **Rotate the secret FIRST** — even if it looks brand-new or unused. Once a
   secret has touched git it is treated as compromised:
   - API tokens / PATs → revoke and reissue
   - Cloud access keys → deactivate and rotate
   - Passwords / DB credentials → change immediately
   - TLS keys / certificates → reissue from the CA
3. **Identify type and blast radius** — what does the credential grant access to?
4. **Preserve evidence** — record the commit SHA, file and line, and the scanner
   finding. **Never** paste the secret value into tickets, logs or chat.

## Containment & Removal (1–4 hours)

5. **Purge from history** — deleting in a new commit does NOT remove a secret
   that is already in history:
   ```bash
   # Rewrites SHAs — coordinate with every clone/collaborator first
   git filter-repo --invert-paths --path <path-to-file>
   git push --force-with-lease
   ```
6. **Confirm removal** — re-scan clean:
   ```bash
   gitleaks detect --source . --redact -v
   detect-secrets scan --baseline .secrets.baseline
   ```
7. **Check for abuse** — review access logs for use of the exposed credential
   during the exposure window.

## Post-Incident

8. **Document the root cause** — how did the secret get committed?
9. **Strengthen controls** — add the pattern to `.gitignore`, extend the
   detect-secrets baseline/plugins, confirm pre-commit gitleaks is installed.
10. **Assess regulatory impact** — GDPR Art. 33 notification within 72 hours if
    personal data was exposed; PCI-DSS incident reporting as applicable.
11. **File a compliance event** — record in `jolarca-compliance`.

> **Rule:** Any secret found in git is an incident. Rotate first, document
> second. "Probably fine" is not a verdict.
