import logging
import asyncio
from typing import Optional, Dict
import yt_dlp

logger = logging.getLogger(__name__)

_now_playing: Dict[int, dict] = {}


def _get_yt_stream_url(query: str):
    opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 20,
        "cookiefile": "/app/cookies.txt",
        "http_headers": {
            "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12) gzip",
        },
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if "entries" in info and info["entries"]:
                info = info["entries"][0]
            return (
                info.get("url"),
                info.get("title", "Unknown"),
                info.get("duration", 0),
                info.get("thumbnail", ""),
                info.get("webpage_url", ""),
            )
    except Exception as e:
        logger.error(f"YT stream error: {e}")
        return None, None, 0, "", ""


async def voice_play(chat_id: int, query: str, song_data: dict = None) -> dict:
    title = song_data.get("title", query) if song_data else query
    loop = asyncio.get_event_loop()
    yt_url, yt_title, yt_dur, yt_thumb, yt_page = await loop.run_in_executor(
        None, _get_yt_stream_url, title
    )
    if yt_url:
        play_data = {
            "title": yt_title or title,
            "stream_url": yt_url,
            "duration": yt_dur,
            "thumbnail": yt_thumb,
            "webpage_url": yt_page,
        }
        _now_playing[chat_id] = play_data
        return {"success": True, "title": play_data["title"], "duration": yt_dur, "url": yt_page}
    return {"success": False, "msg": "YouTube se song nahi mila. Cookies check karo."}


async def voice_skip(chat_id: int, song_data: dict = None) -> dict:
    if song_data:
        return await voice_play(chat_id, song_data.get("title", ""), song_data)
    if chat_id in _now_playing:
        del _now_playing[chat_id]
    return {"success": True}


async def voice_leave(chat_id: int) -> bool:
    if chat_id in _now_playing:
        del _now_playing[chat_id]
    return True


async def voice_pause(chat_id: int) -> bool:
    return True


async def voice_resume(chat_id: int) -> bool:
    return True


async def init_pytgcalls(pyrogram_client=None):
    logger.info("✅ Voice chat module ready (YouTube cookies mode)")
    return True


def get_now_playing(chat_id: int) -> Optional[dict]:
    return _now_playing.get(chat_id)


def is_voice_available() -> bool:
    return True
