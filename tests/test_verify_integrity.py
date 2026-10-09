"""Tests for verify_integrity.py — hash-chain integrity verification."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT = BASE_DIR / "scripts" / "verify_integrity.py"


def test_integrity_script_exists() -> None:
    """The integrity verification script must exist."""
    assert SCRIPT.exists(), f"Script not found: {SCRIPT}"


def test_integrity_script_runs_clean() -> None:
    """The integrity verification script must pass against current configs."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
    )
    assert result.returncode == 0, (
        f"Integrity verification failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_hash_chain_config_exists() -> None:
    """The hash-chain configuration YAML must exist."""
    config = BASE_DIR / "audit-trail" / "integrity" / "hash-chain.yml"
    assert config.exists(), f"Hash-chain config not found: {config}"
