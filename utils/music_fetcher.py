import aiohttp
import asyncio
from typing import Optional, Dict, List
import logging

from config import MAX_SONG_DURATION

logger = logging.getLogger(__name__)

# JioSaavn unofficial API - free, no auth, no cookies needed
JIOSAAVN_API = "https://saavn.dev/api"
# Fallback API mirror
JIOSAAVN_API_2 = "https://jiosaavn-api-2-harsh-patel.vercel.app/api"


class MusicFetcher:
    def __init__(self):
        self.session = None
        logger.info("MusicFetcher initialized with JioSaavn API")

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session

    def _format_duration(self, seconds) -> str:
        if not seconds:
            return "0:00"
        s = int(seconds)
        return f"{s // 60}:{s % 60:02d}"

    async def _search_jiosaavn(self, query: str, base_url: str) -> Optional[Dict]:
        """Search JioSaavn for a song"""
        try:
            session = await self._get_session()
            url = f"{base_url}/search/songs"
            params = {"query": query, "page": 1, "limit": 1}

            async with session.get(url, params=params, ssl=False) as resp:
                if resp.status != 200:
                    logger.warning(f"JioSaavn returned {resp.status}")
                    return None

                data = await resp.json()

                # Handle different API response formats
                songs = None
                if data.get("data") and data["data"].get("results"):
                    songs = data["data"]["results"]
                elif data.get("results"):
                    songs = data["results"]
                elif isinstance(data.get("data"), list):
                    songs = data["data"]

                if not songs:
                    logger.warning("No songs found in JioSaavn response")
                    return None

                song = songs[0]

                # Get best quality download URL
                download_url = self._extract_download_url(song)
                if not download_url:
                    logger.warning("No download URL found")
                    return None

                # Extract duration
                duration = 0
                dur_raw = song.get("duration") or song.get("more_info", {}).get("duration", 0)
                if dur_raw:
                    try:
                        duration = int(dur_raw)
                    except (ValueError, TypeError):
                        duration = 0

                if duration and duration > MAX_SONG_DURATION:
                    logger.warning(f"Song too long: {duration}s")
                    return None

                # Extract title and artist
                title = song.get("name") or song.get("title") or "Unknown"
                artists = ""
                if song.get("artists") and song["artists"].get("primary"):
                    artists = ", ".join(
                        a.get("name", "") for a in song["artists"]["primary"]
                    )
                elif song.get("primaryArtists") or song.get("primary_artists"):
                    artists = song.get("primaryArtists") or song.get("primary_artists", "")

                full_title = f"{title} - {artists}" if artists else title

                # Extract image/thumbnail
                thumbnail = ""
                if song.get("image"):
                    if isinstance(song["image"], list):
                        imgs = song["image"]
                        thumbnail = imgs[-1].get("url") or imgs[-1].get("link", "") if imgs else ""
                    else:
                        thumbnail = str(song["image"])

                # Song page URL
                song_url = song.get("url") or song.get("perma_url", "")

                logger.info(f"✅ Found on JioSaavn: {full_title} | {self._format_duration(duration)}")

                return {
                    "title": full_title,
                    "url": download_url,
                    "webpage_url": song_url,
                    "duration": duration,
                    "duration_str": self._format_duration(duration),
                    "thumbnail": thumbnail,
                    "source": "JioSaavn",
                    "video_id": song.get("id", ""),
                    "uploader": artists,
                }

        except asyncio.TimeoutError:
            logger.warning(f"JioSaavn timeout for: {query}")
            return None
        except Exception as e:
            logger.error(f"JioSaavn search error: {e}")
            return None

    def _extract_download_url(self, song: dict) -> Optional[str]:
        """Extract best quality download URL from song data"""
        # Try direct download_url field
        if song.get("downloadUrl"):
            urls = song["downloadUrl"]
            if isinstance(urls, list) and urls:
                # Get highest quality (last item usually)
                for quality in reversed(urls):
                    url = quality.get("url") or quality.get("link")
                    if url and url.startswith("http"):
                        return url
            elif isinstance(urls, str) and urls.startswith("http"):
                return urls

        # Try download_url with different key names
        for key in ["download_url", "media_url", "media_preview_url", "vlink"]:
            val = song.get(key) or song.get("more_info", {}).get(key)
            if val and isinstance(val, str) and val.startswith("http"):
                return val

        # Try encrypted_media_url (needs decoding - skip)
        return None

    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        """Search music - JioSaavn first, then fallback"""
        logger.info(f"Searching for: {query}")

        # Try primary JioSaavn API
        result = await self._search_jiosaavn(query, JIOSAAVN_API)
        if result:
            return result

        # Try mirror API
        logger.info("Trying JioSaavn mirror...")
        result = await self._search_jiosaavn(query, JIOSAAVN_API_2)
        if result:
            return result

        logger.error(f"All search methods failed for: {query}")
        return None

    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Alias for compatibility"""
        return await self.search_music(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        """Placeholder - playlist not supported with JioSaavn"""
        return []

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
