import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils.music_fetcher import MusicFetcher
from utils.mongo_queue_manager import MongoQueueManager
from utils.claude_assistant import GPTAssistant

logger = logging.getLogger(__name__)
music_fetcher = MusicFetcher()
queue_manager = MongoQueueManager()
gpt_assistant = GPTAssistant()


def fmt_dur(seconds) -> str:
    if not seconds:
        return "0:00"
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def safe_md(text: str) -> str:
    """Escape MarkdownV2 special chars"""
    special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in special:
        text = text.replace(ch, f'\\{ch}')
    return text


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play a song"""
    user = update.effective_user
    user_name = user.first_name

    if not context.args:
        keyboard = [[InlineKeyboardButton("🎵 How to play?", callback_data="how_to_play")]]
        await update.message.reply_text(
            f"🎵 *Hey {safe_md(user_name)}\\!*\n\n"
            "Usage: `/play song name`\n\n"
            "*Examples:*\n"
            "• `/play Tum Hi Aana`\n"
            "• `/play Shape of You`\n"
            "• `/play Humsafar`",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    # Show searching message
    search_msg = await update.message.reply_text(
        f"🔍 Searching: *{safe_md(query)}*\\.\\.\\.",
        parse_mode="MarkdownV2"
    )

    # Get better search query from AI
    search_query = await gpt_assistant.suggest_song_search(query)

    # Search YouTube
    song_data = await music_fetcher.search_music(search_query)

    if not song_data:
        await search_msg.edit_text(
            f"❌ *Could not find:* {safe_md(query)}\n\n"
            "💡 Try:\n"
            "• Different spelling\n"
            "• Add artist name\n"
            "• English song name",
            parse_mode="MarkdownV2"
        )
        return

    group_id = update.effective_chat.id
    requester_id = update.effective_user.id
    added = await queue_manager.add_song(group_id, song_data, requester_id)

    if added:
        title = song_data.get("title", "Unknown")
        duration = song_data.get("duration", 0)
        duration_str = fmt_dur(duration)
        queue_length = await queue_manager.get_queue_length(group_id)
        webpage_url = song_data.get("webpage_url", "")

        keyboard = [
            [
                InlineKeyboardButton("⏭️ Skip", callback_data="btn_skip"),
                InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
            ],
            [
                InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
                InlineKeyboardButton("🗑️ Clear All", callback_data="btn_clear"),
            ],
        ]
        if webpage_url:
            keyboard.append([InlineKeyboardButton("🔗 Open on YouTube", url=webpage_url)])

        await search_msg.edit_text(
            f"✅ *Added to Queue\\!*\n\n"
            f"🎵 *{safe_md(title[:70])}*\n"
            f"⏱ Duration: `{duration_str}`\n"
            f"📍 Source: YouTube\n"
            f"📊 Position: \\#{queue_length}\n"
            f"👤 Added by: [{safe_md(user_name)}](tg://user?id={user.id})",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await search_msg.edit_text(
            "❌ *Queue is full\\!*\n\nUse /skip or /clear\\_queue first\\.",
            parse_mode="MarkdownV2"
        )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show next song"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.peek_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 *Queue is empty\\!*", parse_mode="MarkdownV2")
        return

    title = next_song.get("title", "Unknown")
    duration_str = fmt_dur(next_song.get("duration", 0))

    keyboard = [[
        InlineKeyboardButton("⏭️ Skip to this", callback_data="btn_skip"),
        InlineKeyboardButton("📋 Full Queue", callback_data="btn_queue"),
    ]]

    await update.message.reply_text(
        f"▶️ *Next Song:*\n\n"
        f"🎵 *{safe_md(title[:70])}*\n"
        f"⏱ Duration: `{duration_str}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip current song"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.get_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 *Queue is empty\\!*", parse_mode="MarkdownV2")
        return

    title = next_song.get("title", "Unknown")
    duration_str = fmt_dur(next_song.get("duration", 0))

    keyboard = [[
        InlineKeyboardButton("⏭️ Skip Again", callback_data="btn_skip"),
        InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
    ]]

    await update.message.reply_text(
        f"⏭️ *Skipped\\!*\n\n"
        f"🎵 *{safe_md(title[:70])}*\n"
        f"⏱ Duration: `{duration_str}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display queue"""
    group_id = update.effective_chat.id
    queue = await queue_manager.get_queue(group_id)

    if not queue:
        keyboard = [[InlineKeyboardButton("🎵 Play a Song", switch_inline_query_current_chat="/play ")]]
        await update.message.reply_text(
            "📋 *Queue is empty\\!*\n\nUse `/play song name` to add songs\\.",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = f"📋 *Queue — {len(queue)} song{'s' if len(queue) > 1 else ''}*\n\n"
    for i, song in enumerate(queue[:10], 1):
        title = safe_md(song.get("title", "Unknown")[:45])
        dur = fmt_dur(song.get("duration", 0))
        text += f"`{i}.` {title} \\| `{dur}`\n"

    if len(queue) > 10:
        text += f"\n_\\.\\.\\. and {len(queue) - 10} more songs_"

    keyboard = [
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
            InlineKeyboardButton("🗑️ Clear All", callback_data="btn_clear"),
        ]
    ]

    await update.message.reply_text(
        text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear queue"""
    group_id = update.effective_chat.id
    count = await queue_manager.clear_queue(group_id)
    await update.message.reply_text(
        f"🗑️ *Cleared {count} songs from queue\\!*",
        parse_mode="MarkdownV2"
    )


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shuffle queue"""
    group_id = update.effective_chat.id
    if await queue_manager.shuffle_queue(group_id):
        keyboard = [[InlineKeyboardButton("📋 View Queue", callback_data="btn_queue")]]
        await update.message.reply_text(
            "🔀 *Queue shuffled\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ *Not enough songs to shuffle\\!*", parse_mode="MarkdownV2")


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove song from queue"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/remove position`\nExample: `/remove 2`",
            parse_mode="MarkdownV2"
        )
        return

    try:
        position = int(context.args[0]) - 1
        if position < 0:
            await update.message.reply_text("❌ Position must be 1 or higher\\!", parse_mode="MarkdownV2")
            return

        group_id = update.effective_chat.id
        song = await queue_manager.remove_song(group_id, position)

        if song:
            title = safe_md(song.get("title", "Unknown")[:60])
            await update.message.reply_text(
                f"❌ *Removed:*\n🎵 {title}",
                parse_mode="MarkdownV2"
            )
        else:
            await update.message.reply_text(
                "❌ *Invalid position\\!* Use /queue to see positions\\.",
                parse_mode="MarkdownV2"
            )
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number\\!", parse_mode="MarkdownV2")


