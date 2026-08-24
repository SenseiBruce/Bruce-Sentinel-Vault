"""Tests for YouTubeAuditor token path defaults and injected client usage."""

from __future__ import annotations

import json
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
        payload = self.channel_payload

        class Channels:
            def list(self, **kwargs):
                return FakeExecute(payload)

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


def test_list_pipeline_with_injected_client():
    class RichFake(FakeYouTube):
        def playlistItems(self):

            class Playlist:
                def list(self, **kwargs):
                    return FakeExecute(
                        {
                            "items": [
                                {
                                    "contentDetails": {"videoId": "abc"},
                                    "snippet": {"title": "Tax Explainer"},
                                    "status": {"privacyStatus": "public"},
                                }
                            ]
                        }
                    )

            return Playlist()

        def videos(self):
            class Videos:
                def list(self, **kwargs):
                    return FakeExecute(
                        {
                            "items": [
                                {
                                    "status": {
                                        "privacyStatus": "public",
                                        "publishAt": "N/A",
                                    },
                                    "snippet": {"title": "Tax Explainer"},
                                    "statistics": {"viewCount": "9", "likeCount": "2"},
                                }
                            ]
                        }
                    )

            return Videos()

    auditor = YouTubeAuditor(youtube_client=RichFake())
    pipeline = auditor.list_pipeline(max_results=1)
    assert pipeline[0]["video_id"] == "abc"
    stats = auditor.get_detailed_stats(max_results=1)
    assert stats[0]["views"] == "9"


def test_build_report_and_json_cli(monkeypatch, capsys):
    from YouTubeAuditor import main as auditor_main

    class RichFake(FakeYouTube):
        def playlistItems(self):

            class Playlist:
                def list(self, **kwargs):
                    return FakeExecute(
                        {
                            "items": [
                                {
                                    "contentDetails": {"videoId": "abc"},
                                    "snippet": {"title": "Tax Explainer"},
                                    "status": {"privacyStatus": "public"},
                                }
                            ]
                        }
                    )

            return Playlist()

        def videos(self):
            class Videos:
                def list(self, **kwargs):
                    return FakeExecute(
                        {
                            "items": [
                                {
                                    "status": {
                                        "privacyStatus": "public",
                                        "publishAt": "N/A",
                                    },
                                    "snippet": {"title": "Tax Explainer"},
                                    "statistics": {"viewCount": "9", "likeCount": "2"},
                                }
                            ]
                        }
                    )

            return Videos()

    auditor = YouTubeAuditor(youtube_client=RichFake())
    report = auditor.build_report(max_results=1)
    assert report["channel"]["title"] == "Capital Architects"
    assert report["pipeline"][0]["video_id"] == "abc"
    assert report["stats"][0]["views"] == "9"

    monkeypatch.setattr(
        "YouTubeAuditor.YouTubeAuditor",
        lambda token_file=None, youtube_client=None: auditor,
    )
    auditor_main(["--json", "--max-results", "1"])
    payload = json.loads(capsys.readouterr().out)
    assert payload["channel"]["title"] == "Capital Architects"
