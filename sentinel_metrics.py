"""In-memory counters for pipeline stage visibility (no external deps)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from threading import Lock


@dataclass
class MetricsRegistry:
    _counts: Counter[str] = field(default_factory=Counter)
    _lock: Lock = field(default_factory=Lock)

    def incr(self, name: str, amount: int = 1) -> int:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        with self._lock:
            self._counts[name] += amount
            return self._counts[name]

    def get(self, name: str) -> int:
        with self._lock:
            return int(self._counts.get(name, 0))

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counts)

    def reset(self) -> None:
        with self._lock:
            self._counts.clear()


# Process-wide default registry used by CLIs when none is injected.
default_metrics = MetricsRegistry()
