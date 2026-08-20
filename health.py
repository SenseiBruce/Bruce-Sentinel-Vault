"""Lightweight health / readiness helpers for local and container checks."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HealthStatus:
    status: str
    service: str
    version: str
    checks: dict[str, str]


def build_health(
    *,
    scripts_file: str | None = None,
    version: str = "0.1.1",
) -> HealthStatus:
    """Return a structured health payload without calling external APIs."""
    checks: dict[str, str] = {
        "python": "ok",
        "cwd": "ok" if Path.cwd().exists() else "fail",
    }
    target = scripts_file or os.environ.get("SCRIPTS_FILE") or "scripts.example.json"
    checks["scripts_file"] = "ok" if Path(target).exists() else "missing"
    status = "ok" if checks["scripts_file"] == "ok" else "degraded"
    return HealthStatus(
        status=status,
        service="bruce-sentinel-vault",
        version=version,
        checks=checks,
    )


def health_json(**kwargs: object) -> str:
    return json.dumps(asdict(build_health(**kwargs)), indent=2)  # type: ignore[arg-type]


def main() -> int:
    print(health_json())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
