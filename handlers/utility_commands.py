import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()

DEV_USERNAME = "@secret_fetcher"
DEV_URL = "tg://resolve?domain=secret_fetcher"


def safe_md(text: str) -> str:
    special = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for ch in special:
        text = text.replace(ch, f'\\{ch}')
    return text


def dev_button():
    return InlineKeyboardButton("👨‍💻 Developer", url=DEV_URL)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start from user_id={user.id}, chat_id={update.effective_chat.id}")
    user_mention = f"[{safe_md(user.first_name)}](tg://user?id={user.id})"

    welcome_text = (
        f"✨ *ʜᴇʏ {user_mention}* ✨\n"
        f"🎵 *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {safe_md(BOT_NAME)}* 🎵\n\n"
        "╔══════════════════╗\n"
        "║  🎧 𝗬𝗢𝗨𝗥 𝗠𝗨𝗦𝗜𝗖 𝗣𝗔𝗥𝗧𝗡𝗘𝗥  ║\n"
        "╚══════════════════╝\n\n"
        "🌟 *ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ:*\n"
        "┣ 🎵 ᴘʟᴀʏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ\n"
        "┣ 📋 ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n"
        "┣ 🔀 sʜᴜғғʟᴇ & sᴋɪᴘ\n"
        "┣ 👥 ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ ᴛᴏᴏʟs\n"
        "┣ 📊 ᴜsᴀɢᴇ sᴛᴀᴛɪsᴛɪᴄs\n"
        "┗ 📢 ʙʀᴏᴀᴅᴄᴀsᴛ sʏsᴛᴇᴍ\n\n"
        "👇 *ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ\\!*"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴍᴜsɪᴄ", switch_inline_query_current_chat="/play "),
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
        ],
        [
            InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
            InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
            InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
        ],
        [
            InlineKeyboardButton("📖 ᴄᴏᴍᴍᴀɴᴅs", callback_data="util_commands"),
            InlineKeyboardButton("❓ ʜᴏᴡ ᴛᴏ ᴜsᴇ", callback_data="util_howto"),
        ],
        [
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="util_about"),
        ],
        [
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
            dev_button(),
        ],
    ]

    await update.message.reply_text(
        welcome_text,
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 𝗟𝗜𝗦𝗧*\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎵 *ᴍᴜsɪᴄ ᴄᴏᴍᴍᴀɴᴅs*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "▶️ `/play` \\<song\\> — ᴘʟᴀʏ\n"
        "⏭️ `/skip` — sᴋɪᴘ sᴏɴɢ\n"
        "⏩ `/next` — ɴᴇxᴛ ɪɴғᴏ\n"
        "📋 `/queue` — ᴠɪᴇᴡ ǫᴜᴇᴜᴇ\n"
        "🔀 `/shuffle` — sʜᴜғғʟᴇ\n"
        "❌ `/remove` \\<pos\\> — ʀᴇᴍᴏᴠᴇ\n"
        "🗑️ `/clear\\_queue` — ᴄʟᴇᴀʀ ᴀʟʟ\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👥 *ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚙️ `/init` — sᴇᴛᴜᴘ ɢʀᴏᴜᴘ\n"
        "ℹ️ `/info` — ɢʀᴏᴜᴘ ɪɴғᴏ\n"
        "👑 `/admin\\_add` \\<id\\>\n"
        "🚫 `/ban` \\<id\\>\n"
        "✅ `/unban` \\<id\\>\n"
        "🔤 `/set\\_prefix` \\<char\\>\n"
        "🔢 `/queue\\_limit` \\<num\\>\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👤 *ᴏᴡɴᴇʀ ᴏɴʟʏ*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📢 `/broadcast` \\<msg\\>"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴍᴜsɪᴄ", switch_inline_query_current_chat="/play "),
        ],
        [
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
        ],
        [
            InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
            dev_button(),
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

    if query.data == "util_commands":
        text = (
            "📖 *𝗤𝗨𝗜𝗖𝗞 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦*\n\n"
            "🎵 `/play` \\<song name\\>\n"
            "⏭️ `/skip` — sᴋɪᴘ ᴄᴜʀʀᴇɴᴛ\n"
            "📋 `/queue` — ᴠɪᴇᴡ ǫᴜᴇᴜᴇ\n"
            "🔀 `/shuffle` — sʜᴜғғʟᴇ\n"
            "🗑️ `/clear\\_queue` — ᴄʟᴇᴀʀ\n"
            "📊 `/stats` — sᴛᴀᴛɪsᴛɪᴄs\n"
            "ℹ️ `/info` — ɢʀᴏᴜᴘ ɪɴғᴏ\n"
            "👑 `/admin\\_add` \\<id\\>\n"
            "🚫 `/ban` \\<id\\>"
        )
        keyboard = [
            [
                InlineKeyboardButton("▶️ ᴘʟᴀʏ", switch_inline_query_current_chat="/play "),
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            ],
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
                dev_button(),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_howto":
        text = (
            "❓ *𝗛𝗢𝗪 𝗧𝗢 𝗨𝗦𝗘*\n\n"
            "𝗦𝘁𝗲𝗽 𝟭 ➤ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ\n"
            "𝗦𝘁𝗲𝗽 𝟮 ➤ ᴛʏᴘᴇ `/init` ᴛᴏ sᴇᴛᴜᴘ\n"
            "𝗦𝘁𝗲𝗽 𝟯 ➤ ᴛʏᴘᴇ `/play Tum Hi Aana`\n"
            "𝗦𝘁𝗲𝗽 𝟰 ➤ sᴏɴɢ ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ✅\n\n"
            "💡 *ᴛɪᴘs:*\n"
            "┣ ᴜsᴇ ғᴜʟʟ sᴏɴɢ ɴᴀᴍᴇ\n"
            "┣ ᴀᴅᴅ ᴀʀᴛɪsᴛ ɴᴀᴍᴇ ғᴏʀ ʙᴇsᴛ ʀᴇsᴜʟᴛ\n"
            "┣ `/queue` ᴛᴏ sᴇᴇ ᴀʟʟ sᴏɴɢs\n"
            "┣ `/shuffle` ғᴏʀ ʀᴀɴᴅᴏᴍ ᴏʀᴅᴇʀ\n"
            "┗ ᴀᴅᴍɪɴs ᴄᴀɴ `/ban` sᴘᴀᴍᴍᴇʀs"
        )
        keyboard = [
            [
                InlineKeyboardButton("🎵 ᴛʀʏ ᴘʟᴀʏɪɴɢ", switch_inline_query_current_chat="/play "),
            ],
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
                dev_button(),
            ],
        ]
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
            "📊 *𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦*\n\n"
            f"🎵 sᴏɴɢs ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
            f"➕ sᴏɴɢs ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
            f"📻 ɪɴ ǫᴜᴇᴜᴇ ɴᴏᴡ ➤ `{queue_len}`\n"
            f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
            f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`"
        )
        keyboard = [
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"),
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            ],
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
                dev_button(),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_about":
        text = (
            "ℹ️ *𝗔𝗕𝗢𝗨𝗧*\n\n"
            "𝙄 𝙖𝙢 𝙖 𝙈𝙪𝙨𝙞𝙘 𝘽𝙤𝙩\n"
            "𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙙 𝙗𝙮 [secret\\_fetcher](tg://resolve?domain=secret_fetcher)"
        )
        keyboard = [
            [
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
                dev_button(),
            ],
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_queue":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        queue = await qm.get_queue(chat_id)

        if not queue:
            text = "📋 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*\n\nᴜsᴇ `/play song name` ᴛᴏ ᴀᴅᴅ sᴏɴɢs\\."
        else:
            text = f"📋 *𝗤𝗨𝗘𝗨𝗘 — {len(queue)} sᴏɴɢ{'s' if len(queue) > 1 else ''}*\n\n"
            for i, song in enumerate(queue[:8], 1):
                title = safe_md(song.get("title", "Unknown")[:38])
                dur = song.get("duration", 0)
                s = int(dur)
                dur_str = f"{s // 60}:{s % 60:02d}"
                text += f"`{i}.` {title} ┃ `{dur_str}`\n"
            if len(queue) > 8:
                text += f"\n_\\+{len(queue) - 8} ᴍᴏʀᴇ_"

        keyboard = [
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
                InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_queue"),
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
            ],
            [dev_button()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_skip":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        next_song = await qm.get_next_song(chat_id)
        if next_song:
            title = safe_md(next_song.get("title", "Unknown")[:55])
            dur = next_song.get("duration", 0)
            s = int(dur)
            dur_str = f"{s // 60}:{s % 60:02d}"
            text = f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!*\n\n🎵 *{title}*\n⏱ `{dur_str}`"
        else:
            text = "🎵 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*"
        keyboard = [
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="util_skip"),
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            ],
            [
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
                dev_button(),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "util_shuffle":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        if await qm.shuffle_queue(chat_id):
            await query.answer("🔀 Queue shuffled!", show_alert=False)
        else:
            await query.answer("❌ Not enough songs!", show_alert=True)

    elif query.data == "util_clear":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        count = await qm.clear_queue(chat_id)
        keyboard = [
            [
                InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play "),
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
            ],
            [dev_button()],
        ]
        await query.edit_message_text(
            f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs ғʀᴏᴍ ǫᴜᴇᴜᴇ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "util_back":
        user = query.from_user
        user_mention = f"[{safe_md(user.first_name)}](tg://user?id={user.id})"
        text = (
            f"✨ *ʜᴇʏ {user_mention}* ✨\n"
            f"🎵 *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {safe_md(BOT_NAME)}* 🎵\n\n"
            "╔══════════════════╗\n"
            "║  🎧 𝗬𝗢𝗨𝗥 𝗠𝗨𝗦𝗜𝗖 𝗣𝗔𝗥𝗧𝗡𝗘𝗥  ║\n"
            "╚══════════════════╝\n\n"
            "🌟 *ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ:*\n"
            "┣ 🎵 ᴘʟᴀʏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ\n"
            "┣ 📋 ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n"
            "┣ 🔀 sʜᴜғғʟᴇ & sᴋɪᴘ\n"
            "┣ 👥 ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ ᴛᴏᴏʟs\n"
            "┣ 📊 ᴜsᴀɢᴇ sᴛᴀᴛɪsᴛɪᴄs\n"
            "┗ 📢 ʙʀᴏᴀᴅᴄᴀsᴛ sʏsᴛᴇᴍ\n\n"
            "👇 *ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ\\!*"
        )
        keyboard = [
            [
                InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴍᴜsɪᴄ", switch_inline_query_current_chat="/play "),
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            ],
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
                InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
            ],
            [
                InlineKeyboardButton("📖 ᴄᴏᴍᴍᴀɴᴅs", callback_data="util_commands"),
                InlineKeyboardButton("❓ ʜᴏᴡ ᴛᴏ ᴜsᴇ", callback_data="util_howto"),
            ],
            [
                InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
                InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="util_about"),
            ],
            [
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
                dev_button(),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /ask your question")
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

    keyboard = [
        [
            InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"),
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
        ],
        [dev_button()],
    ]
    await update.message.reply_text(
        f"📊 *𝗚𝗥𝗢𝗨𝗣 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦*\n\n"
        f"🎵 sᴏɴɢs ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
        f"➕ sᴏɴɢs ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
        f"📻 ɪɴ ǫᴜᴇᴜᴇ ➤ `{queue_length}`\n"
        f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
        f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
            dev_button(),
        ]
    ]
    await update.message.reply_text(
        "ℹ️ *𝗔𝗕𝗢𝗨𝗧*\n\n"
        "𝙄 𝙖𝙢 𝙖 𝙈𝙪𝙨𝙞𝙘 𝘽𝙤𝙩\n"
        "𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙙 𝙗𝙮 [secret\\_fetcher](tg://resolve?domain=secret_fetcher)",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    try:
        await update.message.reply_text(
            "❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ\\. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴜsᴇ /help",
            parse_mode="MarkdownV2"
        )
    except Exception:
        pass
