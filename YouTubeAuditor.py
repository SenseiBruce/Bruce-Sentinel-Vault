import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from datetime import datetime

TOKEN_FILE = "/Users/kinshuk.prasad/.openclaw/workspace/youtube_token.json"

class YouTubeAuditor:
    def __init__(self):
        self.credentials = None
        self._load_credentials()

    def _load_credentials(self):
        if not os.path.exists(TOKEN_FILE):
            print(f"❌ No token found at {TOKEN_FILE}. Authenticate first.")
            return
        with open(TOKEN_FILE, "r") as token_file:
            creds_data = json.load(token_file)
            self.credentials = Credentials.from_authorized_user_info(creds_data)

    def get_channel_summary(self):
        if not self.credentials: return
        youtube = build("youtube", "v3", credentials=self.credentials)

        request = youtube.channels().list(part="snippet,contentDetails,statistics", mine=True)
        response = request.execute()
        
        if not response["items"]:
            print("❌ No channel found.")
            return

        channel = response["items"][0]
        snippet = channel["snippet"]
        stats = channel["statistics"]

        print(f"\n📊 **Channel Summary: {snippet['title']}**")
        print(f"   • Subscribers: {stats.get('subscriberCount', 'Hidden')}")
        print(f"   • Total Views: {stats.get('viewCount', '0')}")
        print(f"   • Video Count: {stats.get('videoCount', '0')}")
        print(f"   • Description: {snippet['description'][:100]}...")

    def list_pipeline(self, max_results=10):
        if not self.credentials: return
        youtube = build("youtube", "v3", credentials=self.credentials)

        request = youtube.channels().list(part="contentDetails", mine=True)
        response = request.execute()
        uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        request = youtube.playlistItems().list(
            part="snippet,contentDetails,status",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        response = request.execute()

        print(f"\n📦 **Current Video Pipeline (Last {max_results} Uploads):**")
        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            
            vid_req = youtube.videos().list(part="status,snippet", id=video_id)
            vid_res = vid_req.execute()
            v_item = vid_res["items"][0]
            status = v_item["status"]
            privacy = status["privacyStatus"]
            pub_at = status.get("publishAt", "N/A")
            
            print(f"   • [{privacy.upper()}] {title[:50]}")
            if privacy == "private" and pub_at != "N/A":
                print(f"     └─ Scheduled for: {pub_at}")
            elif privacy == "private":
                print(f"     └─ Manual release required")

    def get_detailed_stats(self, max_results=15):
        if not self.credentials: return
        youtube = build("youtube", "v3", credentials=self.credentials)
        
        request = youtube.channels().list(part="contentDetails", mine=True)
        response = request.execute()
        uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        request = youtube.playlistItems().list(
            part="snippet,contentDetails,status",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        response = request.execute()

        print(f"\n📈 **Full Stats Audit (Last {max_results} Videos):**")
        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            privacy = item["status"]["privacyStatus"]

            vid_req = youtube.videos().list(part="statistics", id=video_id)
            vid_res = vid_req.execute()
            stats = vid_res["items"][0].get("statistics", {})
            views = stats.get("viewCount", "0")
            likes = stats.get("likeCount", "0")

            print(f"   • [{privacy.upper()}] {title[:40]}... | Views: {views} | Likes: {likes}")

if __name__ == "__main__":
    auditor = YouTubeAuditor()
    auditor.get_channel_summary()
    auditor.list_pipeline()
    auditor.get_detailed_stats()
