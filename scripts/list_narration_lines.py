#!/usr/bin/env python3
"""List scene narration lines from a scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCRIPTS_FILE = Path(__file__).resolve().parent.parent / "scripts.example.json"


def list_narration_lines(payload: Any) -> list[str]:
    entries = payload if isinstance(payload, list) else [payload]
    lines: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        scenes = entry.get("scenes") or []
        if not isinstance(scenes, list):
            continue
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            narration = scene.get("narration")
            if isinstance(narration, str) and narration.strip():
                lines.append(narration.strip())
    return lines


def load_scripts(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Unable to read scripts file {path}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scripts-file",
        type=Path,
        default=DEFAULT_SCRIPTS_FILE,
        help="Path to scripts JSON",
    )
    args = parser.parse_args(argv)
    lines = list_narration_lines(load_scripts(args.scripts_file))
    json.dump({"count": len(lines), "narration": lines}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
