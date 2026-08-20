"""Shared pytest fixtures: dummy secrets and network isolation defaults."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _dummy_api_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure no test accidentally relies on real operator credentials."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    monkeypatch.setenv("RUNWARE_API_KEY", "test-runware-key")
    monkeypatch.setenv("MATON_KEY", "test-maton-key")
    monkeypatch.setenv("OLLAMA_URL", "http://127.0.0.1:9/api/generate")
