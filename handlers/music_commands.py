import logging
import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils.music_fetcher import MusicFetcher
from utils.mongo_queue_manager import MongoQueueManager
from utils.claude_assistant import GPTAssistant
from utils.voice_chat import (
    voice_play, voice_skip, voice_pause, voice_resume,
    voice_leave, get_now_playing, is_voice_available
)

logger = logging.getLogger(__name__)
music_fetcher = MusicFetcher()
queue_manager = MongoQueueManager()
gpt_assistant = GPTAssistant()

DEV_URL = "tg://resolve?domain=secret_fetcher"

# Auto reactions for music events
PLAY_REACTIONS = ["🎵", "🎶", "🎸", "🔥", "✨", "💫", "🎤", "🎧"]
SKIP_REACTIONS = ["⏭", "👋", "🔄"]
ADDED_REACTIONS = ["✅", "🎵", "💯", "🔥"]


def dev_btn():
    return InlineKeyboardButton("👨‍💻 ᴅᴇᴠ", url=DEV_URL)


def fmt(s) -> str:
    if not s: return "0:00"
    s = int(s)
    return f"{s//60}:{s%60:02d}"


def esc(text: str) -> str:
    for c in ['_','*','[',']','(',')','>','#','+','-','=','|','{','}','.','!','~','`']:
        text = text.replace(c, f'\\{c}')
    return text


