#!/usr/bin/env python3
"""List news verdicts from a grader news JSON list."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def list_news_verdicts(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    verdicts: list[str] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        verdict = entry.get("verdict")
        if isinstance(verdict, str) and verdict.strip():
            verdicts.append(verdict.strip())
    return verdicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List news item verdicts")
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
    print(json.dumps({"verdicts": list_news_verdicts(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
