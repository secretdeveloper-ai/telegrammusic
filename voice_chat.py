import logging
import asyncio
import os
import tempfile
from typing import Optional, Dict
import yt_dlp
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioImagePiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pyrogram import Client

logger = logging.getLogger(__name__)

# Global pytgcalls instance
_pytgcalls: Optional[PyTgCalls] = None
_pyrogram_client: Optional[Client] = None

# Track current playing per group
_now_playing: Dict[int, dict] = {}


def get_pytgcalls() -> Optional[PyTgCalls]:
    return _pytgcalls


async def init_pytgcalls(pyrogram_client: Client):
    """Initialize PyTgCalls with pyrogram client"""
    global _pytgcalls, _pyrogram_client
    try:
        _pyrogram_client = pyrogram_client
        _pytgcalls = PyTgCalls(pyrogram_client)

        @_pytgcalls.on_stream_end()
        async def on_stream_end(client, update: Update):
            logger.info(f"Stream ended in chat: {update.chat_id}")
            if update.chat_id in _now_playing:
                del _now_playing[update.chat_id]

        await _pytgcalls.start()
        logger.info("✅ PyTgCalls initialized for voice streaming")
        return True
    except Exception as e:
        logger.error(f"PyTgCalls init failed: {e}")
        return False


def _get_yt_audio_url(query: str) -> Optional[str]:
    """Get direct audio stream URL from YouTube using yt-dlp"""
    opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 20,
        "http_headers": {
            "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12) gzip",
        },
        "extractor_args": {
            "youtube": {"player_client": ["android"]}
        },
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            search = f"ytsearch1:{query}"
            info = ydl.extract_info(search, download=False)
            if "entries" in info and info["entries"]:
                info = info["entries"][0]
            url = info.get("url")
            title = info.get("title", "Unknown")
            duration = info.get("duration", 0)
            if url:
                logger.info(f"✅ YouTube audio URL: {title}")
                return url, title, duration
    except Exception as e:
        logger.error(f"yt-dlp error: {e}")
    return None, None, 0


async def join_and_play(chat_id: int, query: str, song_data: dict = None) -> dict:
    """
    Join voice chat and start playing.
    Returns dict with status and message.
    """
    global _pytgcalls, _now_playing

    if not _pytgcalls:
        return {"success": False, "msg": "Voice streaming not initialized"}

    try:
        # Get audio URL - try yt-dlp first for full songs
        audio_url = None
        title = query
        duration = 0

        if song_data and song_data.get("url"):
            # Use existing song URL (from Deezer/JioSaavn)
            audio_url = song_data["url"]
            title = song_data.get("title", query)
            duration = song_data.get("duration", 0)
        else:
            # Try YouTube for full song
            audio_url, title, duration = await asyncio.get_event_loop().run_in_executor(
                None, _get_yt_audio_url, query
            )

        if not audio_url:
            return {"success": False, "msg": "Could not get audio stream"}

        # Check if already in a call
        try:
            active_calls = await _pytgcalls.active_calls()
            already_in_call = any(call.chat_id == chat_id for call in active_calls)
        except Exception:
            already_in_call = False

        stream = AudioPiped(audio_url, HighQualityAudio())

        if already_in_call:
            # Change stream if already playing
            await _pytgcalls.change_stream(chat_id, stream)
            logger.info(f"Changed stream in {chat_id}: {title}")
        else:
            # Join voice chat and start playing
            await _pytgcalls.join_group_call(
                chat_id,
                stream,
                stream_type=None,
            )
            logger.info(f"Joined voice chat in {chat_id}: {title}")

        _now_playing[chat_id] = {
            "title": title,
            "duration": duration,
            "url": audio_url,
        }

        return {
            "success": True,
            "title": title,
            "duration": duration,
            "msg": f"Now playing: {title}",
        }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Voice chat error in {chat_id}: {error_msg}")

        if "GROUPCALL_FORBIDDEN" in error_msg:
            return {"success": False, "msg": "Voice chat is not enabled in this group!"}
        elif "GROUP_CALL_INVALID" in error_msg:
            return {"success": False, "msg": "Please start a voice chat first!"}
        else:
            return {"success": False, "msg": f"Error: {error_msg[:100]}"}


async def leave_voice_chat(chat_id: int) -> bool:
    """Leave voice chat"""
    global _pytgcalls, _now_playing
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.leave_group_call(chat_id)
        if chat_id in _now_playing:
            del _now_playing[chat_id]
        logger.info(f"Left voice chat: {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Leave voice chat error: {e}")
        return False


async def pause_voice_chat(chat_id: int) -> bool:
    """Pause playback"""
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.pause_stream(chat_id)
        return True
    except Exception as e:
        logger.error(f"Pause error: {e}")
        return False


async def resume_voice_chat(chat_id: int) -> bool:
    """Resume playback"""
    if not _pytgcalls:
        return False
    try:
        await _pytgcalls.resume_stream(chat_id)
        return True
    except Exception as e:
        logger.error(f"Resume error: {e}")
        return False


def get_now_playing(chat_id: int) -> Optional[dict]:
    return _now_playing.get(chat_id)
