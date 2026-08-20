"""Tests for path sanitization."""

from __future__ import annotations

from pathlib import Path

import pytest

from sentinel_paths import PathValidationError, resolve_under


def test_resolve_under_allows_relative_child(tmp_path: Path):
    child = tmp_path / "a.txt"
    child.write_text("x", encoding="utf-8")
    assert resolve_under(tmp_path, "a.txt") == child.resolve()


def test_resolve_under_rejects_escape(tmp_path: Path):
    with pytest.raises(PathValidationError):
        resolve_under(tmp_path, "../outside.txt")
