#!/usr/bin/env python3
"""Count scenes in a video-factory scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "scripts.example.json"


def scene_count_for_entry(entry: Any) -> int:
    if not isinstance(entry, dict):
        return 0
    scenes = entry.get("scenes")
    if isinstance(scenes, list):
        return len(scenes)
    return 0


def count_script_scenes(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, list):
        return {"scripts": 0, "scenes": 0, "entries": []}
    entries: list[dict[str, Any]] = []
    total = 0
    for index, entry in enumerate(payload):
        scenes = scene_count_for_entry(entry)
        total += scenes
        name = ""
        if isinstance(entry, dict) and isinstance(entry.get("project_name"), str):
            name = entry["project_name"]
        entries.append({"index": index, "project_name": name, "scenes": scenes})
    return {"scripts": len(payload), "scenes": total, "entries": entries}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count scenes in scripts JSON")
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
    print(json.dumps(count_script_scenes(payload), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
