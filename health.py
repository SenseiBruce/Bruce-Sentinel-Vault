"""Lightweight health / readiness helpers for local and container checks."""

from __future__ import annotations

import argparse
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
    version: str | None = None,
) -> HealthStatus:
    """Return a structured health payload without calling external APIs."""
    resolved_version = version or os.environ.get("SENTINEL_VERSION") or "0.1.4"
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
        version=resolved_version,
        checks=checks,
    )


def health_json(**kwargs: object) -> str:
    return json.dumps(asdict(build_health(**kwargs)), indent=2)  # type: ignore[arg-type]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bruce Sentinel Vault health check")
    parser.add_argument(
        "--scripts-file",
        default=None,
        help="Optional scripts JSON path override for the readiness check",
    )
    parser.add_argument(
        "--fail-on-degraded",
        action="store_true",
        help="Exit 1 when status is not ok (useful for container healthchecks)",
    )
    args = parser.parse_args(argv)
    status = build_health(scripts_file=args.scripts_file)
    print(json.dumps(asdict(status), indent=2))
    if args.fail_on_degraded and status.status != "ok":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
