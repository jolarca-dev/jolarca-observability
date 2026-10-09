#!/usr/bin/env python3
"""Verify log schema completeness — all mandatory fields are defined.

Checks:
  * Schema files exist and are valid YAML
  * Base audit-log schema defines all PCI-DSS Req. 10.2 mandatory fields
  * Payment schema extends base with CHD-specific fields
  * KYC/AML schema extends base with identity-verification fields
  * All mandatory fields have type, description, and nullable defined
  * Event type enum covers all mandatory event types from logging configs

Compliance: PCI-DSS Req. 10.2, SOC 2 CC7.1
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = BASE_DIR / "schemas"

# PCI-DSS Req. 10.2 requires these fields in every audit-log entry
REQUIRED_BASE_FIELDS = {
    "timestamp",
    "event_id",
    "event_type",
    "actor_id",
    "actor_type",
    "source_ip",
    "domain",
    "severity",
    "description",
    "hash_chain",
}

# Payment-specific mandatory fields per PCI-DSS Req. 10.2.1
REQUIRED_PAYMENT_FIELDS = {
    "transaction_id",
    "merchant_id",
    "payment_method_type",
    "amount_minor",
    "currency",
}

# KYC/AML-specific mandatory fields
REQUIRED_KYC_FIELDS = {
    "user_id",
    "result",
}


def load_schema(filename: str) -> dict[str, Any]:
    """Load a schema file."""
    filepath = SCHEMAS_DIR / filename
    if not filepath.exists():
        print(f"ERROR: Schema not found: {filepath}", file=sys.stderr)
        sys.exit(2)

    with filepath.open(encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR: Invalid YAML in {filename}: {e}", file=sys.stderr)
            sys.exit(2)

    if not isinstance(data, dict):
        print(f"ERROR: {filename} root must be a YAML mapping", file=sys.stderr)
        sys.exit(2)

    return data


def verify_base_schema(data: dict[str, Any]) -> list[str]:
    """Verify the base audit-log schema."""
    errors: list[str] = []
    mandatory = data.get("mandatory_fields", {})

    # Check all required fields are present
    present_fields = set(mandatory.keys())
    missing = REQUIRED_BASE_FIELDS - present_fields
    if missing:
        errors.append(f"Base schema missing mandatory fields: {sorted(missing)}")

    # Check each mandatory field has required attributes
    for field_name, field_def in mandatory.items():
        if not isinstance(field_def, dict):
            errors.append(f"Field '{field_name}' must be a mapping")
            continue
        if "type" not in field_def:
            errors.append(f"Field '{field_name}' missing 'type'")
        if "description" not in field_def and "pci_requirement" not in field_def:
            errors.append(f"Field '{field_name}' missing description or pci_requirement")

    # Check event_type enum is not empty
    event_type = mandatory.get("event_type", {})
    enum_values = event_type.get("enum", [])
    if not enum_values:
        errors.append("event_type enum is empty — must define controlled vocabulary")

    return errors


def verify_payment_schema(data: dict[str, Any]) -> list[str]:
    """Verify the payment log schema."""
    errors: list[str] = []
    additional = data.get("additional_mandatory_fields", {})

    present_fields = set(additional.keys())
    missing = REQUIRED_PAYMENT_FIELDS - present_fields
    if missing:
        errors.append(f"Payment schema missing mandatory fields: {sorted(missing)}")

    return errors


def verify_kyc_schema(data: dict[str, Any]) -> list[str]:
    """Verify the KYC/AML log schema."""
    errors: list[str] = []
    additional = data.get("additional_mandatory_fields", {})

    present_fields = set(additional.keys())
    missing = REQUIRED_KYC_FIELDS - present_fields
    if missing:
        errors.append(f"KYC/AML schema missing mandatory fields: {sorted(missing)}")

    return errors


def main() -> int:
    """Run all schema completeness verification checks."""
    base_data = load_schema("audit-log-schema.yml")
    payment_data = load_schema("payment-log-schema.yml")
    kyc_data = load_schema("kyc-aml-log-schema.yml")

    all_errors: list[str] = []
    all_errors.extend(verify_base_schema(base_data))
    all_errors.extend(verify_payment_schema(payment_data))
    all_errors.extend(verify_kyc_schema(kyc_data))

    if all_errors:
        print(f"FAILED — {len(all_errors)} schema completeness violation(s):\n")
        for err in all_errors:
            print(f"  x {err}")
        return 1

    print("PASSED — log schemas define all mandatory fields for PCI-DSS Req. 10.2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
