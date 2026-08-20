"""Simple token-bucket style rate limiter for CLI bursts."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class RateLimiter:
    rate: float = 5.0
    capacity: float = 5.0
    tokens: float = field(init=False)
    updated_at: float = field(init=False)

    def __post_init__(self) -> None:
        if self.rate <= 0 or self.capacity <= 0:
            raise ValueError("rate and capacity must be positive")
        self.tokens = self.capacity
        self.updated_at = time.monotonic()

    def allow(self, now: float | None = None) -> bool:
        ts = time.monotonic() if now is None else now
        elapsed = max(0.0, ts - self.updated_at)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.updated_at = ts
        if self.tokens < 1.0:
            return False
        self.tokens -= 1.0
        return True