async def music_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle music button presses"""
    query = update.callback_query
    await query.answer()
    group_id = query.message.chat_id

    if query.data == "btn_skip":
        next_song = await queue_manager.get_next_song(group_id)
        if next_song:
            title = safe_md(next_song.get("title", "Unknown")[:60])
            dur = fmt_dur(next_song.get("duration", 0))
            keyboard = [[
                InlineKeyboardButton("⏭️ Skip Again", callback_data="btn_skip"),
                InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
            ]]
            await query.edit_message_text(
                f"⏭️ *Skipped\\!*\n\n🎵 *{title}*\n⏱ `{dur}`",
                parse_mode="MarkdownV2",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.edit_message_text("🎵 *Queue is empty\\!*", parse_mode="MarkdownV2")

    elif query.data == "btn_queue":
        queue = await queue_manager.get_queue(group_id)
        if not queue:
            await query.answer("Queue is empty!", show_alert=True)
            return
        text = f"📋 *Queue — {len(queue)} songs*\n\n"
        for i, song in enumerate(queue[:8], 1):
            title = safe_md(song.get("title", "Unknown")[:40])
            dur = fmt_dur(song.get("duration", 0))
            text += f"`{i}.` {title} \\| `{dur}`\n"
        if len(queue) > 8:
            text += f"\n_\\+{len(queue) - 8} more_"
        keyboard = [[
            InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
            InlineKeyboardButton("🗑️ Clear", callback_data="btn_clear"),
        ]]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "btn_shuffle":
        if await queue_manager.shuffle_queue(group_id):
            await query.answer("🔀 Queue shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    elif query.data == "btn_clear":
        count = await queue_manager.clear_queue(group_id)
        await query.edit_message_text(
            f"🗑️ *Cleared {count} songs\\!*",
            parse_mode="MarkdownV2"
        )

    elif query.data == "how_to_play":
        await query.answer(
            "Type /play followed by song name!\nExample: /play Tum Hi Aana",
            show_alert=True
        )
