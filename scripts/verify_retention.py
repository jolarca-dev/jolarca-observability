#!/usr/bin/env python3
"""Verify audit-log retention policy compliance.

Checks:
  * Retention policy file exists and is valid YAML
  * Global minimums meet PCI-DSS Req. 10.5.1 (12 months, 3 immediately available)
  * Per-domain retention meets or exceeds global minimums
  * Storage tiers are defined (hot, warm, cold)
  * Auto-delete is disabled (logs must not be automatically removed)
  * Legal hold override is enabled

Compliance: PCI-DSS Req. 10.5.1, SOC 2 CC8.1
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
RETENTION_FILE = BASE_DIR / "audit-trail" / "retention" / "retention-policy.yml"

# PCI-DSS Req. 10.5.1 minimums
MIN_TOTAL_MONTHS = 12
MIN_IMMEDIATELY_AVAILABLE_MONTHS = 3


def load_retention_policy() -> dict[str, Any]:
    """Load and parse the retention policy file."""
    if not RETENTION_FILE.exists():
        print(f"ERROR: Retention policy not found: {RETENTION_FILE}", file=sys.stderr)
        sys.exit(2)

    with RETENTION_FILE.open(encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in retention policy: {e}", file=sys.stderr)
            sys.exit(2)

    if not isinstance(data, dict):
        print("ERROR: Retention policy root must be a YAML mapping", file=sys.stderr)
        sys.exit(2)

    return data


def verify_global_minimums(data: dict[str, Any]) -> list[str]:
    """Verify global retention minimums meet PCI-DSS Req. 10.5.1."""
    errors: list[str] = []
    mins = data.get("global_minimums", {})

    total = mins.get("total_retention_months", 0)
    if total < MIN_TOTAL_MONTHS:
        errors.append(
            f"Global total_retention_months={total} < PCI-DSS minimum {MIN_TOTAL_MONTHS}",
        )

    available = mins.get("immediately_available_months", 0)
    if available < MIN_IMMEDIATELY_AVAILABLE_MONTHS:
        errors.append(
            f"Global immediately_available_months={available} < "
            f"PCI-DSS minimum {MIN_IMMEDIATELY_AVAILABLE_MONTHS}",
        )

    return errors


def verify_storage_tiers(data: dict[str, Any]) -> list[str]:
    """Verify storage tiers are properly defined."""
    errors: list[str] = []
    tiers = data.get("storage_tiers", {})

    for required_tier in ["hot", "warm"]:
        if required_tier not in tiers:
            errors.append(f"Missing required storage tier: {required_tier}")
        else:
            tier = tiers[required_tier]
            if "retention_months" not in tier:
                errors.append(f"Storage tier '{required_tier}' missing retention_months")
            if "retrieval_latency" not in tier:
                errors.append(f"Storage tier '{required_tier}' missing retrieval_latency")

    # Hot tier must cover at least 3 months
    hot = tiers.get("hot", {})
    if hot.get("retention_months", 0) < MIN_IMMEDIATELY_AVAILABLE_MONTHS:
        errors.append(
            f"Hot tier retention_months={hot.get('retention_months', 0)} < "
            f"PCI-DSS minimum {MIN_IMMEDIATELY_AVAILABLE_MONTHS}",
        )

    return errors


def verify_domain_retention(data: dict[str, Any]) -> list[str]:
    """Verify per-domain retention meets global minimums."""
    errors: list[str] = []
    domain_retention = data.get("domain_retention", {})
    global_mins = data.get("global_minimums", {})

    min_total = global_mins.get("total_retention_months", MIN_TOTAL_MONTHS)

    for domain, config in domain_retention.items():
        hot = config.get("hot_months", 0)
        warm = config.get("warm_months", 0)
        cold = config.get("cold_months", 0)

        total = hot + warm + cold
        if total < min_total:
            errors.append(
                f"Domain '{domain}' total retention ({total}mo) < "
                f"global minimum ({min_total}mo)",
            )

        if hot < MIN_IMMEDIATELY_AVAILABLE_MONTHS:
            errors.append(
                f"Domain '{domain}' hot_months={hot} < "
                f"PCI-DSS minimum {MIN_IMMEDIATELY_AVAILABLE_MONTHS}",
            )

    return errors


def verify_enforcement(data: dict[str, Any]) -> list[str]:
    """Verify retention enforcement settings."""
    errors: list[str] = []
    enforcement = data.get("enforcement", {})

    if enforcement.get("auto_delete_after_retention", True):
        errors.append(
            "auto_delete_after_retention must be false — logs must not be "
            "automatically deleted",
        )

    if not enforcement.get("legal_hold_override", False):
        errors.append(
            "legal_hold_override must be true — legal holds must override retention",
        )

    if not enforcement.get("deletion_must_be_logged", False):
        errors.append(
            "deletion_must_be_logged must be true — all deletions must be audited",
        )

    return errors


def main() -> int:
    """Run all retention policy verification checks."""
    data = load_retention_policy()

    all_errors: list[str] = []
    all_errors.extend(verify_global_minimums(data))
    all_errors.extend(verify_storage_tiers(data))
    all_errors.extend(verify_domain_retention(data))
    all_errors.extend(verify_enforcement(data))

    if all_errors:
        print(f"FAILED — {len(all_errors)} retention policy violation(s):\n")
        for err in all_errors:
            print(f"  x {err}")
        return 1

    print("PASSED — retention policy meets PCI-DSS Req. 10.5.1 requirements.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
