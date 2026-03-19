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
        self.yt_dlp_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": 30,
            "http_headers": {
                "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"],
                }
            },
        }

        self.spotify_client = None
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and SPOTIFY_CLIENT_ID.strip() and SPOTIFY_CLIENT_SECRET.strip():
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

    def _format_duration(self, seconds: int) -> str:
        """Format seconds to mm:ss"""
        if not seconds:
            return "0:00"
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"

    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search and fetch song info from YouTube"""
        try:
            search_query = f"ytsearch1:{query}"
            with yt_dlp.YoutubeDL(self.yt_dlp_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)

                if not info:
                    return None

                # Extract from search results
                if "entries" in info:
                    entries = info.get("entries", [])
                    if not entries:
                        return None
                    info = entries[0]

                if not info:
                    return None

                duration = info.get("duration") or 0

                # Skip if too long
                if duration and duration > MAX_SONG_DURATION:
                    logger.warning(f"Song too long: {duration}s")
                    return None

                title = info.get("title", "Unknown")
                video_id = info.get("id", "")
                webpage_url = info.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"
                audio_url = info.get("url", "")

                logger.info(f"Found: {title} | Duration: {duration}s | ID: {video_id}")

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
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return None

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        """Search music - uses YouTube directly"""
        return await self.search_youtube(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        """Fetch songs from YouTube playlist"""
        try:
            opts = {
                **self.yt_dlp_opts,
                "extract_flat": "in_playlist",
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                songs = []
                for entry in info.get("entries", [])[:20]:
                    url = entry.get("url") or entry.get("id", "")
                    if url:
                        song_result = await self.search_youtube(url)
                        if song_result:
                            songs.append(song_result)
                return songs
        except Exception as e:
            logger.error(f"Playlist fetch error: {e}")
            return []
