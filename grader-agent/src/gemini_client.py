"""Thin Gemini client used by the grader agent.

Supports dependency injection so tests can supply a fake without network access.
"""

from __future__ import annotations

import logging
import os
from typing import Protocol

import requests

logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    def generate_response(self, messages: list[dict]) -> str:  # pragma: no cover - protocol
        ...


class GeminiClient:
    """Minimal HTTP client for a Gemini-compatible generate endpoint."""

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.0-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = model
        self.base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

    def generate_response(self, messages: list[dict]) -> str:
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Export it or inject a mock LLMClient."
            )

        # Convert chat-style messages into a single Gemini user prompt.
        prompt = "\n".join(
            f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(
            self.base_url,
            params={"key": self.api_key},
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            logger.exception("Unexpected Gemini response shape")
            raise RuntimeError(f"Unexpected Gemini response: {data}") from exc
