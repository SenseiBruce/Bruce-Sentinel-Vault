#!/usr/bin/env python3
"""List HTTP(S) news URLs from a grader news JSON list."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def list_news_urls(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    urls: list[str] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        url = entry.get("url")
        if not isinstance(url, str):
            continue
        cleaned = url.strip()
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
            urls.append(cleaned)
    return urls


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List news item URLs")
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
    print(json.dumps({"urls": list_news_urls(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
