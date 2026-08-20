"""Tests for VideoFactory configuration and script loading (no network)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from produce_video import (  # noqa: E402
    ConfigurationError,
    VideoFactory,
    _require_env,
    default_scripts_file,
)


def test_require_env_missing(monkeypatch):
    monkeypatch.delenv("RUNWARE_API_KEY", raising=False)
    with pytest.raises(ConfigurationError, match="RUNWARE_API_KEY"):
        _require_env("RUNWARE_API_KEY")


def test_require_env_present(monkeypatch):
    monkeypatch.setenv("RUNWARE_API_KEY", "secret")
    assert _require_env("RUNWARE_API_KEY") == "secret"


def test_default_scripts_file_uses_env(monkeypatch, tmp_path):
    path = tmp_path / "scripts.json"
    monkeypatch.setenv("SCRIPTS_FILE", str(path))
    assert default_scripts_file() == str(path)


def test_video_factory_loads_scripts(tmp_path):
    scripts = [{"project_name": "Demo", "scenes": []}]
    path = tmp_path / "scripts.json"
    path.write_text(json.dumps(scripts), encoding="utf-8")
    factory = VideoFactory(str(path), tts=object(), youtube_factory=lambda i, t: object())
    assert factory.scripts == scripts


def test_video_factory_missing_file(tmp_path):
    with pytest.raises(ConfigurationError, match="not found"):
        VideoFactory(str(tmp_path / "missing.json"))


def test_video_factory_invalid_index(tmp_path):
    path = tmp_path / "scripts.json"
    path.write_text(json.dumps([{"project_name": "A", "scenes": []}]), encoding="utf-8")
    factory = VideoFactory(str(path), tts=object(), youtube_factory=lambda i, t: object())
    with pytest.raises(ConfigurationError, match="Invalid index"):
        factory.produce(0)


def test_video_factory_dry_run(tmp_path):
    path = tmp_path / "scripts.json"
    path.write_text(
        json.dumps(
            [{"project_name": "Demo", "scenes": [{"narration": "a", "image_prompt": "b"}]}]
        ),
        encoding="utf-8",
    )
    factory = VideoFactory(str(path), tts=object(), youtube_factory=lambda i, t: object())
    plan = factory.produce(1, dry_run=True)
    assert plan["dry_run"] is True
    assert plan["scene_count"] == 1

