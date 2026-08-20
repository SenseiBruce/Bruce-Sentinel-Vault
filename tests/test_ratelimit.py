"""Tests for RateLimiter."""

from __future__ import annotations

import pytest

from sentinel_ratelimit import RateLimiter


def test_rate_limiter_allows_burst_then_blocks():
    limiter = RateLimiter(rate=1.0, capacity=2.0)
    assert limiter.allow(now=100.0) is True
    assert limiter.allow(now=100.0) is True
    assert limiter.allow(now=100.0) is False


def test_rate_limiter_refills():
    limiter = RateLimiter(rate=10.0, capacity=1.0)
    assert limiter.allow(now=0.0) is True
    assert limiter.allow(now=0.0) is False
    assert limiter.allow(now=0.2) is True


def test_rate_limiter_rejects_invalid():
    with pytest.raises(ValueError):
        RateLimiter(rate=0, capacity=1)
