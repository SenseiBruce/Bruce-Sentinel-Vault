"""Unit tests for Shadow-Coder Ollama response parsing and HTTP handling."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shadow-coder"))

from coder import (  # noqa: E402
    OllamaError,
    get_file_content,
    parse_ollama_response,
    run_shadow_coder,
)


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_parse_ollama_response_extracts_text():
    assert parse_ollama_response({"response": "def hello():\n    pass"}) == (
        "def hello():\n    pass"
    )


def test_parse_ollama_response_missing_key():
    assert parse_ollama_response({}) == "No response from model."


def test_get_file_content_reads_and_handles_missing(tmp_path):
    target = tmp_path / "sample.py"
    target.write_text("print('hi')\n", encoding="utf-8")
    assert "print('hi')" in get_file_content(str(target))
    with pytest.raises(OllamaError, match="Error reading"):
        get_file_content(str(tmp_path / "nope.py"))


def test_run_shadow_coder_posts_payload_and_parses_response(tmp_path):
    sample = tmp_path / "mod.py"
    sample.write_text("x = 1\n", encoding="utf-8")
    captured = {}

    def fake_post(url, json=None, timeout=None):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse({"response": "FILE: mod.py\n```\nx = 2\n```"})

    result = run_shadow_coder(
        "bump x",
        [str(sample)],
        model="qwen2.5:7b",
        ollama_url="http://ollama.test/api/generate",
        post=fake_post,
    )

    assert "x = 2" in result
    assert captured["url"] == "http://ollama.test/api/generate"
    assert captured["json"]["model"] == "qwen2.5:7b"
    assert "bump x" in captured["json"]["prompt"]
    assert "x = 1" in captured["json"]["prompt"]
    assert captured["timeout"] == 300


def test_run_shadow_coder_raises_on_http_failure():
    def boom_post(url, json=None, timeout=None):
        raise ConnectionError("refused")

    with pytest.raises(OllamaError, match="refused"):
        run_shadow_coder("task", [], post=boom_post)