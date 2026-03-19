import logging
import asyncio
import os
import tempfile
from typing import Optional, Dict
import yt_dlp

logger = logging.getLogger(__name__)

_now_playing: Dict[int, dict] = {}


def _get_cookies_file():
    cookies_content = os.getenv("YOUTUBE_COOKIES", "")
    if not cookies_content:
        return None
    try:
        # Fix newlines corrupted in environment variables
        cookies_content = cookies_content.replace("\\n", "\n").replace("\\t", "\t")

        # Ensure Netscape header
        if not cookies_content.strip().startswith("# Netscape"):
            cookies_content = "# Netscape HTTP Cookie File\n# https://curl.haxx.se/rfc/cookie_spec.html\n# This is a generated file! Do not edit.\n\n" + cookies_content

        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        tmp.write(cookies_content)
        tmp.flush()
        tmp.close()
        logger.info(f"✅ Cookies file created successfully")
        return tmp.name
    except Exception as e:
        logger.error(f"Cookies file error: {e}")
        return None


def _get_yt_stream_url(query: str):
    cookies_file = _get_cookies_file()
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
    if cookies_file:
        opts["cookiefile"] = cookies_file

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
    finally:
        if cookies_file:
            try:
                os.unlink(cookies_file)
            except Exception:
                pass


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
        return {
            "success": True,
            "title": play_data["title"],
            "duration": yt_dur,
            "url": yt_page
        }
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
    cookies = os.getenv("YOUTUBE_COOKIES", "")
    if cookies:
        logger.info("✅ Voice chat module ready (YouTube cookies loaded)")
    else:
        logger.warning("⚠️ Voice chat ready but YOUTUBE_COOKIES not set!")
    return True


def get_now_playing(chat_id: int) -> Optional[dict]:
    return _now_playing.get(chat_id)


def is_voice_available() -> bool:
    return True
```

---

Saath mein **Railway pe YOUTUBE_COOKIES variable fix karo:**

1. Railway → Variables → `YOUTUBE_COOKIES` **delete** karo
2. Naya variable banao
3. Value mein ye **exact format** mein paste karo — tab (`	`) aur newline sab sahi rakho:
```
# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1808508822	SAPISID	N6k-uGMnYBLep5tZ/AA6MrmpMItr6j27Sf
.youtube.com	TRUE	/	TRUE	1808508822	__Secure-3PAPISID	N6k-uGMnYBLep5tZ/AA6MrmpMItr6j27Sf
.youtube.com	TRUE	/	TRUE	1808508822	__Secure-1PAPISID	N6k-uGMnYBLep5tZ/AA6MrmpMItr6j27Sf
.youtube.com	TRUE	/	TRUE	1808508822	__Secure-1PSID	g.a0008AgpxYMru85j09dyG3rfCuazLNMK_9zV9YiWesS_n8ZtYeWfkLEQoGKRJc1un1VB4-HJLQACgYKAeYSARISFQHGX2Mi4Rgym6C83IEl5-e1krBNfhoVAUF8yKohAmIOg-0BLXlbk7-2qKP_0076
.youtube.com	TRUE	/	TRUE	1808508822	__Secure-3PSID	g.a0008AgpxYMru85j09dyG3rfCuazLNMK_9zV9YiWesS_n8ZtYeWfsFAJf6t4EHwmM0hyshQSkgACgYKAYgSARISFQHGX2MiGdjbCIFJ80Tv_gl93DtjJRoVAUF8yKq3RBB05cnBOoVxLXctI6Kv0076
.youtube.com	TRUE	/	FALSE	1808508822	SID	g.a0008AgpxYMru85j09dyG3rfCuazLNMK_9zV9YiWesS_n8ZtYeWfVS5WSvmIC8aIF419TJWW5gACgYKAaISARISFQHGX2Mim8MnVsBgKUwCMidksFYbnRoVAUF8yKpuzE7X54DeDWXlj2Xet3tt0076
.youtube.com	TRUE	/	TRUE	1808508822	LOGIN_INFO	AFmmF2swRgIhAL3loi1w8o2KX3VP3eyK4cEYQmep8oUYCWF_Gcj3aeQTAiEAoM3zhKipmZXjXY2cihfzp5uc-01-Gob0KMrcG7ZR1RM:QUQ3MjNmeUtqQnQ5RnhOZzdwNkJLYzBNeEZDSkxaV2NoQTc0dmVPd2FMaGUyOGVpRHFLcUROdFNPYk5jc05XNlBSRkdhQU9vS1RpQXRQakFkSVNydVlQaFRpejhSazhlVXJIYkZLRHMtOUl3S0tEOFQyVEEzTVpxU0RqWXE0LXpid1FiNUR2SU95cW1LcmN3SkMzOXFvWGJCUDhlZTljV3hn
.youtube.com	TRUE	/	TRUE	1805484822	__Secure-1PSIDTS	sidts-CjQBBj1CYnNJzWbdhTnspjqZo-pdYes_d962Zb1wrXo-Ni_fucxQG0HEpmrkuGqgMqFQE6sUEAA
.youtube.com	TRUE	/	TRUE	1805484822	__Secure-3PSIDTS	sidts-CjQBBj1CYnNJzWbdhTnspjqZo-pdYes_d962Zb1wrXo-Ni_fucxQG0HEpmrkuGqgMqFQE6sUEAA
.youtube.com	TRUE	/	FALSE	1805484838	SIDCC	AKEyXzXV9wttRf88nrX0bLwHa6B1TODB-0WwAoKkZjmET_nsqtC3-uswrbNsmu25l-VlgHugMg
.youtube.com	TRUE	/	TRUE	1805484838	__Secure-1PSIDCC	AKEyXzUdFZLCasIjVoggrDZv9QXQmp3HxgzYXv0HvJ1rVmE9LSU-dtRcXSIrB2Bnln31W7O0EQ
.youtube.com	TRUE	/	TRUE	1805484838	__Secure-3PSIDCC	AKEyXzX37E1DVZ7Y1We0ArUCgmiIqCT-vuHWwwp8mOehxV5lVf06vU1uXhgqiXD9JLUSQUkfWA
