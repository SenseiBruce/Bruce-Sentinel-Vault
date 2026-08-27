#!/usr/bin/env python3
"""Validate a video-factory scripts JSON file against ScriptEntry schema."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "grader-agent" / "src"))

from schemas import SchemaError, parse_script_entries  # noqa: E402


def validate_file(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 1, f"File not found: {path}"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return 1, f"Invalid JSON in {path}: {exc}"
    try:
        entries = parse_script_entries(raw)
    except SchemaError as exc:
        return 1, f"Invalid scripts JSON: {exc}"
    return 0, f"{path}: {len(entries)} script(s) valid"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate scripts JSON used by produce_video.py"
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=str(ROOT / "scripts.example.json"),
        help="Path to scripts JSON (default: scripts.example.json)",
    )
    args = parser.parse_args(argv)
    code, message = validate_file(Path(args.file))
    stream = sys.stdout if code == 0 else sys.stderr
    print(message, file=stream)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
