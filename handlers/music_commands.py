import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils.music_fetcher import MusicFetcher
from utils.mongo_queue_manager import MongoQueueManager
from utils.claude_assistant import GPTAssistant
from utils.voice_chat import join_and_play, leave_voice_chat, pause_voice_chat, resume_voice_chat, get_now_playing

logger = logging.getLogger(__name__)
music_fetcher = MusicFetcher()
queue_manager = MongoQueueManager()
gpt_assistant = GPTAssistant()

DEV_URL = "tg://resolve?domain=secret_fetcher"


def dev_button():
    return InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)


def fmt_dur(seconds) -> str:
    if not seconds:
        return "0:00"
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def safe_md(text: str) -> str:
    special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in special:
        text = text.replace(ch, f'\\{ch}')
    return text


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play a song - adds to queue AND streams in voice chat"""
    user = update.effective_user
    user_name = user.first_name

    if not context.args:
        keyboard = [
            [InlineKeyboardButton("🎵 ᴛʀʏ ᴘʟᴀʏɪɴɢ", switch_inline_query_current_chat="/play ")],
            [dev_button()],
        ]
        await update.message.reply_text(
            f"🎵 *ʜᴇʏ {safe_md(user_name)}\\!*\n\n"
            "ᴜsᴀɢᴇ: `/play song name`\n\n"
            "*ᴇxᴀᴍᴘʟᴇs:*\n"
            "• `/play Tum Hi Aana`\n"
            "• `/play Shape of You`\n"
            "• `/play Humsafar`",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    query = " ".join(context.args)
    chat_id = update.effective_chat.id
    await update.message.chat.send_action(ChatAction.TYPING)

    search_msg = await update.message.reply_text(
        f"🔍 *sᴇᴀʀᴄʜɪɴɢ:* `{safe_md(query)}`\\.\\.\\.",
        parse_mode="MarkdownV2"
    )

    search_query = await gpt_assistant.suggest_song_search(query)
    song_data = await music_fetcher.search_music(search_query)

    if not song_data:
        keyboard = [
            [InlineKeyboardButton("🔁 ᴛʀʏ ᴀɢᴀɪɴ", switch_inline_query_current_chat="/play ")],
            [dev_button()],
        ]
        await search_msg.edit_text(
            f"❌ *ɴᴏᴛ ғᴏᴜɴᴅ:* `{safe_md(query)}`\n\n"
            "💡 *ᴛɪᴘs:*\n"
            "┣ ᴄʜᴇᴄᴋ sᴘᴇʟʟɪɴɢ\n"
            "┣ ᴀᴅᴅ ᴀʀᴛɪsᴛ ɴᴀᴍᴇ\n"
            "┗ ᴛʀʏ ᴇɴɢʟɪsʜ ɴᴀᴍᴇ",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Add to queue
    requester_id = user.id
    added = await queue_manager.add_song(chat_id, song_data, requester_id)

    title = song_data.get("title", "Unknown")
    duration = song_data.get("duration", 0)
    duration_str = fmt_dur(duration)
    queue_length = await queue_manager.get_queue_length(chat_id)
    webpage_url = song_data.get("webpage_url", "")
    source = song_data.get("source", "Unknown")

    if not added:
        keyboard = [
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"),
            ],
            [dev_button()],
        ]
        await search_msg.edit_text(
            "❌ *ǫᴜᴇᴜᴇ ɪs ғᴜʟʟ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # Try to play in voice chat
    vc_result = await join_and_play(chat_id, query, song_data)
    vc_status = ""
    if vc_result["success"]:
        vc_status = "\n🔊 *ᴘʟᴀʏɪɴɢ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*"
    else:
        vc_status = f"\n⚠️ _{safe_md(vc_result['msg'])}_"

    keyboard = [
        [
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"),
            InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="mc_pause"),
            InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", callback_data="mc_resume"),
        ],
        [
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"),
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"),
            InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"),
        ],
        [
            InlineKeyboardButton("🔇 ʟᴇᴀᴠᴇ ᴠᴄ", callback_data="mc_leave_vc"),
            InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴏʀᴇ", switch_inline_query_current_chat="/play "),
        ],
    ]
    if webpage_url:
        keyboard.append([InlineKeyboardButton("🔗 ᴏᴘᴇɴ sᴏɴɢ", url=webpage_url)])
    keyboard.append([dev_button()])

    await search_msg.edit_text(
        f"✅ *ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ\\!*{vc_status}\n\n"
        f"🎵 *{safe_md(title[:65])}*\n"
        f"⏱ ᴅᴜʀᴀᴛɪᴏɴ ➤ `{duration_str}`\n"
        f"📍 sᴏᴜʀᴄᴇ ➤ {safe_md(source)}\n"
        f"📊 ᴘᴏsɪᴛɪᴏɴ ➤ \\#{queue_length}\n"
        f"👤 ʙʏ ➤ [{safe_md(user_name)}](tg://user?id={user.id})",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    next_song = await queue_manager.peek_next_song(group_id)
    if not next_song:
        await update.message.reply_text("🎵 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*", parse_mode="MarkdownV2")
        return
    title = next_song.get("title", "Unknown")
    duration_str = fmt_dur(next_song.get("duration", 0))
    keyboard = [[
        InlineKeyboardButton("⏭ sᴋɪᴘ ᴛᴏ ᴛʜɪs", callback_data="mc_skip"),
        InlineKeyboardButton("📋 ғᴜʟʟ ǫᴜᴇᴜᴇ", callback_data="mc_queue"),
    ], [dev_button()]]
    await update.message.reply_text(
        f"▶️ *ɴᴇxᴛ sᴏɴɢ:*\n\n🎵 *{safe_md(title[:65])}*\n⏱ `{duration_str}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    next_song = await queue_manager.get_next_song(group_id)
    if not next_song:
        await update.message.reply_text("🎵 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*", parse_mode="MarkdownV2")
        return

    title = next_song.get("title", "Unknown")
    duration_str = fmt_dur(next_song.get("duration", 0))

    # Play next in voice chat
    vc_result = await join_and_play(group_id, title, next_song)
    vc_status = "🔊 *ᴘʟᴀʏɪɴɢ ɪɴ ᴠᴄ\\!*" if vc_result["success"] else f"_{safe_md(vc_result['msg'])}_"

    keyboard = [[
        InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="mc_skip"),
        InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"),
    ], [dev_button()]]
    await update.message.reply_text(
        f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!* {vc_status}\n\n🎵 *{safe_md(title[:65])}*\n⏱ `{duration_str}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    queue = await queue_manager.get_queue(group_id)
    now = get_now_playing(group_id)

    if not queue and not now:
        keyboard = [
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴀ sᴏɴɢ", switch_inline_query_current_chat="/play ")],
            [dev_button()],
        ]
        await update.message.reply_text(
            "📋 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = ""
    if now:
        text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 {safe_md(now['title'][:45])}\n\n"

    if queue:
        text += f"📋 *ǫᴜᴇᴜᴇ — {len(queue)} sᴏɴɢs*\n\n"
        for i, song in enumerate(queue[:10], 1):
            title = safe_md(song.get("title", "Unknown")[:38])
            dur = fmt_dur(song.get("duration", 0))
            text += f"`{i}.` {title} ┃ `{dur}`\n"
        if len(queue) > 10:
            text += f"\n_\\+{len(queue) - 10} ᴍᴏʀᴇ_"

    keyboard = [
        [
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"),
            InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="mc_pause"),
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"),
        ],
        [
            InlineKeyboardButton("🔇 ʟᴇᴀᴠᴇ ᴠᴄ", callback_data="mc_leave_vc"),
            InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear"),
        ],
        [dev_button()],
    ]
    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    count = await queue_manager.clear_queue(group_id)
    keyboard = [
        [InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play ")],
        [dev_button()],
    ]
    await update.message.reply_text(
        f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    if await queue_manager.shuffle_queue(group_id):
        keyboard = [[InlineKeyboardButton("📋 ᴠɪᴇᴡ ǫᴜᴇᴜᴇ", callback_data="mc_queue"), dev_button()]]
        await update.message.reply_text("🔀 *ǫᴜᴇᴜᴇ sʜᴜғғʟᴇᴅ\\!*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("❌ *ɴᴏᴛ ᴇɴᴏᴜɢʜ sᴏɴɢs\\!*", parse_mode="MarkdownV2")


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: `/remove position`", parse_mode="MarkdownV2")
        return
    try:
        position = int(context.args[0]) - 1
        if position < 0:
            await update.message.reply_text("❌ ᴘᴏsɪᴛɪᴏɴ ≥ 1", parse_mode="MarkdownV2")
            return
        group_id = update.effective_chat.id
        song = await queue_manager.remove_song(group_id, position)
        if song:
            title = safe_md(song.get("title", "Unknown")[:55])
            await update.message.reply_text(f"❌ *ʀᴇᴍᴏᴠᴇᴅ:*\n🎵 {title}", parse_mode="MarkdownV2",
                                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue"), dev_button()]]))
        else:
            await update.message.reply_text("❌ *ɪɴᴠᴀʟɪᴅ ᴘᴏsɪᴛɪᴏɴ\\!*", parse_mode="MarkdownV2")
    except ValueError:
        await update.message.reply_text("❌ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴅᴇ\\!", parse_mode="MarkdownV2")


async def music_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_id = query.message.chat_id

    if query.data == "mc_skip":
        next_song = await queue_manager.get_next_song(group_id)
        if next_song:
            title = safe_md(next_song.get("title", "Unknown")[:55])
            dur = fmt_dur(next_song.get("duration", 0))
            await join_and_play(group_id, next_song.get("title", ""), next_song)
            keyboard = [[InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="mc_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="mc_queue")], [dev_button()]]
            await query.edit_message_text(f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!*\n\n🎵 *{title}*\n⏱ `{dur}`", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.edit_message_text("🎵 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*", parse_mode="MarkdownV2")

    elif query.data == "mc_pause":
        success = await pause_voice_chat(group_id)
        await query.answer("⏸ Paused!" if success else "Not playing!", show_alert=not success)

    elif query.data == "mc_resume":
        success = await resume_voice_chat(group_id)
        await query.answer("▶️ Resumed!" if success else "Nothing to resume!", show_alert=not success)

    elif query.data == "mc_leave_vc":
        success = await leave_voice_chat(group_id)
        keyboard = [[InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴀɢᴀɪɴ", switch_inline_query_current_chat="/play ")], [dev_button()]]
        await query.edit_message_text(
            "🔇 *ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*" if success else "❌ *ɴᴏᴛ ɪɴ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "mc_queue":
        queue = await queue_manager.get_queue(group_id)
        now = get_now_playing(group_id)
        if not queue and not now:
            await query.answer("Queue is empty!", show_alert=True)
            return
        text = ""
        if now:
            text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 {safe_md(now['title'][:40])}\n\n"
        if queue:
            text += f"📋 *ǫᴜᴇᴜᴇ — {len(queue)} sᴏɴɢs*\n\n"
            for i, song in enumerate(queue[:8], 1):
                title = safe_md(song.get("title", "Unknown")[:38])
                dur = fmt_dur(song.get("duration", 0))
                text += f"`{i}.` {title} ┃ `{dur}`\n"
            if len(queue) > 8:
                text += f"\n_\\+{len(queue) - 8} ᴍᴏʀᴇ_"
        keyboard = [[InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="mc_skip"), InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="mc_shuffle"), InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="mc_clear")], [dev_button()]]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "mc_shuffle":
        if await queue_manager.shuffle_queue(group_id):
            await query.answer("🔀 Shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    elif query.data == "mc_clear":
        count = await queue_manager.clear_queue(group_id)
        await leave_voice_chat(group_id)
        keyboard = [[InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play ")], [dev_button()]]
        await query.edit_message_text(f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*", parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))
