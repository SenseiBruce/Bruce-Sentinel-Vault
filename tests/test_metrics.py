"""Tests for in-memory metrics registry."""

from __future__ import annotations

import pytest

from sentinel_metrics import MetricsRegistry


def test_incr_and_snapshot():
    registry = MetricsRegistry()
    assert registry.incr("grade.pass") == 1
    assert registry.incr("grade.pass", 2) == 3
    assert registry.get("grade.pass") == 3
    assert registry.snapshot() == {"grade.pass": 3}


def test_reset_and_reject_negative():
    registry = MetricsRegistry()
    registry.incr("x")
    registry.reset()
    assert registry.snapshot() == {}
    with pytest.raises(ValueError):
        registry.incr("x", -1)
