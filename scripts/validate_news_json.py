#!/usr/bin/env python3
"""Validate a grader news JSON list against NewsItem schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "grader-agent" / "src"))

from schemas import SchemaError, parse_news_items  # noqa: E402


def validate_file(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 1, f"File not found: {path}"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return 1, f"Invalid JSON in {path}: {exc}"
    try:
        items = parse_news_items(raw)
    except SchemaError as exc:
        return 1, f"Invalid news JSON: {exc}"
    return 0, f"{path}: {len(items)} news item(s) valid"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate grader news JSON")
    parser.add_argument("file", help="Path to news JSON list")
    args = parser.parse_args(argv)
    code, message = validate_file(Path(args.file))
    print(message, file=sys.stdout if code == 0 else sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
