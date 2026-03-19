import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME, OWNER_ID

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()

DEVELOPER = "@secret\\_fetcher"


def esc(text: str) -> str:
    """Escape ALL MarkdownV2 special chars safely"""
    if not text:
        return ""
    # Convert to plain ASCII-safe string first for display
    safe = ""
    for ch in str(text):
        if ord(ch) > 127:
            # Replace non-ASCII unicode with safe equivalent
            safe += ch
        else:
            safe += ch
    # Now escape MarkdownV2 special chars
    for ch in r'\_*[]()~`>#+-=|{}.!':
        safe = safe.replace(ch, f'\\{ch}')
    return safe


def safe_name(user) -> str:
    """Get safe display name - escape but keep readable"""
    name = user.first_name or "User"
    # Remove/replace problematic unicode bold/italic chars
    cleaned = name.encode('ascii', 'ignore').decode('ascii')
    if not cleaned.strip():
        cleaned = "User"
    return esc(cleaned)


def mention(user) -> str:
    """Create safe mention link"""
    name = safe_name(user)
    return f"[{name}](tg://user?id={user.id})"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    logger.info(f"/start from user_id={user.id}, chat_id={chat.id}")

    # Notify owner — use HTML to avoid MarkdownV2 issues with unicode names
    try:
        chat_info = "Private Chat" if chat.type == "private" else f"Group: {chat.title or 'Unknown'}"
        username = f"@{user.username}" if user.username else "no username"
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=(
                f"🔔 <b>New User Started Bot!</b>\n\n"
                f"👤 Name: <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
                f"🆔 User ID: <code>{user.id}</code>\n"
                f"📱 Username: {username}\n"
                f"💬 Chat: {chat_info}\n"
                f"🆔 Chat ID: <code>{chat.id}</code>"
            ),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.warning(f"Could not notify owner: {e}")

    # Welcome message — use HTML for main message too (safer with unicode names)
    chat_display = "Private" if chat.type == "private" else esc(chat.title or "Group")

    keyboard = [
        [
            InlineKeyboardButton("🎵 Commands", callback_data="util_commands"),
            InlineKeyboardButton("❓ How to Use", callback_data="util_howto"),
        ],
        [
            InlineKeyboardButton("📊 Statistics", callback_data="util_stats"),
            InlineKeyboardButton("ℹ️ About", callback_data="util_about"),
        ],
        [
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        f"<b>🎵 Hey <a href='tg://user?id={user.id}'>{user.first_name}</a>! Welcome to {BOT_NAME}</b>\n\n"
        f"╔══════════════════╗\n"
        f"║  🎧  <b>MUSIC BOT</b>  🎧  ║\n"
        f"╚══════════════════╝\n\n"
        f"✨ <b>Your Premium Music Experience</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎵  Stream from YouTube\n"
        f"📋  Smart queue system\n"
        f"🔀  Shuffle &amp; skip anytime\n"
        f"👥  Group admin controls\n"
        f"📊  Live statistics\n"
        f"📢  Owner broadcasts\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👨‍💻 <b>Dev:</b> @secret_fetcher\n\n"
        f"👇 <b>Choose an option below</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 Play Music", switch_inline_query_current_chat="/play ")],
        [
            InlineKeyboardButton("📋 Queue", callback_data="util_queue"),
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        f"<b>📖 {BOT_NAME} — Commands</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎵 <b>MUSIC</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"▶️ /play &lt;song&gt;\n"
        f"⏭️ /skip — Skip song\n"
        f"⏩ /next — Next info\n"
        f"📋 /queue — View queue\n"
        f"🔀 /shuffle — Shuffle\n"
        f"❌ /remove &lt;pos&gt;\n"
        f"🗑️ /clear_queue\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>ADMIN</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ /init — Setup group\n"
        f"ℹ️ /info — Group info\n"
        f"👑 /admin_add &lt;id&gt;\n"
        f"🚫 /ban &lt;id&gt;\n"
        f"✅ /unban &lt;id&gt;\n"
        f"🔤 /set_prefix &lt;char&gt;\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>OWNER ONLY</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📢 /broadcast &lt;msg&gt;\n\n"
        f"👨‍💻 <b>Dev:</b> @secret_fetcher",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def util_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    def back_btn():
        return [[InlineKeyboardButton("🔙 Back", callback_data="util_back")]]

    if query.data == "util_commands":
        await query.edit_message_text(
            f"🎵 <b>Quick Commands:</b>\n\n"
            f"▶️ /play &lt;song name&gt;\n"
            f"📋 /queue — View queue\n"
            f"⏭️ /skip — Skip song\n"
            f"🔀 /shuffle — Shuffle\n"
            f"🗑️ /clear_queue — Clear all\n"
            f"📊 /stats — Statistics\n"
            f"ℹ️ /info — Group info\n\n"
            f"👨‍💻 <b>Dev:</b> @secret_fetcher",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(back_btn())
        )

    elif query.data == "util_howto":
        await query.edit_message_text(
            f"❓ <b>How to Use:</b>\n\n"
            f"<b>Step 1️⃣</b> — Add bot to your group\n"
            f"<b>Step 2️⃣</b> — Type /init to setup\n"
            f"<b>Step 3️⃣</b> — Type /play Tum Hi Aana\n"
            f"<b>Step 4️⃣</b> — Song added to queue!\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 <b>Pro Tips:</b>\n"
            f"• Use full song name for best results\n"
            f"• Add artist name for accuracy\n"
            f"• /queue to see all songs\n"
            f"• /shuffle for random play\n"
            f"• Admins can /ban spammers\n\n"
            f"👨‍💻 <b>Dev:</b> @secret_fetcher",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(back_btn())
        )

    elif query.data == "util_stats":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.mongo_group_manager import MongoGroupManager
        qm = MongoQueueManager()
        gm = MongoGroupManager()
        chat_id = query.message.chat_id
        settings = await gm.get_group_settings(chat_id)
        queue_len = await qm.get_queue_length(chat_id)

        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="util_stats")],
            [InlineKeyboardButton("🔙 Back", callback_data="util_back")],
        ]
        await query.edit_message_text(
            f"📊 <b>Statistics</b>\n\n"
            f"🎵 Songs Played: <code>{settings['stats']['total_songs_played']}</code>\n"
            f"➕ Songs Queued: <code>{settings['stats']['total_queue_added']}</code>\n"
            f"📻 In Queue Now: <code>{queue_len}</code>\n"
            f"👥 Admins: <code>{len(settings['admins'])}</code>\n"
            f"🚫 Banned Users: <code>{len(settings['banned_users'])}</code>\n\n"
            f"👨‍💻 <b>Dev:</b> @secret_fetcher",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "util_about":
        keyboard = [
            [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)],
            [InlineKeyboardButton("🔙 Back", callback_data="util_back")],
        ]
        await query.edit_message_text(
            f"╔══════════════════╗\n"
            f"║  🎧  <b>MUSIC BOT</b>  🎧  ║\n"
            f"╚══════════════════╝\n\n"
            f"🌟 <b>Premium Music Bot</b>\n\n"
            f"✅ YouTube streaming\n"
            f"✅ Smart queue system\n"
            f"✅ Group admin controls\n"
            f"✅ Live statistics\n"
            f"✅ Owner broadcasts\n"
            f"✅ MongoDB database\n"
            f"✅ 24/7 on Railway\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 <b>Developer:</b> @secret_fetcher\n"
            f"🚀 <b>Hosted:</b> Railway\n"
            f"💾 <b>Database:</b> MongoDB",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "util_queue":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        queue = await qm.get_queue(chat_id)

        if not queue:
            text = f"📋 <b>Queue is empty!</b>\n\nUse /play song name to add songs.\n\n👨‍💻 <b>Dev:</b> @secret_fetcher"
        else:
            text = f"📋 <b>Queue — {len(queue)} song{'s' if len(queue) > 1 else ''}</b>\n\n"
            for i, song in enumerate(queue[:8], 1):
                title = song.get("title", "Unknown")[:38]
                dur = song.get("duration", 0)
                s = int(dur)
                dur_str = f"{s // 60}:{s % 60:02d}"
                text += f"<code>{i}.</code> {title} — <code>{dur_str}</code>\n"
            if len(queue) > 8:
                text += f"\n<i>+{len(queue) - 8} more songs</i>"
            text += f"\n\n👨‍💻 <b>Dev:</b> @secret_fetcher"

        await query.edit_message_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif query.data == "util_back":
        user = query.from_user
        keyboard = [
            [
                InlineKeyboardButton("🎵 Commands", callback_data="util_commands"),
                InlineKeyboardButton("❓ How to Use", callback_data="util_howto"),
            ],
            [
                InlineKeyboardButton("📊 Statistics", callback_data="util_stats"),
                InlineKeyboardButton("ℹ️ About", callback_data="util_about"),
            ],
            [
                InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
            ],
        ]
        await query.edit_message_text(
            f"<b>🎵 Hey <a href='tg://user?id={user.id}'>{user.first_name}</a>! Welcome to {BOT_NAME}</b>\n\n"
            f"╔══════════════════╗\n"
            f"║  🎧  <b>MUSIC BOT</b>  🎧  ║\n"
            f"╚══════════════════╝\n\n"
            f"✨ <b>Your Premium Music Experience</b>\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎵  Stream from YouTube\n"
            f"📋  Smart queue system\n"
            f"🔀  Shuffle &amp; skip anytime\n"
            f"👥  Group admin controls\n"
            f"📊  Live statistics\n"
            f"📢  Owner broadcasts\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👨‍💻 <b>Dev:</b> @secret_fetcher\n\n"
            f"👇 <b>Choose an option below</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ask your question")
        return
    question = " ".join(context.args)
    await update.message.chat.send_action("typing")
    response = await gpt_assistant.get_response(question)
    await update.message.reply_text(response)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from utils.mongo_queue_manager import MongoQueueManager
    from utils.mongo_group_manager import MongoGroupManager
    qm = MongoQueueManager()
    gm = MongoGroupManager()
    group_id = update.effective_chat.id
    settings = await gm.get_group_settings(group_id)
    queue_length = await qm.get_queue_length(group_id)

    keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="util_stats")]]
    await update.message.reply_text(
        f"📊 <b>Statistics</b>\n\n"
        f"🎵 Songs Played: <code>{settings['stats']['total_songs_played']}</code>\n"
        f"➕ Songs Queued: <code>{settings['stats']['total_queue_added']}</code>\n"
        f"📻 In Queue: <code>{queue_length}</code>\n"
        f"👥 Admins: <code>{len(settings['admins'])}</code>\n"
        f"🚫 Banned: <code>{len(settings['banned_users'])}</code>\n\n"
        f"👨‍💻 <b>Dev:</b> @secret_fetcher",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
         InlineKeyboardButton("📋 Commands", callback_data="util_commands")],
    ]
    await update.message.reply_text(
        f"╔══════════════════╗\n"
        f"║  🎧  <b>MUSIC BOT</b>  🎧  ║\n"
        f"╚══════════════════╝\n\n"
        f"✅ YouTube streaming\n"
        f"✅ Queue management\n"
        f"✅ Group controls\n"
        f"✅ 24/7 on Railway\n\n"
        f"👨‍💻 <b>Dev:</b> @secret_fetcher",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")
    try:
        await update.message.reply_text(
            "❌ Something went wrong. Please try again."
        )
    except Exception:
        pass
