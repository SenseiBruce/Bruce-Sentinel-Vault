"""Smoke test that the committed lockfile installs cleanly."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_poetry_lock_exists():
    assert (ROOT / "poetry.lock").exists()


def test_requirements_lock_install_dry_run():
    lock = ROOT / "requirements.lock"
    assert lock.exists()
    # Resolve packages without mutating the active environment.
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--dry-run", "-r", str(lock)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
