#!/usr/bin/env python3
"""Count nonempty news dates from a grader news JSON list."""

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


def count_news_dates(payload: Any) -> int:
    if not isinstance(payload, list):
        return 0
    total = 0
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        if _entry_date(entry) is not None:
            total += 1
    return total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count news item dates")
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
    print(json.dumps({"date_count": count_news_dates(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
