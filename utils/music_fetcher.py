import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
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
            "default_search": "ytsearch",
            "socket_timeout": 30,
        }

        # Initialize Spotify client if credentials provided
        if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
            auth_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET
            )
            self.spotify_client = spotipy.Spotify(auth_manager=auth_manager)
        else:
            self.spotify_client = None
            logger.warning("Spotify credentials not provided")

    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search and fetch song from YouTube"""
        try:
            with yt_dlp.YoutubeDL(self.yt_dlp_opts) as ydl:
                info = ydl.extract_info(query, download=False)

                if isinstance(info, list) and len(info) > 0:
                    info = info[0]

                duration = info.get("duration", 0)
                if duration > MAX_SONG_DURATION:
                    return None

                return {
                    "title": info.get("title", "Unknown"),
                    "url": info.get("url", ""),
                    "duration": duration,
                    "thumbnail": info.get("thumbnail", ""),
                    "source": "YouTube",
                    "video_id": info.get("id", ""),
                }
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return None

    async def search_spotify(self, query: str) -> Optional[Dict]:
        """Search and fetch song from Spotify"""
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

            # Get preview URL or search YouTube for the track
            preview_url = track.get("preview_url")
            if not preview_url:
                # Fall back to YouTube search
                artists = ", ".join([artist["name"] for artist in track.get("artists", [])])
                youtube_result = await self.search_youtube(
                    f"{track['name']} {artists}"
                )
                if youtube_result:
                    return {
                        **youtube_result,
                        "source": "Spotify→YouTube",
                        "spotify_id": track.get("id", ""),
                    }
                return None

            return {
                "title": f"{track['name']} - {', '.join([a['name'] for a in track['artists']])}",
                "url": preview_url,
                "duration": duration,
                "thumbnail": track.get("album", {}).get("images", [{}])[0].get("url", ""),
                "source": "Spotify",
                "spotify_id": track.get("id", ""),
            }
        except Exception as e:
            logger.error(f"Spotify search error: {e}")
            return None

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        """Search music from specified source"""
        if source == "youtube":
            return await self.search_youtube(query)
        elif source == "spotify":
            return await self.search_spotify(query)
        elif source == "both":
            # Try Spotify first, then YouTube
            result = await self.search_spotify(query)
            if not result:
                result = await self.search_youtube(query)
            return result
        return None

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

                for entry in info.get("entries", [])[:20]:  # Limit to 20 songs
                    song_result = await self.search_youtube(entry.get("url"))
                    if song_result:
                        songs.append(song_result)

                return songs
        except Exception as e:
            logger.error(f"Playlist fetch error: {e}")
            return []

    async def get_playlist_spotify(self, playlist_url: str) -> List[Dict]:
        """Fetch multiple songs from Spotify playlist"""
        if not self.spotify_client:
            return []

        try:
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            results = self.spotify_client.playlist_tracks(playlist_id, limit=20)
            songs = []

            for item in results.get("items", []):
                track = item.get("track")
                if track:
                    song_result = await self.search_spotify(
                        f"{track['name']} {track['artists'][0]['name']}"
                    )
                    if song_result:
                        songs.append(song_result)

            return songs
        except Exception as e:
            logger.error(f"Spotify playlist error: {e}")
            return []
