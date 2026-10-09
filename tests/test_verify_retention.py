"""Tests for verify_retention.py — retention policy verification."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT = BASE_DIR / "scripts" / "verify_retention.py"


def test_retention_script_exists() -> None:
    """The retention verification script must exist."""
    assert SCRIPT.exists(), f"Script not found: {SCRIPT}"


def test_retention_script_runs_clean() -> None:
    """The retention verification script must pass against current configs."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    assert result.returncode == 0, (
        f"Retention verification failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_retention_policy_file_exists() -> None:
    """The retention policy YAML must exist."""
    policy = BASE_DIR / "audit-trail" / "retention" / "retention-policy.yml"
    assert policy.exists(), f"Retention policy not found: {policy}"
