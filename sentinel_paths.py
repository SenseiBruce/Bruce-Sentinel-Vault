"""Path sanitization helpers for user-supplied file arguments."""

from __future__ import annotations

from pathlib import Path


class PathValidationError(ValueError):
    """Raised when a path escapes the allowed root."""


def resolve_under(root: str | Path, user_path: str | Path) -> Path:
    """Resolve `user_path` and ensure it stays under `root`."""
    base = Path(root).resolve()
    target = (base / user_path).resolve() if not Path(user_path).is_absolute() else Path(user_path).resolve()
    try:
        target.relative_to(base)
    except ValueError as exc:
        raise PathValidationError(f"path escapes root: {user_path}") from exc
    return target
