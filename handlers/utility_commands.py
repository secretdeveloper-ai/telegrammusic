import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME, OWNER_ID

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()

DEVELOPER = "@secret_fetcher"


def esc(text: str) -> str:
    """Escape MarkdownV2 special chars"""
    for ch in r'\_*[]()~`>#+-=|{}.!':
        text = text.replace(ch, f'\\{ch}')
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    logger.info(f"/start from user_id={user.id}, chat_id={chat.id}")

    user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"
    chat_type = "Private" if chat.type == "private" else f"Group: {esc(chat.title or 'Unknown')}"

    # Notify owner
    try:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=(
                f"🔔 *New User Started Bot\\!*\n\n"
                f"👤 User: [{esc(user.first_name)}](tg://user?id={user.id})\n"
                f"🆔 User ID: `{user.id}`\n"
                f"📱 Username: @{esc(user.username or 'none')}\n"
                f"💬 Chat: {chat_type}\n"
                f"🆔 Chat ID: `{chat.id}`"
            ),
            parse_mode="MarkdownV2"
        )
    except Exception as e:
        logger.warning(f"Could not notify owner: {e}")

    welcome_text = (
        f"🎵 *Hey {user_mention}\\!*\n\n"
        f"╔══════════════════╗\n"
        f"║  🎧  *{esc(BOT_NAME)}*  🎧  ║\n"
        f"╚══════════════════╝\n\n"
        f"✨ *Your Premium Music Experience*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎵  Stream from YouTube\n"
        f"📋  Smart queue system\n"
        f"🔀  Shuffle & skip anytime\n"
        f"👥  Group admin controls\n"
        f"📊  Live statistics\n"
        f"📢  Owner broadcasts\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👨‍💻 *Dev:* {DEVELOPER}\n\n"
        f"👇 *Choose an option below*"
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
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        f"📖 *{esc(BOT_NAME)} — Commands*\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎵 *MUSIC*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"▶️ `/play` \\<song\\>\n"
        f"⏭️ `/skip` — Skip song\n"
        f"⏩ `/next` — Next info\n"
        f"📋 `/queue` — View queue\n"
        f"🔀 `/shuffle` — Shuffle\n"
        f"❌ `/remove` \\<pos\\>\n"
        f"🗑️ `/clear\\_queue`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 *ADMIN*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ `/init` — Setup group\n"
        f"ℹ️ `/info` — Group info\n"
        f"👑 `/admin\\_add` \\<id\\>\n"
        f"🚫 `/ban` \\<id\\>\n"
        f"✅ `/unban` \\<id\\>\n"
        f"🔤 `/set\\_prefix` \\<char\\>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *OWNER ONLY*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📢 `/broadcast` \\<msg\\>\n\n"
        f"👨‍💻 *Dev:* {DEVELOPER}"
    )

    keyboard = [
        [InlineKeyboardButton("🎵 Play Music", switch_inline_query_current_chat="/play ")],
        [
            InlineKeyboardButton("📋 Queue", callback_data="util_queue"),
            InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
        ],
    ]

    await update.message.reply_text(
        help_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def util_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    def back_btn():
        return [[InlineKeyboardButton("🔙 Back", callback_data="util_back")]]

    if query.data == "util_commands":
        text = (
            f"🎵 *Quick Commands:*\n\n"
            f"▶️ `/play` \\<song name\\>\n"
            f"📋 `/queue` — View queue\n"
            f"⏭️ `/skip` — Skip song\n"
            f"🔀 `/shuffle` — Shuffle\n"
            f"🗑️ `/clear\\_queue` — Clear all\n"
            f"📊 `/stats` — Statistics\n"
            f"ℹ️ `/info` — Group info\n\n"
            f"👨‍💻 *Dev:* {DEVELOPER}"
        )
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif query.data == "util_howto":
        text = (
            f"❓ *How to Use:*\n\n"
            f"*Step 1️⃣* — Add bot to your group\n"
            f"*Step 2️⃣* — Type `/init` to setup\n"
            f"*Step 3️⃣* — Type `/play Tum Hi Aana`\n"
            f"*Step 4️⃣* — Song added to queue\\!\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Pro Tips:*\n"
            f"• Use full song name for best results\n"
            f"• Add artist name for accuracy\n"
            f"• `/queue` to see all songs\n"
            f"• `/shuffle` for random play\n"
            f"• Admins can `/ban` spammers\n\n"
            f"👨‍💻 *Dev:* {DEVELOPER}"
        )
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif query.data == "util_stats":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.mongo_group_manager import MongoGroupManager
        qm = MongoQueueManager()
        gm = MongoGroupManager()
        chat_id = query.message.chat_id
        settings = await gm.get_group_settings(chat_id)
        queue_len = await qm.get_queue_length(chat_id)

        text = (
            f"📊 *Statistics*\n\n"
            f"🎵 Songs Played: `{settings['stats']['total_songs_played']}`\n"
            f"➕ Songs Queued: `{settings['stats']['total_queue_added']}`\n"
            f"📻 In Queue Now: `{queue_len}`\n"
            f"👥 Admins: `{len(settings['admins'])}`\n"
            f"🚫 Banned Users: `{len(settings['banned_users'])}`\n\n"
            f"👨‍💻 *Dev:* {DEVELOPER}"
        )
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="util_stats")],
            [InlineKeyboardButton("🔙 Back", callback_data="util_back")],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_about":
        text = (
            f"╔══════════════════╗\n"
            f"║  🎧  *{esc(BOT_NAME)}*  🎧  ║\n"
            f"╚══════════════════╝\n\n"
            f"🌟 *Premium Music Bot*\n\n"
            f"✅ YouTube streaming\n"
            f"✅ Smart queue system\n"
            f"✅ Group admin controls\n"
            f"✅ Live statistics\n"
            f"✅ Owner broadcasts\n"
            f"✅ MongoDB database\n"
            f"✅ 24/7 on Railway\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👨‍💻 *Developer:* {DEVELOPER}\n"
            f"🚀 *Hosted:* Railway\n"
            f"💾 *Database:* MongoDB"
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
            text = f"📋 *Queue is empty\\!*\n\nUse `/play song name` to add songs\\.\n\n👨‍💻 *Dev:* {DEVELOPER}"
        else:
            text = f"📋 *Queue — {len(queue)} song{'s' if len(queue) > 1 else ''}*\n\n"
            for i, song in enumerate(queue[:8], 1):
                title = esc(song.get("title", "Unknown")[:38])
                dur = song.get("duration", 0)
                s = int(dur)
                dur_str = f"{s // 60}:{s % 60:02d}"
                text += f"`{i}\\.` {title} — `{dur_str}`\n"
            if len(queue) > 8:
                text += f"\n_\\+{len(queue) - 8} more songs_"

        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(back_btn()))

    elif query.data == "util_back":
        user = query.from_user
        user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"
        text = (
            f"🎵 *Hey {user_mention}\\!*\n\n"
            f"╔══════════════════╗\n"
            f"║  🎧  *{esc(BOT_NAME)}*  🎧  ║\n"
            f"╚══════════════════╝\n\n"
            f"✨ *Your Premium Music Experience*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎵  Stream from YouTube\n"
            f"📋  Smart queue system\n"
            f"🔀  Shuffle & skip anytime\n"
            f"👥  Group admin controls\n"
            f"📊  Live statistics\n"
            f"📢  Owner broadcasts\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👨‍💻 *Dev:* {DEVELOPER}\n\n"
            f"👇 *Choose an option below*"
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
                InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
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
    await update.message.reply_text(esc(response), parse_mode="MarkdownV2")


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
        f"📊 *Statistics*\n\n"
        f"🎵 Songs Played: `{settings['stats']['total_songs_played']}`\n"
        f"➕ Songs Queued: `{settings['stats']['total_queue_added']}`\n"
        f"📻 In Queue: `{queue_length}`\n"
        f"👥 Admins: `{len(settings['admins'])}`\n"
        f"🚫 Banned: `{len(settings['banned_users'])}`\n\n"
        f"👨‍💻 *Dev:* {DEVELOPER}",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
         InlineKeyboardButton("📋 Commands", callback_data="util_commands")],
    ]
    await update.message.reply_text(
        f"╔══════════════════╗\n"
        f"║  🎧  *{esc(BOT_NAME)}*  🎧  ║\n"
        f"╚══════════════════╝\n\n"
        f"✅ YouTube streaming\n"
        f"✅ Queue management\n"
        f"✅ Group controls\n"
        f"✅ 24/7 on Railway\n\n"
        f"👨‍💻 *Dev:* {DEVELOPER}",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")
    try:
        await update.message.reply_text(
            "❌ Something went wrong\\. Please try again\\.",
            parse_mode="MarkdownV2"
        )
    except Exception:
        pass
