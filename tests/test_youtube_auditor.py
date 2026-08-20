"""Tests for YouTubeAuditor token path defaults and injected client usage."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from YouTubeAuditor import TokenError, YouTubeAuditor, default_token_file  # noqa: E402


class FakeExecute:
    def __init__(self, payload):
        self.payload = payload

    def execute(self):
        return self.payload


class FakeYouTube:
    def __init__(self):
        self.channel_payload = {
            "items": [
                {
                    "snippet": {
                        "title": "Capital Architects",
                        "description": "Finance channel " * 10,
                    },
                    "statistics": {
                        "subscriberCount": "1000",
                        "viewCount": "50000",
                        "videoCount": "12",
                    },
                    "contentDetails": {
                        "relatedPlaylists": {"uploads": "UPLOADS"}
                    },
                }
            ]
        }

    def channels(self):
        parent = self

        class Channels:
            def list(self, **kwargs):
                return FakeExecute(parent.channel_payload)

        return Channels()


def test_default_token_file_env(monkeypatch, tmp_path):
    token = tmp_path / "tok.json"
    monkeypatch.setenv("YOUTUBE_TOKEN_FILE", str(token))
    assert default_token_file() == str(token)


def test_missing_token_raises(tmp_path):
    with pytest.raises(TokenError, match="No token found"):
        YouTubeAuditor(token_file=str(tmp_path / "missing.json"))


def test_get_channel_summary_with_injected_client():
    auditor = YouTubeAuditor(youtube_client=FakeYouTube())
    summary = auditor.get_channel_summary()
    assert summary["title"] == "Capital Architects"
    assert summary["subscribers"] == "1000"
