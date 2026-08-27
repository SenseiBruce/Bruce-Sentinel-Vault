#!/usr/bin/env python3
"""List scene image_prompt values from a scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_SCRIPTS_FILE = Path(__file__).resolve().parent.parent / "scripts.example.json"


def list_image_prompts(payload: Any) -> list[str]:
    entries = payload if isinstance(payload, list) else [payload]
    prompts: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        scenes = entry.get("scenes") or []
        if not isinstance(scenes, list):
            continue
        for scene in scenes:
            if not isinstance(scene, dict):
                continue
            prompt = scene.get("image_prompt")
            if isinstance(prompt, str) and prompt.strip():
                prompts.append(prompt.strip())
    return prompts


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
        help="Path to scripts JSON (list of project entries)",
    )
    args = parser.parse_args(argv)
    prompts = list_image_prompts(load_scripts(args.scripts_file))
    json.dump({"count": len(prompts), "image_prompts": prompts}, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
