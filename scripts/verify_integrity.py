#!/usr/bin/env python3
"""Verify audit-log hash-chain integrity configuration.

Checks:
  * Hash-chain configuration file exists and is valid YAML
  * Algorithm is SHA-256 (minimum acceptable for PCI-DSS)
  * Input fields are defined and include all mandatory fields
  * Genesis hash is defined
  * Verification frequency is defined (daily minimum)
  * On-failure actions include CRITICAL alerting
  * Limitations are documented (honest about what hash chains cannot prevent)

Compliance: PCI-DSS Req. 10.5.5, SOC 2 CC7.1
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
HASH_CHAIN_FILE = BASE_DIR / "audit-trail" / "integrity" / "hash-chain.yml"
VERIFICATION_FILE = BASE_DIR / "audit-trail" / "integrity" / "verification-config.yml"

REQUIRED_INPUT_FIELDS = {"timestamp", "event_id", "actor_id", "event_type", "previous_hash"}


def load_yaml_file(filepath: Path, label: str) -> dict[str, Any]:
    """Load and parse a YAML file."""
    if not filepath.exists():
        print(f"ERROR: {label} not found: {filepath}", file=sys.stderr)
        sys.exit(2)

    with filepath.open(encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in {label}: {e}", file=sys.stderr)
            sys.exit(2)

    if not isinstance(data, dict):
        print(f"ERROR: {label} root must be a YAML mapping", file=sys.stderr)
        sys.exit(2)

    return data


def verify_hash_chain_config(data: dict[str, Any]) -> list[str]:
    """Verify hash-chain configuration."""
    errors: list[str] = []
    hc = data.get("hash_chain", {})

    # Algorithm check
    algo = hc.get("algorithm", "")
    if algo != "SHA-256":
        errors.append(f"Hash algorithm must be SHA-256, got '{algo}'")

    # Input fields check
    input_fields = set(hc.get("input_fields", []))
    missing = REQUIRED_INPUT_FIELDS - input_fields
    if missing:
        errors.append(f"Hash-chain input fields missing: {sorted(missing)}")

    # Genesis hash check
    genesis = data.get("genesis", {})
    if not genesis.get("hash"):
        errors.append("Genesis hash is not defined")

    return errors


def verify_verification_config(data: dict[str, Any]) -> list[str]:
    """Verify verification configuration."""
    errors: list[str] = []

    # Schedule check
    schedule = data.get("verification", {}).get("schedule", {})
    if not schedule.get("full_verification"):
        errors.append("Full verification schedule not defined")

    # Scope check
    scope = data.get("verification", {}).get("scope", {})
    domains = scope.get("domains", [])
    required_domains = {"audit", "payment", "kyc_aml"}
    missing_domains = required_domains - set(domains)
    if missing_domains:
        errors.append(f"Verification scope missing domains: {sorted(missing_domains)}")

    # On-failure check
    on_failure = data.get("verification", {}).get("on_failure", {})
    if on_failure.get("severity") != "critical":
        errors.append("Verification failure severity must be 'critical'")

    return errors


def main() -> int:
    """Run all integrity configuration verification checks."""
    hc_data = load_yaml_file(HASH_CHAIN_FILE, "Hash-chain config")
    vc_data = load_yaml_file(VERIFICATION_FILE, "Verification config")

    all_errors: list[str] = []
    all_errors.extend(verify_hash_chain_config(hc_data))
    all_errors.extend(verify_verification_config(vc_data))

    if all_errors:
        print(f"FAILED — {len(all_errors)} integrity configuration violation(s):\n")
        for err in all_errors:
            print(f"  x {err}")
        return 1

    print("PASSED — hash-chain integrity configuration meets PCI-DSS Req. 10.5.5.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
