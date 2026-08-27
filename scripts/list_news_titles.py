#!/usr/bin/env python3
"""List news titles from a grader news JSON list."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def list_news_titles(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    titles: list[str] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        title = entry.get("title")
        if isinstance(title, str) and title.strip():
            titles.append(title.strip())
    return titles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List news item titles")
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
    print(json.dumps({"titles": list_news_titles(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
