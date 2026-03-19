import httpx
import asyncio
from typing import Optional, Dict, List
import logging

from config import MAX_SONG_DURATION

logger = logging.getLogger(__name__)


class MusicFetcher:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=15.0,
            follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MusicBot/1.0)"},
        )
        logger.info("MusicFetcher initialized")

    def _fmt(self, seconds) -> str:
        if not seconds:
            return "0:00"
        s = int(seconds)
        return f"{s // 60}:{s % 60:02d}"

    # ─────────────────────────────────────────────
    # Method 1: JioSaavn via RapidAPI-style public proxy
    # ─────────────────────────────────────────────
    async def _try_jiosaavn_proxy(self, query: str) -> Optional[Dict]:
        urls = [
            f"https://jiosaavn-api-privatecvc2.vercel.app/api/search/songs?query={query}&page=1&limit=1",
            f"https://jiosaavn-api-ts.vercel.app/api/search/songs?query={query}&page=1&limit=1",
            f"https://saavn-api-inky.vercel.app/api/search/songs?query={query}&page=1&limit=1",
        ]
        for url in urls:
            try:
                r = await self.client.get(url)
                if r.status_code != 200:
                    continue
                data = r.json()
                results = None
                if isinstance(data.get("data"), dict):
                    results = data["data"].get("results", [])
                elif isinstance(data.get("data"), list):
                    results = data["data"]
                elif data.get("results"):
                    results = data["results"]
                if not results:
                    continue
                song = results[0]
                dl_url = self._get_dl_url(song)
                if not dl_url:
                    continue
                dur = int(song.get("duration") or 0)
                name = song.get("name") or song.get("title") or "Unknown"
                artists = self._get_artists(song)
                title = f"{name} - {artists}" if artists else name
                logger.info(f"✅ JioSaavn proxy: {title}")
                return {
                    "title": title,
                    "url": dl_url,
                    "webpage_url": song.get("url") or song.get("perma_url", ""),
                    "duration": dur,
                    "duration_str": self._fmt(dur),
                    "thumbnail": self._get_thumb(song),
                    "source": "JioSaavn",
                    "video_id": str(song.get("id", "")),
                    "uploader": artists,
                }
            except Exception as e:
                logger.warning(f"JioSaavn proxy failed ({url[:40]}): {e}")
        return None

    # ─────────────────────────────────────────────
    # Method 2: iTunes Search API (Apple) — always works
    # ─────────────────────────────────────────────
    async def _try_itunes(self, query: str) -> Optional[Dict]:
        try:
            import urllib.parse
            q = urllib.parse.quote(query)
            url = f"https://itunes.apple.com/search?term={q}&media=music&limit=1&entity=song"
            r = await self.client.get(url)
            if r.status_code != 200:
                return None
            data = r.json()
            results = data.get("results", [])
            if not results:
                return None
            song = results[0]
            preview_url = song.get("previewUrl")
            if not preview_url:
                return None
            dur_ms = song.get("trackTimeMillis", 0)
            dur = dur_ms // 1000 if dur_ms else 30
            title = f"{song.get('trackName', 'Unknown')} - {song.get('artistName', '')}"
            logger.info(f"✅ iTunes: {title} (30s preview)")
            return {
                "title": title,
                "url": preview_url,
                "webpage_url": song.get("trackViewUrl", ""),
                "duration": dur,
                "duration_str": self._fmt(dur),
                "thumbnail": song.get("artworkUrl100", ""),
                "source": "iTunes Preview",
                "video_id": str(song.get("trackId", "")),
                "uploader": song.get("artistName", ""),
            }
        except Exception as e:
            logger.warning(f"iTunes failed: {e}")
            return None

    # ─────────────────────────────────────────────
    # Method 3: Deezer API — free, no auth needed
    # ─────────────────────────────────────────────
    async def _try_deezer(self, query: str) -> Optional[Dict]:
        try:
            import urllib.parse
            q = urllib.parse.quote(query)
            url = f"https://api.deezer.com/search?q={q}&limit=1"
            r = await self.client.get(url)
            if r.status_code != 200:
                return None
            data = r.json()
            results = data.get("data", [])
            if not results:
                return None
            song = results[0]
            preview_url = song.get("preview")
            if not preview_url:
                return None
            dur = song.get("duration", 30)
            title = f"{song.get('title', 'Unknown')} - {song.get('artist', {}).get('name', '')}"
            logger.info(f"✅ Deezer: {title}")
            return {
                "title": title,
                "url": preview_url,
                "webpage_url": song.get("link", ""),
                "duration": dur,
                "duration_str": self._fmt(dur),
                "thumbnail": song.get("album", {}).get("cover_medium", ""),
                "source": "Deezer",
                "video_id": str(song.get("id", "")),
                "uploader": song.get("artist", {}).get("name", ""),
            }
        except Exception as e:
            logger.warning(f"Deezer failed: {e}")
            return None

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────
    def _get_dl_url(self, song: dict) -> Optional[str]:
        for key in ["downloadUrl", "download_url", "media_url"]:
            val = song.get(key)
            if isinstance(val, list) and val:
                for item in reversed(val):
                    u = item.get("url") or item.get("link")
                    if u and u.startswith("http"):
                        return u
            elif isinstance(val, str) and val.startswith("http"):
                return val
        return None

    def _get_artists(self, song: dict) -> str:
        if song.get("artists") and isinstance(song["artists"], dict):
            primary = song["artists"].get("primary", [])
            if primary:
                return ", ".join(a.get("name", "") for a in primary)
        for key in ["primaryArtists", "primary_artists", "artist"]:
            val = song.get(key)
            if val and isinstance(val, str):
                return val
        return ""

    def _get_thumb(self, song: dict) -> str:
        imgs = song.get("image")
        if isinstance(imgs, list) and imgs:
            last = imgs[-1]
            return last.get("url") or last.get("link", "")
        if isinstance(imgs, str):
            return imgs
        return ""

    # ─────────────────────────────────────────────
    # Main search — tries all methods
    # ─────────────────────────────────────────────
    async def search_music(self, query: str, source: str = "both") -> Optional[Dict]:
        logger.info(f"Searching: {query}")

        # 1. JioSaavn proxy (best for Indian songs — full songs)
        result = await self._try_jiosaavn_proxy(query)
        if result:
            return result

        # 2. Deezer (30s preview, global songs)
        result = await self._try_deezer(query)
        if result:
            return result

        # 3. iTunes (30s preview, Apple catalog)
        result = await self._try_itunes(query)
        if result:
            return result

        logger.error(f"All methods failed for: {query}")
        return None

    async def search_youtube(self, query: str) -> Optional[Dict]:
        return await self.search_music(query)

    async def get_playlist_youtube(self, playlist_url: str) -> List[Dict]:
        return []

    async def close(self):
        await self.client.aclose()
