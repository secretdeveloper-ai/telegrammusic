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
            "source_address": "0.0.0.0",
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
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
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
            logger.warning("Spotify credentials not provided, skipping")

    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search and fetch song from YouTube"""
        try:
            search_query = f"ytsearch1:{query}"
            with yt_dlp.YoutubeDL(self.yt_dlp_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)

                if "entries" in info and info["entries"]:
                    info = info["entries"][0]

                if not info:
                    return None

                duration = info.get("duration", 0)
                if duration and duration > MAX_SONG_DURATION:
                    return None

                return {
                    "title": info.get("title", "Unknown"),
                    "url": info.get("url", ""),
                    "webpage_url": info.get("webpage_url", ""),
                    "duration": duration or 0,
                    "thumbnail": info.get("thumbnail", ""),
                    "source": "YouTube",
                    "video_id": info.get("id", ""),
                }
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return None

    async def search_spotify(self, query: str) -> Optional[Dict]:
        """Search Spotify then fetch from YouTube"""
        if not self.spotify_client:
            return None

        try:
            results = self.spotify_client.search(q=query, type="track", limit=1)
            tracks = results.get("tracks", {}).get("items", [])

            if not tracks:
                return None

            track = tracks[0]
            duration = track.get("duration_ms", 0) // 1000

            if duration > MAX_SONG_DURATION:
                return None

            artists = ", ".join([a["name"] for a in track.get("artists", [])])
            song_name = f"{track['name']} {artists}"

            youtube_result = await self.search_youtube(song_name)
            if youtube_result:
                return {
                    **youtube_result,
                    "source": "Spotify+YouTube",
                    "spotify_id": track.get("id", ""),
                }
            return None

        except Exception as e:
            logger.error(f"Spotify search error: {e}")
            return None

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        """Search music - tries YouTube directly"""
        return await self.search_youtube(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        """Fetch multiple songs from YouTube playlist"""
        try:
            opts = {
                **self.yt_dlp_opts,
                "extract_flat": "in_playlist",
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                songs = []

                for entry in info.get("entries", [])[:20]:
                    song_result = await self.search_youtube(entry.get("url", ""))
                    if song_result:
                        songs.append(song_result)

                return songs
        except Exception as e:
            logger.error(f"Playlist fetch error: {e}")
            return []
