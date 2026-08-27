#!/usr/bin/env python3
"""Count narration words in a video-factory scripts JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "scripts.example.json"


def word_count(text: str) -> int:
    return len(text.split())


def summarize(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, list):
        return {"scripts": 0, "scenes": 0, "words": 0, "by_project": []}
    by_project: list[dict[str, Any]] = []
    scenes = 0
    words = 0
    for item in payload:
        if not isinstance(item, dict):
            continue
        name = str(item.get("project_name") or "untitled")
        project_words = 0
        project_scenes = item.get("scenes")
        if isinstance(project_scenes, list):
            for scene in project_scenes:
                scenes += 1
                if isinstance(scene, dict) and isinstance(scene.get("narration"), str):
                    project_words += word_count(scene["narration"])
        words += project_words
        by_project.append({"project_name": name, "words": project_words})
    return {"scripts": len(by_project), "scenes": scenes, "words": words, "by_project": by_project}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count narration words in scripts JSON")
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
    print(json.dumps(summarize(payload)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
