"""Small retry helper with exponential backoff for flaky HTTP/API calls."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class RetryError(RuntimeError):
    """Raised when all retry attempts are exhausted."""


def retry_call(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    base_delay: float = 0.05,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleeper: Callable[[float], None] = time.sleep,
) -> T:
    """Call `fn` up to `attempts` times with exponential backoff."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    last: BaseException | None = None
    for index in range(attempts):
        try:
            return fn()
        except retry_on as exc:  # noqa: PERF203 - intentional retry loop
            last = exc
            if index == attempts - 1:
                break
            sleeper(base_delay * (2**index))
    assert last is not None
    raise RetryError(f"failed after {attempts} attempts: {last}") from last
