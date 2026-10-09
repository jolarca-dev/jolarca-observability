"""Tests for verify_completeness.py — log schema completeness verification."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT = BASE_DIR / "scripts" / "verify_completeness.py"


def test_completeness_script_exists() -> None:
    """The completeness verification script must exist."""
    assert SCRIPT.exists(), f"Script not found: {SCRIPT}"


def test_completeness_script_runs_clean() -> None:
    """The completeness verification script must pass against current configs."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    assert result.returncode == 0, (
        f"Completeness verification failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_schema_files_exist() -> None:
    """All schema YAML files must exist."""
    schemas_dir = BASE_DIR / "schemas"
    assert (schemas_dir / "audit-log-schema.yml").exists()
    assert (schemas_dir / "payment-log-schema.yml").exists()
    assert (schemas_dir / "kyc-aml-log-schema.yml").exists()
