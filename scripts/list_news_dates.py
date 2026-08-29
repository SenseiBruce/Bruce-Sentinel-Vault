#!/usr/bin/env python3
"""List news dates from a grader news JSON list."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DATE_KEYS = ("date", "published", "published_at", "publishedAt")


def _entry_date(entry: dict[str, Any]) -> str | None:
    for key in DATE_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def list_news_dates(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    dates: list[str] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        found = _entry_date(entry)
        if found is not None:
            dates.append(found)
    return dates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List news item dates")
    parser.add_argument("file", help="Path to news JSON list")
    args = parser.parse_args(argv)
    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {path}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"dates": list_news_dates(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
