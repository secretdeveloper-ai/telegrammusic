import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()


def safe_md(text: str) -> str:
    special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in special:
        text = text.replace(ch, f'\\{ch}')
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with attractive UI and user tagging"""
    user = update.effective_user
    logger.info(f"/start from user_id={user.id}, chat_id={update.effective_chat.id}")

    user_mention = f"[{safe_md(user.first_name)}](tg://user?id={user.id})"

    welcome_text = (
        f"🎵 *Hey {user_mention}\\! Welcome to {safe_md(BOT_NAME)}*\n\n"
        "┌─────────────────────┐\n"
        "│  🎧 *MUSIC BOT*  │\n"
        "│  Your Music Partner  │\n"
        "└─────────────────────┘\n\n"
        "🌟 *Features:*\n"
        "╠ 🎵 Play from YouTube\n"
        "╠ 📋 Queue management\n"
        "╠ 🔀 Shuffle & skip\n"
        "╠ 👥 Group admin tools\n"
        "╠ 📊 Usage statistics\n"
        "╚ 📢 Owner broadcast\n\n"
        "👇 *Tap a button to get started\\!*"
    )

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
            InlineKeyboardButton("💬 Support Chat", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help with buttons"""
    help_text = (
        "📖 *COMMANDS LIST*\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "🎵 *MUSIC*\n"
        "━━━━━━━━━━━━━━━━\n"
        "▶️ `/play` \\<song\\>\n"
        "⏭️ `/skip` — Skip song\n"
        "⏩ `/next` — Next info\n"
        "📋 `/queue` — View queue\n"
        "🔀 `/shuffle` — Shuffle\n"
        "❌ `/remove` \\<pos\\>\n"
        "🗑️ `/clear\\_queue`\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "👥 *ADMIN*\n"
        "━━━━━━━━━━━━━━━━\n"
        "⚙️ `/init` — Setup\n"
        "ℹ️ `/info` — Group info\n"
        "👑 `/admin\\_add` \\<id\\>\n"
        "🚫 `/ban` \\<id\\>\n"
        "✅ `/unban` \\<id\\>\n"
        "🔤 `/set\\_prefix` \\<char\\>\n"
        "🔢 `/queue\\_limit` \\<num\\>\n\n"
        "━━━━━━━━━━━━━━━━\n"
        "👤 *OWNER ONLY*\n"
        "━━━━━━━━━━━━━━━━\n"
        "📢 `/broadcast` \\<msg\\>"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎵 Play Music", switch_inline_query_current_chat="/play "),
        ],
        [
            InlineKeyboardButton("📋 View Queue", callback_data="util_queue"),
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        help_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def util_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle utility button presses"""
    query = update.callback_query
    await query.answer()

    if query.data == "util_commands":
        text = (
            "🎵 *Quick Commands:*\n\n"
            "▶️ `/play` \\<song name\\>\n"
            "📋 `/queue` — View queue\n"
            "⏭️ `/skip` — Skip song\n"
            "🔀 `/shuffle` — Shuffle\n"
            "🗑️ `/clear\\_queue` — Clear\n"
            "📊 `/stats` — Statistics\n"
            "ℹ️ `/info` — Group info"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="util_back")]]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_howto":
        text = (
            "❓ *How to Use:*\n\n"
            "*Step 1:* Add bot to your group\n"
            "*Step 2:* Type `/init` to setup\n"
            "*Step 3:* Type `/play Tum Hi Aana`\n"
            "*Step 4:* Song added to queue\\!\n\n"
            "💡 *Tips:*\n"
            "• Use full song name for best results\n"
            "• Add artist name for accuracy\n"
            "• `/queue` to see all songs\n"
            "• `/shuffle` for random order\n"
            "• Admins can `/ban` spammers"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="util_back")]]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_stats":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.mongo_group_manager import MongoGroupManager
        qm = MongoQueueManager()
        gm = MongoGroupManager()
        chat_id = query.message.chat_id
        settings = await gm.get_group_settings(chat_id)
        queue_len = await qm.get_queue_length(chat_id)

        text = (
            "📊 *Statistics*\n\n"
            f"🎵 Songs Played: `{settings['stats']['total_songs_played']}`\n"
            f"➕ Songs Queued: `{settings['stats']['total_queue_added']}`\n"
            f"📻 In Queue Now: `{queue_len}`\n"
            f"👥 Admins: `{len(settings['admins'])}`\n"
            f"🚫 Banned Users: `{len(settings['banned_users'])}`"
        )
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="util_stats")],
            [InlineKeyboardButton("🔙 Back", callback_data="util_back")],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_about":
        text = (
            f"🎵 *{safe_md(BOT_NAME)}*\n\n"
            "A powerful music bot for Telegram groups\\!\n\n"
            "✅ YouTube music streaming\n"
            "✅ Smart queue management\n"
            "✅ Group admin controls\n"
            "✅ Usage statistics\n"
            "✅ Owner broadcast\n"
            "✅ MongoDB database\n\n"
            "🚀 Hosted on Railway\n"
            "💾 Powered by MongoDB"
        )
        keyboard = [
            [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)],
            [InlineKeyboardButton("🔙 Back", callback_data="util_back")],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_queue":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        queue = await qm.get_queue(chat_id)

        if not queue:
            text = "📋 *Queue is empty\\!*\n\nUse `/play song name` to add songs\\."
        else:
            text = f"📋 *Queue \\({len(queue)} songs\\):*\n\n"
            for i, song in enumerate(queue[:8], 1):
                title = safe_md(song.get("title", "Unknown")[:40])
                dur = song.get("duration", 0)
                s = int(dur)
                dur_str = f"{s // 60}:{s % 60:02d}"
                text += f"`{i}.` {title} \\| `{dur_str}`\n"
            if len(queue) > 8:
                text += f"\n_\\+{len(queue) - 8} more_"

        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="util_back")]]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_back":
        user = query.from_user
        user_mention = f"[{safe_md(user.first_name)}](tg://user?id={user.id})"
        text = (
            f"🎵 *Hey {user_mention}\\! Welcome to {safe_md(BOT_NAME)}*\n\n"
            "┌─────────────────────┐\n"
            "│  🎧 *MUSIC BOT*  │\n"
            "│  Your Music Partner  │\n"
            "└─────────────────────┘\n\n"
            "🌟 *Features:*\n"
            "╠ 🎵 Play from YouTube\n"
            "╠ 📋 Queue management\n"
            "╠ 🔀 Shuffle & skip\n"
            "╠ 👥 Group admin tools\n"
            "╠ 📊 Usage statistics\n"
            "╚ 📢 Owner broadcast\n\n"
            "👇 *Tap a button to get started\\!*"
        )
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
                InlineKeyboardButton("💬 Support Chat", url=SUPPORT_CHAT),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /ask your question")
        return
    question = " ".join(context.args)
    await update.message.chat.send_action("typing")
    response = await gpt_assistant.get_response(question)
    await update.message.reply_text(safe_md(response), parse_mode="MarkdownV2")


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
        f"📊 *Group Statistics*\n\n"
        f"🎵 Songs Played: `{settings['stats']['total_songs_played']}`\n"
        f"➕ Songs Queued: `{settings['stats']['total_queue_added']}`\n"
        f"📻 In Queue: `{queue_length}`\n"
        f"👥 Admins: `{len(settings['admins'])}`\n"
        f"🚫 Banned: `{len(settings['banned_users'])}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
            InlineKeyboardButton("📋 Commands", callback_data="util_commands"),
        ]
    ]
    await update.message.reply_text(
        f"🎵 *{safe_md(BOT_NAME)}*\n\n"
        "A powerful music bot for Telegram groups\\!\n\n"
        "✅ YouTube music streaming\n"
        "✅ Queue management\n"
        "✅ Group permissions\n"
        "✅ Statistics tracking\n"
        "✅ Owner broadcast\n\n"
        "🚀 Hosted on Railway",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    try:
        await update.message.reply_text(
            "❌ An error occurred\\. Please try again or use /help",
            parse_mode="MarkdownV2"
        )
    except Exception:
        pass
