"""Tests for retry helper."""

from __future__ import annotations

import pytest

from sentinel_retry import RetryError, retry_call


def test_retry_succeeds_without_retry():
    assert retry_call(lambda: 42, attempts=3) == 42


def test_retry_recovers_after_transient_failure():
    state = {"n": 0}
    sleeps: list[float] = []

    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise ConnectionError("boom")
        return "ok"

    assert (
        retry_call(flaky, attempts=3, base_delay=0.01, sleeper=sleeps.append) == "ok"
    )
    assert state["n"] == 3
    assert sleeps == [0.01, 0.02]


def test_retry_raises_after_exhaustion():
    with pytest.raises(RetryError, match="failed after 2"):
        retry_call(lambda: (_ for _ in ()).throw(TimeoutError("x")), attempts=2, sleeper=lambda _: None)


def test_retry_rejects_invalid_attempts():
    with pytest.raises(ValueError):
        retry_call(lambda: 1, attempts=0)
