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
        # Method 1: Android client (most reliable)
        self.opts_android = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"],
                    "player_skip": ["webpage", "configs"],
                }
            },
            "http_headers": {
                "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12) gzip",
            },
        }

        # Method 2: iOS client fallback
        self.opts_ios = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "extractor_args": {
                "youtube": {
                    "player_client": ["ios"],
                }
            },
            "http_headers": {
                "User-Agent": "com.google.ios.youtube/19.09.3 (iPhone14,3; U; CPU iOS 16_3 like Mac OS X)",
            },
        }

        # Method 3: TV client fallback
        self.opts_tv = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "extractor_args": {
                "youtube": {
                    "player_client": ["tv_embedded"],
                }
            },
        }

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

    def _format_duration(self, seconds) -> str:
        if not seconds:
            return "0:00"
        seconds = int(seconds)
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"

    def _extract_info_safe(self, opts: dict, search_query: str) -> Optional[Dict]:
        """Try to extract info with given options"""
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                if not info:
                    return None
                if "entries" in info:
                    entries = info.get("entries", [])
                    if not entries:
                        return None
                    info = entries[0]
                if not info or not info.get("id"):
                    return None
                return info
        except Exception as e:
            logger.warning(f"Extract failed with opts: {e}")
            return None

    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search YouTube with multiple fallback methods"""
        search_query = f"ytsearch1:{query}"
        logger.info(f"Searching YouTube for: {query}")

        # Try each method in order
        info = None
        for opts in [self.opts_android, self.opts_ios, self.opts_tv]:
            info = self._extract_info_safe(opts, search_query)
            if info:
                break

        if not info:
            logger.error(f"All YouTube methods failed for: {query}")
            return None

        duration = info.get("duration") or 0
        if duration and duration > MAX_SONG_DURATION:
            logger.warning(f"Song too long: {duration}s")
            return None

        title = info.get("title", "Unknown")
        video_id = info.get("id", "")
        webpage_url = info.get("webpage_url") or f"https://youtu.be/{video_id}"
        audio_url = info.get("url", "")

        logger.info(f"Found: {title} | {self._format_duration(duration)} | {video_id}")

        return {
            "title": title,
            "url": audio_url,
            "webpage_url": webpage_url,
            "duration": duration,
            "duration_str": self._format_duration(duration),
            "thumbnail": info.get("thumbnail", ""),
            "source": "YouTube",
            "video_id": video_id,
            "uploader": info.get("uploader", ""),
        }

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        """Search music"""
        return await self.search_youtube(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        """Fetch songs from YouTube playlist"""
        try:
            opts = {**self.opts_android, "extract_flat": "in_playlist"}
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
            logger.error(f"Playlist fetch error: {e}")
            return []
