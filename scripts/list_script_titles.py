#!/usr/bin/env python3
"""List project titles from a video-factory scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "scripts.example.json"


def list_script_titles(payload: Any) -> list[str]:
    if not isinstance(payload, list):
        return []
    titles: list[str] = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        name = entry.get("project_name")
        if isinstance(name, str) and name.strip():
            titles.append(name.strip())
    return titles


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="List script project titles")
    parser.add_argument(
        "file",
        nargs="?",
        default=str(DEFAULT_FILE),
        help="Path to scripts JSON (default: scripts.example.json)",
    )
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
    print(json.dumps({"titles": list_script_titles(payload)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