async def auto_react(update: Update, emoji: str):
    """Add auto reaction to message"""
    try:
        await update.message.set_reaction(emoji)
    except Exception:
        pass


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if not context.args:
        keyboard = [
            [
                InlineKeyboardButton("🎵 ᴘʟᴀʏ sᴏɴɢ", switch_inline_query_current_chat="/play "),
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"),
            ],
            [dev_btn()],
        ]
        await update.message.reply_text(
            f"🎵 *ʜᴇʏ [{esc(user.first_name)}](tg://user?id={user.id})\\!*\n\n"
            "ᴜsᴀɢᴇ: `/play song name`\n\n"
            "• `/play Tum Hi Aana`\n"
            "• `/play Kesariya`\n"
            "• `/play Humsafar`",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    # Auto react with random emoji
    asyncio.create_task(auto_react(update, random.choice(["🔍", "🎵", "⏳"])))

    msg = await update.message.reply_text(
        f"🔍 *sᴇᴀʀᴄʜɪɴɢ* `{esc(query)}`\\.\\.\\.",
        parse_mode="MarkdownV2"
    )

    search_query = await gpt_assistant.suggest_song_search(query)
    song_data = await music_fetcher.search_music(search_query)

    if not song_data:
        keyboard = [
            [InlineKeyboardButton("🔁 ᴛʀʏ ᴀɢᴀɪɴ", switch_inline_query_current_chat="/play ")],
            [dev_btn()],
        ]
        await msg.edit_text(
            f"❌ *ɴᴏᴛ ғᴏᴜɴᴅ:* `{esc(query)}`\n\n"
            "💡 ᴛɪᴘs: ᴀᴅᴅ ᴀʀᴛɪsᴛ ɴᴀᴍᴇ",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    added = await queue_manager.add_song(chat_id, song_data, user.id)

    if not added:
        keyboard = [
            [InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"), InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear")],
            [dev_btn()],
        ]
        await msg.edit_text("❌ *ǫᴜᴇᴜᴇ ɪs ғᴜʟʟ\\!*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    title = song_data.get("title", "Unknown")
    duration = song_data.get("duration", 0)
    dur_str = fmt(duration)
    q_len = await queue_manager.get_queue_length(chat_id)
    source = song_data.get("source", "")
    webpage = song_data.get("webpage_url", "")

    # Try voice chat
    vc_text = ""
    if is_voice_available():
        vc = await voice_play(chat_id, query, song_data)
        if vc["success"]:
            vc_text = "\n🔊 *ᴘʟᴀʏɪɴɢ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*"
            asyncio.create_task(auto_react(update, random.choice(PLAY_REACTIONS)))
        else:
            vc_text = f"\n⚠️ _{esc(vc.get('msg','VC unavailable'))}_"
    else:
        asyncio.create_task(auto_react(update, random.choice(ADDED_REACTIONS)))

    keyboard = [
        [
            InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="mc_pause"),
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"),
            InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", callback_data="mc_resume"),
        ],
        [
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"),
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"),
            InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"),
        ],
        [
            InlineKeyboardButton("🔇 ʟᴇᴀᴠᴇ ᴠᴄ", callback_data="mc_leave"),
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴏʀᴇ", switch_inline_query_current_chat="/play "),
        ],
    ]
    if webpage:
        keyboard.append([InlineKeyboardButton("🔗 ᴏᴘᴇɴ sᴏɴɢ", url=webpage)])
    keyboard.append([dev_btn()])

    await msg.edit_text(
        f"✅ *ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\\!*{vc_text}\n\n"
        f"🎵 *{esc(title[:65])}*\n"
        f"⏱ ᴅᴜʀᴀᴛɪᴏɴ ➤ `{dur_str}`\n"
        f"📍 sᴏᴜʀᴄᴇ ➤ {esc(source)}\n"
        f"📊 ᴘᴏsɪᴛɪᴏɴ ➤ \\#{q_len}\n"
        f"👤 ʙʏ ➤ [{esc(user.first_name)}](tg://user?id={user.id})",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    next_song = await queue_manager.get_next_song(chat_id)

    if not next_song:
        await update.message.reply_text("🎵 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*", parse_mode="MarkdownV2")
        return

    title = next_song.get("title", "Unknown")
    dur_str = fmt(next_song.get("duration", 0))

    vc_text = ""
    if is_voice_available():
        vc = await voice_play(chat_id, title, next_song)
        vc_text = "\n🔊 *ᴘʟᴀʏɪɴɢ\\!*" if vc["success"] else f"\n_{esc(vc.get('msg',''))}_"

    asyncio.create_task(auto_react(update, random.choice(SKIP_REACTIONS)))

    keyboard = [
        [InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="mc_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue")],
        [dev_btn()],
    ]
    await update.message.reply_text(
        f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!*{vc_text}\n\n🎵 *{esc(title[:65])}*\n⏱ `{dur_str}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    now = get_now_playing(chat_id)
    next_s = await queue_manager.peek_next_song(chat_id)

    text = ""
    if now:
        text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 *{esc(now.get('title','')[:50])}*\n\n"
    if next_s:
        text += f"▶️ *ɴᴇxᴛ:*\n🎵 *{esc(next_s.get('title','')[:50])}*\n⏱ `{fmt(next_s.get('duration',0))}`"
    else:
        text += "📭 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ*"

    keyboard = [
        [InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue")],
        [dev_btn()],
    ]
    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    queue = await queue_manager.get_queue(chat_id)
    now = get_now_playing(chat_id)

    if not queue and not now:
        keyboard = [
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ sᴏɴɢ", switch_inline_query_current_chat="/play ")],
            [dev_btn()],
        ]
        await update.message.reply_text(
            "📭 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*\n\n`/play song name` ᴛᴏ ᴀᴅᴅ sᴏɴɢs",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = ""
    if now:
        text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 {esc(now.get('title','')[:45])}\n\n"

    if queue:
        text += f"📋 *ǫᴜᴇᴜᴇ — {len(queue)} sᴏɴɢ{'s' if len(queue)>1 else ''}*\n\n"
        for i, s in enumerate(queue[:10], 1):
            t = esc(s.get("title","Unknown")[:35])
            d = fmt(s.get("duration",0))
            text += f"`{i}.` {t} ┃ `{d}`\n"
        if len(queue) > 10:
            text += f"\n_\\+{len(queue)-10} ᴍᴏʀᴇ_"

    keyboard = [
        [
            InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="mc_pause"),
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"),
            InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", callback_data="mc_resume"),
        ],
        [
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"),
            InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"),
            InlineKeyboardButton("🔇 ʟᴇᴀᴠᴇ ᴠᴄ", callback_data="mc_leave"),
        ],
        [InlineKeyboardButton("➕ ᴀᴅᴅ sᴏɴɢ", switch_inline_query_current_chat="/play "), dev_btn()],
    ]
    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    count = await queue_manager.clear_queue(chat_id)
    await voice_leave(chat_id)
    asyncio.create_task(auto_react(update, "🗑"))
    keyboard = [
        [InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play "), dev_btn()],
    ]
    await update.message.reply_text(
        f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if await queue_manager.shuffle_queue(chat_id):
        asyncio.create_task(auto_react(update, "🔀"))
        keyboard = [[InlineKeyboardButton("📋 ᴠɪᴇᴡ ǫᴜᴇᴜᴇ", callback_data="mc_queue"), dev_btn()]]
        await update.message.reply_text("🔀 *ǫᴜᴇᴜᴇ sʜᴜғғʟᴇᴅ\\!*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ *ɴᴏᴛ ᴇɴᴏᴜɢʜ sᴏɴɢs\\!*", parse_mode="MarkdownV2")


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: `/remove pos`", parse_mode="MarkdownV2")
        return
    try:
        pos = int(context.args[0]) - 1
        if pos < 0:
            await update.message.reply_text("❌ ᴘᴏsɪᴛɪᴏɴ ≥ 1", parse_mode="MarkdownV2")
            return
        song = await queue_manager.remove_song(update.effective_chat.id, pos)
        if song:
            keyboard = [[InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"), dev_btn()]]
            await update.message.reply_text(
                f"❌ *ʀᴇᴍᴏᴠᴇᴅ:*\n🎵 {esc(song.get('title','')[:55])}",
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text("❌ *ɪɴᴠᴀʟɪᴅ ᴘᴏsɪᴛɪᴏɴ\\!*", parse_mode="MarkdownV2")
    except ValueError:
        await update.message.reply_text("❌ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴅᴇ\\!", parse_mode="MarkdownV2")


async def music_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == "mc_skip":
        next_song = await queue_manager.get_next_song(chat_id)
        if next_song:
            title = next_song.get("title", "Unknown")
            dur = fmt(next_song.get("duration", 0))
            vc_text = ""
            if is_voice_available():
                vc = await voice_play(chat_id, title, next_song)
                vc_text = " 🔊" if vc["success"] else ""
            kb = [[InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="mc_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue")], [dev_btn()]]
            await query.edit_message_text(
                f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!*{vc_text}\n\n🎵 *{esc(title[:60])}*\n⏱ `{dur}`",
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            await query.edit_message_text("📭 *ǫᴜᴇᴜᴇ ᴇᴍᴘᴛʏ\\!*", parse_mode="MarkdownV2")

    elif query.data == "mc_pause":
        ok = await voice_pause(chat_id)
        await query.answer("⏸ Paused!" if ok else "Not in VC!", show_alert=not ok)

    elif query.data == "mc_resume":
        ok = await voice_resume(chat_id)
        await query.answer("▶️ Resumed!" if ok else "Not paused!", show_alert=not ok)

    elif query.data == "mc_leave":
        ok = await voice_leave(chat_id)
        kb = [[InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴀɢᴀɪɴ", switch_inline_query_current_chat="/play "), dev_btn()]]
        await query.edit_message_text(
            "🔇 *ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*" if ok else "❌ *ɴᴏᴛ ɪɴ ᴀ ᴠᴄ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif query.data == "mc_queue":
        queue = await queue_manager.get_queue(chat_id)
        now = get_now_playing(chat_id)
        if not queue and not now:
            await query.answer("Queue is empty!", show_alert=True)
            return
        text = ""
        if now:
            text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 {esc(now.get('title','')[:40])}\n\n"
        if queue:
            text += f"📋 *{len(queue)} sᴏɴɢs*\n\n"
            for i, s in enumerate(queue[:8], 1):
                text += f"`{i}.` {esc(s.get('title','')[:35])} ┃ `{fmt(s.get('duration',0))}`\n"
            if len(queue) > 8:
                text += f"\n_\\+{len(queue)-8} ᴍᴏʀᴇ_"
        kb = [
            [InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="mc_pause"), InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"), InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", callback_data="mc_resume")],
            [InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"), InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"), InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="mc_queue")],
            [dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "mc_shuffle":
        if await queue_manager.shuffle_queue(chat_id):
            await query.answer("🔀 Shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    elif query.data == "mc_clear":
        count = await queue_manager.clear_queue(chat_id)
        await voice_leave(chat_id)
        kb = [[InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play "), dev_btn()]]
        await query.edit_message_text(
            f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(kb)
        )
