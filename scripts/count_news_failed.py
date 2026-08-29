#!/usr/bin/env python3
"""Count news items with a FAILED verdict."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def count_news_failed(payload: Any) -> int:
    if not isinstance(payload, list):
        return 0
    total = 0
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        verdict = entry.get("verdict")
        if isinstance(verdict, str) and verdict.strip().upper() == "FAILED":
            total += 1
    return total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count news items that failed")
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
    print(json.dumps({"failed_count": count_news_failed(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
