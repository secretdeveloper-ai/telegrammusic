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

DEV = "@secret_fetcher"


def fmt(seconds) -> str:
    if not seconds:
        return "0:00"
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def hesc(text: str) -> str:
    """Escape HTML special chars"""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not context.args:
        keyboard = [[InlineKeyboardButton("💡 Example", callback_data="play_example")]]
        await update.message.reply_text(
            f"🎵 <b>How to play a song:</b>\n\n"
            f"▶️ /play Tum Hi Aana\n"
            f"▶️ /play Shape of You\n"
            f"▶️ /play Humsafar\n\n"
            f"<i>Just type the song name after /play</i>\n\n"
            f"👨‍💻 {DEV}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    search_msg = await update.message.reply_text(
        f"🔍 <b>Searching...</b> <code>{hesc(query)}</code>",
        parse_mode="HTML"
    )

    search_query = await gpt_assistant.suggest_song_search(query)
    song_data = await music_fetcher.search_music(search_query)

    if not song_data:
        keyboard = [[InlineKeyboardButton("🔄 Try Again", switch_inline_query_current_chat=f"/play {query}")]]
        await search_msg.edit_text(
            f"❌ <b>Not Found:</b> <code>{hesc(query)}</code>\n\n"
            f"💡 <b>Tips:</b>\n"
            f"• Check spelling\n"
            f"• Add artist name\n"
            f"• Try English name\n\n"
            f"👨‍💻 {DEV}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    group_id = update.effective_chat.id
    added = await queue_manager.add_song(group_id, song_data, user.id)

    if added:
        title = hesc(song_data.get("title", "Unknown")[:65])
        duration_str = fmt(song_data.get("duration", 0))
        queue_length = await queue_manager.get_queue_length(group_id)
        webpage_url = song_data.get("webpage_url", "")
        uploader = hesc(song_data.get("uploader", "YouTube")[:30])

        keyboard = [
            [
                InlineKeyboardButton("⏭️ Skip", callback_data="btn_skip"),
                InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
            ],
            [
                InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
                InlineKeyboardButton("🗑️ Clear", callback_data="btn_clear"),
            ],
        ]
        if webpage_url:
            keyboard.append([InlineKeyboardButton("▶️ Open on YouTube", url=webpage_url)])

        await search_msg.edit_text(
            f"✅ <b>Added to Queue!</b>\n\n"
            f"🎵 <b>{title}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱  Duration: <code>{duration_str}</code>\n"
            f"📍  Source: YouTube\n"
            f"🎤  By: {uploader}\n"
            f"📊  Position: <code>#{queue_length}</code>\n"
            f"👤  Added by: <a href='tg://user?id={user.id}'>{hesc(user.first_name)}</a>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 {DEV}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await search_msg.edit_text(
            f"❌ <b>Queue is full!</b>\n\nUse /skip or /clear_queue first.\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    next_song = await queue_manager.peek_next_song(group_id)

    if not next_song:
        await update.message.reply_text(
            f"📋 <b>Queue is empty!</b>\n\nAdd songs with /play song name\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )
        return

    keyboard = [[
        InlineKeyboardButton("⏭️ Skip Now", callback_data="btn_skip"),
        InlineKeyboardButton("📋 Full Queue", callback_data="btn_queue"),
    ]]
    await update.message.reply_text(
        f"▶️ <b>Up Next:</b>\n\n"
        f"🎵 <b>{hesc(next_song.get('title', 'Unknown')[:65])}</b>\n"
        f"⏱  <code>{fmt(next_song.get('duration', 0))}</code>\n\n"
        f"👨‍💻 {DEV}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    song = await queue_manager.get_next_song(group_id)

    if not song:
        await update.message.reply_text(
            f"📋 <b>Queue is empty!</b>\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )
        return

    keyboard = [[
        InlineKeyboardButton("⏭️ Skip Again", callback_data="btn_skip"),
        InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
    ]]
    await update.message.reply_text(
        f"⏭️ <b>Skipped!</b>\n\n"
        f"🎵 <b>{hesc(song.get('title', 'Unknown')[:65])}</b>\n"
        f"⏱  <code>{fmt(song.get('duration', 0))}</code>\n\n"
        f"👨‍💻 {DEV}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    queue = await queue_manager.get_queue(group_id)

    if not queue:
        keyboard = [[InlineKeyboardButton("🎵 Add a Song", switch_inline_query_current_chat="/play ")]]
        await update.message.reply_text(
            f"📋 <b>Queue is empty!</b>\n\nUse /play song name to add songs.\n\n👨‍💻 {DEV}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = f"📋 <b>Queue — {len(queue)} song{'s' if len(queue) > 1 else ''}</b>\n\n"
    for i, song in enumerate(queue[:10], 1):
        title = hesc(song.get("title", "Unknown")[:42])
        dur = fmt(song.get("duration", 0))
        text += f"<code>{i}.</code> {title} — <code>{dur}</code>\n"
    if len(queue) > 10:
        text += f"\n<i>+{len(queue) - 10} more</i>"
    text += f"\n\n👨‍💻 {DEV}"

    keyboard = [[
        InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
        InlineKeyboardButton("🗑️ Clear All", callback_data="btn_clear"),
    ]]
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    count = await queue_manager.clear_queue(group_id)
    await update.message.reply_text(
        f"🗑️ <b>Cleared {count} songs!</b>\n\n👨‍💻 {DEV}",
        parse_mode="HTML"
    )


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    if await queue_manager.shuffle_queue(group_id):
        keyboard = [[InlineKeyboardButton("📋 View Queue", callback_data="btn_queue")]]
        await update.message.reply_text(
            f"🔀 <b>Queue shuffled!</b>\n\n👨‍💻 {DEV}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            f"❌ <b>Not enough songs!</b>\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            f"Usage: /remove 2\n<i>Remove song at position 2</i>\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )
        return
    try:
        position = int(context.args[0]) - 1
        if position < 0:
            await update.message.reply_text(f"❌ Position must be 1 or higher!\n\n👨‍💻 {DEV}", parse_mode="HTML")
            return
        group_id = update.effective_chat.id
        song = await queue_manager.remove_song(group_id, position)
        if song:
            await update.message.reply_text(
                f"❌ <b>Removed:</b>\n🎵 {hesc(song.get('title', 'Unknown')[:60])}\n\n👨‍💻 {DEV}",
                parse_mode="HTML"
            )
        else:
            await update.message.reply_text(
                f"❌ <b>Invalid position!</b>\nUse /queue to see positions.\n\n👨‍💻 {DEV}",
                parse_mode="HTML"
            )
    except ValueError:
        await update.message.reply_text(f"❌ Enter a valid number!\n\n👨‍💻 {DEV}", parse_mode="HTML")


async def music_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    group_id = query.message.chat_id

    if query.data == "btn_skip":
        song = await queue_manager.get_next_song(group_id)
        if song:
            keyboard = [[
                InlineKeyboardButton("⏭️ Skip Again", callback_data="btn_skip"),
                InlineKeyboardButton("📋 Queue", callback_data="btn_queue"),
            ]]
            await query.edit_message_text(
                f"⏭️ <b>Skipped!</b>\n\n"
                f"🎵 <b>{hesc(song.get('title', 'Unknown')[:65])}</b>\n"
                f"⏱  <code>{fmt(song.get('duration', 0))}</code>\n\n"
                f"👨‍💻 {DEV}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.edit_message_text(
                f"📋 <b>Queue is empty!</b>\n\n👨‍💻 {DEV}",
                parse_mode="HTML"
            )

    elif query.data == "btn_queue":
        queue = await queue_manager.get_queue(group_id)
        if not queue:
            await query.answer("Queue is empty!", show_alert=True)
            return
        text = f"📋 <b>Queue — {len(queue)} songs</b>\n\n"
        for i, song in enumerate(queue[:8], 1):
            title = hesc(song.get("title", "Unknown")[:38])
            dur = fmt(song.get("duration", 0))
            text += f"<code>{i}.</code> {title} — <code>{dur}</code>\n"
        if len(queue) > 8:
            text += f"\n<i>+{len(queue) - 8} more</i>"
        text += f"\n\n👨‍💻 {DEV}"
        keyboard = [[
            InlineKeyboardButton("🔀 Shuffle", callback_data="btn_shuffle"),
            InlineKeyboardButton("🗑️ Clear", callback_data="btn_clear"),
        ]]
        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "btn_shuffle":
        if await queue_manager.shuffle_queue(group_id):
            await query.answer("🔀 Shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    elif query.data == "btn_clear":
        count = await queue_manager.clear_queue(group_id)
        await query.edit_message_text(
            f"🗑️ <b>Cleared {count} songs!</b>\n\n👨‍💻 {DEV}",
            parse_mode="HTML"
        )

    elif query.data == "play_example":
        await query.answer("Type /play followed by song name!\nExample: /play Tum Hi Aana", show_alert=True)
