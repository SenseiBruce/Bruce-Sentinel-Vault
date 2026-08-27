"""Tests for structured logging and health helpers."""

from __future__ import annotations

import json
import logging

from health import build_health, health_json
from sentinel_logging import JsonFormatter, configure_logging


def test_json_formatter_emits_object():
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello %s",
        args=("world",),
        exc_info=None,
    )
    payload = json.loads(JsonFormatter().format(record))
    assert payload["msg"] == "hello world"
    assert payload["level"] == "INFO"
    assert "ts" in payload


def test_configure_logging_idempotent():
    configure_logging()
    configure_logging()
    assert logging.getLogger().handlers


def test_health_ok_with_example_scripts():
    status = build_health(scripts_file="scripts.example.json")
    assert status.status == "ok"
    assert status.checks["scripts_file"] == "ok"
    assert '"status": "ok"' in health_json(scripts_file="scripts.example.json")


def test_health_text_lists_checks():
    from health import health_text

    text = health_text(scripts_file="scripts.example.json")
    assert "status: ok" in text
    assert "scripts_file: ok" in text
    assert "python: ok" in text


def test_health_cli_text_format(capsys):
    from health import main

    assert main(["--scripts-file", "scripts.example.json", "--format", "text"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("status: ok")
    assert "service: bruce-sentinel-vault" in out


def test_health_version_from_env(monkeypatch):
    monkeypatch.setenv("SENTINEL_VERSION", "9.9.9")
    status = build_health(scripts_file="scripts.example.json")
    assert status.version == "9.9.9"


def test_health_cli_fail_on_degraded(tmp_path):
    from health import main

    assert main(["--scripts-file", "scripts.example.json"]) == 0
    assert main(["--scripts-file", str(tmp_path / "missing.json"), "--fail-on-degraded"]) == 1
