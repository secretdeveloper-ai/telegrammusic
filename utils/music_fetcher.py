import yt_dlp
from typing import Optional, Dict, List
import logging

from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    MAX_SONG_DURATION,
)

logger = logging.getLogger(__name__)


class MusicFetcher:
    def __init__(self):
        # Use web_creator_music client - works best on server environments
        self.base_opts = {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "noplaylist": True,
        }

        self.client_opts_list = [
            # Method 1: web with po_token workaround
            {
                **self.base_opts,
                "format": "bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["web_creator"],
                    }
                },
            },
            # Method 2: mweb (mobile web)
            {
                **self.base_opts,
                "format": "bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["mweb"],
                    }
                },
            },
            # Method 3: tv_embedded - no sign-in needed
            {
                **self.base_opts,
                "format": "bestaudio/best",
                "extractor_args": {
                    "youtube": {
                        "player_client": ["tv_embedded"],
                    }
                },
            },
            # Method 4: default with no client override
            {
                **self.base_opts,
                "format": "bestaudio/best",
            },
        ]

        self.spotify_client = None
        if (SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and
                SPOTIFY_CLIENT_ID.strip() and SPOTIFY_CLIENT_SECRET.strip()):
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyClientCredentials
                auth_manager = SpotifyClientCredentials(
                    client_id=SPOTIFY_CLIENT_ID,
                    client_secret=SPOTIFY_CLIENT_SECRET
                )
                self.spotify_client = spotipy.Spotify(auth_manager=auth_manager)
                logger.info("Spotify client initialized")
            except Exception as e:
                logger.warning(f"Spotify init failed: {e}")
        else:
            logger.info("Spotify not configured, using YouTube only")

    def fmt_dur(self, seconds) -> str:
        if not seconds:
            return "0:00"
        s = int(seconds)
        return f"{s // 60}:{s % 60:02d}"

    def _try_extract(self, opts: dict, search_query: str) -> Optional[dict]:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not info:
                    return None
                if "entries" in info:
                    entries = [e for e in info.get("entries", []) if e]
                    if not entries:
                        return None
                    info = entries[0]
                if not info or not info.get("id"):
                    return None
                return info
        except Exception as e:
            logger.warning(f"Method failed: {str(e)[:80]}")
            return None

    async def search_youtube(self, query: str) -> Optional[Dict]:
        search_query = f"ytsearch1:{query}"
        logger.info(f"Searching: {query}")

        info = None
        for i, opts in enumerate(self.client_opts_list):
            logger.info(f"Trying method {i+1}...")
            info = self._try_extract(opts, search_query)
            if info:
                logger.info(f"Method {i+1} succeeded!")
                break

        if not info:
            logger.error(f"All methods failed for: {query}")
            return None

        duration = info.get("duration") or 0
        if duration and duration > MAX_SONG_DURATION:
            return None

        video_id = info.get("id", "")
        title = info.get("title", "Unknown")
        webpage_url = info.get("webpage_url") or f"https://youtu.be/{video_id}"

        logger.info(f"Found: {title} | {self.fmt_dur(duration)}")

        return {
            "title": title,
            "url": info.get("url", ""),
            "webpage_url": webpage_url,
            "duration": duration,
            "duration_str": self.fmt_dur(duration),
            "thumbnail": info.get("thumbnail", ""),
            "source": "YouTube",
            "video_id": video_id,
            "uploader": info.get("uploader", ""),
        }

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        return await self.search_youtube(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        try:
            opts = {**self.client_opts_list[0], "extract_flat": "in_playlist"}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                songs = []
                for entry in info.get("entries", [])[:20]:
                    url = entry.get("url") or entry.get("id", "")
                    if url:
                        result = await self.search_youtube(url)
                        if result:
                            songs.append(result)
                return songs
        except Exception as e:
            logger.error(f"Playlist error: {e}")
            return []
