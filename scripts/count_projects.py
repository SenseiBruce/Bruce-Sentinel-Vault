#!/usr/bin/env python3
"""Count top-level project entries in a scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCRIPTS_FILE = Path(__file__).resolve().parent.parent / "scripts.example.json"


def count_projects(payload: Any) -> int:
    if isinstance(payload, list):
        return sum(1 for entry in payload if isinstance(entry, dict))
    if isinstance(payload, dict):
        return 1
    return 0


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
    total = count_projects(load_scripts(args.scripts_file))
    json.dump({"project_count": total}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
