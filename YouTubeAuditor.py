"""YouTube channel auditor using OAuth credentials from a token file."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from sentinel_logging import configure_logging

logger = logging.getLogger(__name__)


class TokenError(RuntimeError):
    """Raised when the YouTube OAuth token cannot be loaded."""


def default_token_file() -> str:
    return os.environ.get(
        "YOUTUBE_TOKEN_FILE",
        str(Path(__file__).resolve().parent / "youtube_token.json"),
    )


class YouTubeAuditor:
    def __init__(self, token_file=None, youtube_client=None):
        self.token_file = token_file or default_token_file()
        self.credentials = None
        self._youtube_client = youtube_client
        if youtube_client is None:
            self._load_credentials()

    def _load_credentials(self):
        if not os.path.exists(self.token_file):
            raise TokenError(
                f"No token found at {self.token_file}. "
                "Set YOUTUBE_TOKEN_FILE or place youtube_token.json in the repo root."
            )
        with open(self.token_file, encoding="utf-8") as token_file:
            creds_data = json.load(token_file)
            self.credentials = Credentials.from_authorized_user_info(creds_data)

    def _youtube(self):
        if self._youtube_client is not None:
            return self._youtube_client
        if not self.credentials:
            raise TokenError("YouTube credentials are not loaded.")
        return build("youtube", "v3", credentials=self.credentials)

    def _uploads_playlist_id(self) -> str:
        youtube = self._youtube()
        response = youtube.channels().list(part="contentDetails", mine=True).execute()
        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def _list_upload_items(self, max_results: int) -> list[dict[str, Any]]:
        youtube = self._youtube()
        playlist_id = self._uploads_playlist_id()
        response = (
            youtube.playlistItems()
            .list(
                part="snippet,contentDetails,status",
                playlistId=playlist_id,
                maxResults=max_results,
            )
            .execute()
        )
        return list(response.get("items", []))

    def get_channel_summary(self):
        youtube = self._youtube()
        response = (
            youtube.channels()
            .list(part="snippet,contentDetails,statistics", mine=True)
            .execute()
        )

        if not response.get("items"):
            logger.error("No channel found for authenticated account")
            return None

        channel = response["items"][0]
        snippet = channel["snippet"]
        stats = channel["statistics"]
        summary = {
            "title": snippet["title"],
            "subscribers": stats.get("subscriberCount", "Hidden"),
            "views": stats.get("viewCount", "0"),
            "video_count": stats.get("videoCount", "0"),
            "description": snippet.get("description", "")[:100],
        }
        logger.info(
            "Channel %s — subs=%s views=%s videos=%s",
            summary["title"],
            summary["subscribers"],
            summary["views"],
            summary["video_count"],
        )
        return summary

    def list_pipeline(self, max_results=10):
        youtube = self._youtube()
        pipeline = []
        for item in self._list_upload_items(max_results):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            vid_res = youtube.videos().list(part="status,snippet", id=video_id).execute()
            status = vid_res["items"][0]["status"]
            privacy = status["privacyStatus"]
            pub_at = status.get("publishAt", "N/A")
            entry = {
                "video_id": video_id,
                "title": title,
                "privacy": privacy,
                "publish_at": pub_at,
            }
            pipeline.append(entry)
            logger.info("[%s] %s", privacy.upper(), title[:50])
            if privacy == "private" and pub_at != "N/A":
                logger.info("Scheduled for: %s", pub_at)
            elif privacy == "private":
                logger.info("Manual release required")
        return pipeline

    def get_detailed_stats(self, max_results=15):
        youtube = self._youtube()
        stats_rows = []
        for item in self._list_upload_items(max_results):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            privacy = item["status"]["privacyStatus"]
            vid_res = youtube.videos().list(part="statistics", id=video_id).execute()
            stats = vid_res["items"][0].get("statistics", {})
            row = {
                "video_id": video_id,
                "title": title,
                "privacy": privacy,
                "views": stats.get("viewCount", "0"),
                "likes": stats.get("likeCount", "0"),
            }
            stats_rows.append(row)
            logger.info(
                "[%s] %s... | Views: %s | Likes: %s",
                privacy.upper(),
                title[:40],
                row["views"],
                row["likes"],
            )
        return stats_rows

    def build_report(self, max_results=10) -> dict[str, Any]:
        """Collect channel, pipeline, and stats into one machine-readable report."""
        return {
            "channel": self.get_channel_summary(),
            "pipeline": self.list_pipeline(max_results=max_results),
            "stats": self.get_detailed_stats(max_results=max_results),
        }


def main(argv=None):
    configure_logging()
    parser = argparse.ArgumentParser(description="YouTube channel auditor")
    parser.add_argument(
        "--token-file",
        default=default_token_file(),
        help="Path to OAuth token JSON (or set YOUTUBE_TOKEN_FILE)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Max uploads to inspect for pipeline/stats",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a combined channel/pipeline/stats report as JSON",
    )
    args = parser.parse_args(argv)

    auditor = YouTubeAuditor(token_file=args.token_file)
    report = auditor.build_report(max_results=args.max_results)
    if args.json:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
