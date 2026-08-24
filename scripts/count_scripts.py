#!/usr/bin/env python3
"""Count script entries in a video-factory scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "scripts.example.json"


def count_scripts(payload: Any) -> int:
    if not isinstance(payload, list):
        return 0
    return len(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count script entries")
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
    print(json.dumps({"scripts": count_scripts(payload)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
