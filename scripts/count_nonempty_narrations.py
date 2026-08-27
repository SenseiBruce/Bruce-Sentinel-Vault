#!/usr/bin/env python3
"""Count scenes with a nonempty narration in a scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCRIPTS_FILE = Path(__file__).resolve().parent.parent / "scripts.example.json"


def _is_nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def count_nonempty_narrations(payload: Any) -> int:
    entries = payload if isinstance(payload, list) else [payload]
    total = 0
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        scenes = entry.get("scenes") or []
        if not isinstance(scenes, list):
            continue
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            if _is_nonempty(scene.get("narration")):
                total += 1
    return total


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
    total = count_nonempty_narrations(load_scripts(args.scripts_file))
    json.dump({"nonempty_narration_count": total}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
