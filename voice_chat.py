import logging
import asyncio
from typing import Optional, Dict
import yt_dlp
from pyrogram import Client

logger = logging.getLogger(__name__)

_pytgcalls = None
_now_playing: Dict[int, dict] = {}


async def init_pytgcalls(pyrogram_client: Client):
    global _pytgcalls
    try:
        from pytgcalls import PyTgCalls
        from pytgcalls.types.input_stream import AudioPiped
        from pytgcalls.types.input_stream.quality import HighQualityAudio

        _pytgcalls = PyTgCalls(pyrogram_client)

        @_pytgcalls.on_stream_end()
        async def on_end(client, update):
            chat_id = update.chat_id
            if chat_id in _now_playing:
                del _now_playing[chat_id]

        await _pytgcalls.start()
        logger.info("✅ PyTgCalls voice streaming ready")
        return True
    except Exception as e:
        logger.error(f"PyTgCalls init failed: {e}")
        return False


def _get_yt_stream_url(query: str):
    opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 20,
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
            )
    except Exception as e:
        logger.error(f"YT stream error: {e}")
        return None, None, 0, ""


async def _play_stream(chat_id: int, song_data: dict) -> bool:
    global _pytgcalls, _now_playing
    if not _pytgcalls:
        return False
    try:
        from pytgcalls.types.input_stream import AudioPiped
        from pytgcalls.types.input_stream.quality import HighQualityAudio

        audio_url = song_data.get("stream_url") or song_data.get("url", "")
        if not audio_url:
            return False

        stream = AudioPiped(audio_url, HighQualityAudio())

        try:
            active = await _pytgcalls.active_calls()
            in_call = any(str(c) == str(chat_id) for c in active)
        except Exception:
            in_call = False

        if in_call:
            await _pytgcalls.change_stream(chat_id, stream)
        else:
            await _pytgcalls.join_group_call(chat_id, stream)

        _now_playing[chat_id] = song_data
        logger.info(f"▶️ Playing in {chat_id}: {song_data.get('title')}")
        return True
    except Exception as e:
        logger.error(f"Voice chat error {chat_id}: {e}")
        return False


async def voice_play(chat_id: int, query: str, song_data: dict = None) -> dict:
    if not _pytgcalls:
        return {"success": False, "msg": "Voice streaming not available"}

    title = song_data.get("title", query) if song_data else query

    loop = asyncio.get_event_loop()
    yt_url, yt_title, yt_dur, yt_thumb = await loop.run_in_executor(
        None, _get_yt_stream_url, title
    )

    if yt_url:
        play_data = {
            "title": yt_title or title,
            "stream_url": yt_url,
            "duration": yt_dur,
            "thumbnail": yt_thumb,
        }
    elif song_data and song_data.get("url"):
        play_data = {**song_data, "stream_url": song_data["url"]}
    else:
        return {"success": False, "msg": "Could not get audio stream"}

    success = await _play_stream(chat_id, play_data)

    if success:
        return {
            "success": True,
            "title": play_data["title"],
            "duration": play_data.get("duration", 0),
        }
    else:
        return {"success": False, "msg": "⚠️ Pehle group mein Voice Chat start karo!"}


async def voice_skip(chat_id: int, song_data: dict = None) -> dict:
    if not _pytgcalls:
        return {"success": False}
    if song_data:
        return await voice_play(chat_id, song_data.get("title", ""), song_data)
    try:
        await _pytgcalls.leave_group_call(chat_id)
        if chat_id in _now_playing:
            del _now_playing[chat_id]
        return {"success": True}
    except Exception as e:
        return {"success": False, "msg": str(e)}


async def voice_leave(chat_id: int) -> bool:
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.leave_group_call(chat_id)
        if chat_id in _now_playing:
            del _now_playing[chat_id]
        return True
    except Exception:
        return False


async def voice_pause(chat_id: int) -> bool:
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.pause_stream(chat_id)
        return True
    except Exception:
        return False


async def voice_resume(chat_id: int) -> bool:
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.resume_stream(chat_id)
        return True
    except Exception:
        return False


def get_now_playing(chat_id: int) -> Optional[dict]:
    return _now_playing.get(chat_id)


def is_voice_available() -> bool:
    return _pytgcalls is not None
```

**Commit karo → Railway automatically redeploy karega.**

---

Deploy hone ke baad Railway logs mein ye line aani chahiye:
```
✅ PyTgCalls voice streaming ready
