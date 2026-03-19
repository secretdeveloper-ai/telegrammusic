import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()

DEV_URL = "tg://resolve?domain=secret_fetcher"

# Auto reactions
WELCOME_REACTIONS = ["👋", "🎵", "✨", "🔥", "💫"]


def dev_btn():
    return InlineKeyboardButton("👨‍💻 ᴅᴇᴠ", url=DEV_URL)


def esc(text: str) -> str:
    for c in ['_','*','[',']','(',')','>','#','+','-','=','|','{','}','.','!','~','`']:
        text = text.replace(c, f'\\{c}')
    return text


async def auto_react(update: Update, emoji: str):
    try:
        await update.message.set_reaction(emoji)
    except Exception:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start from user_id={user.id}, chat_id={update.effective_chat.id}")

    asyncio.create_task(auto_react(update, random.choice(WELCOME_REACTIONS)))

    user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"

    text = (
        f"✨ *ʜᴇʏ {user_mention}* ✨\n"
        f"🎵 *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {esc(BOT_NAME)}* 🎵\n\n"
        "╔══════════════════╗\n"
        "║  🎧 𝗬𝗢𝗨𝗥 𝗠𝗨𝗦𝗜𝗖 𝗣𝗔𝗥𝗧𝗡𝗘𝗥  ║\n"
        "╚══════════════════╝\n\n"
        "🌟 *ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ:*\n"
        "┣ 🎵 ᴘʟᴀʏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ\n"
        "┣ 🔊 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛʀᴇᴀᴍɪɴɢ\n"
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
            dev_btn(),
        ],
    ]

    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 *𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦*\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "🎵 *ᴍᴜsɪᴄ*\n"
        "━━━━━━━━━━━━━━━━━\n"
        "▶️ `/play` \\<song\\>\n"
        "⏭️ `/skip` — sᴋɪᴘ\n"
        "⏩ `/next` — ɴᴇxᴛ ɪɴғᴏ\n"
        "📋 `/queue` — ᴠɪᴇᴡ\n"
        "🔀 `/shuffle` — sʜᴜғғʟᴇ\n"
        "❌ `/remove` \\<pos\\>\n"
        "🗑️ `/clear\\_queue`\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "👥 *ᴀᴅᴍɪɴ*\n"
        "━━━━━━━━━━━━━━━━━\n"
        "⚙️ `/init` `/info`\n"
        "👑 `/admin\\_add` \\<id\\>\n"
        "🚫 `/ban` `/unban` \\<id\\>\n"
        "🔤 `/set\\_prefix` \\<char\\>\n"
        "🔢 `/queue\\_limit` \\<num\\>\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "👤 *ᴏᴡɴᴇʀ*\n"
        "━━━━━━━━━━━━━━━━━\n"
        "📢 `/broadcast` \\<msg\\>"
    )

    keyboard = [
        [InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴍᴜsɪᴄ", switch_inline_query_current_chat="/play ")],
        [
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
        ],
        [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
    ]

    await update.message.reply_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def util_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "util_commands":
        text = (
            "📖 *ǫᴜɪᴄᴋ ᴄᴏᴍᴍᴀɴᴅs*\n\n"
            "🎵 `/play` \\<song name\\>\n"
            "⏭️ `/skip` — sᴋɪᴘ sᴏɴɢ\n"
            "📋 `/queue` — ᴠɪᴇᴡ ǫᴜᴇᴜᴇ\n"
            "🔀 `/shuffle` — sʜᴜғғʟᴇ\n"
            "🗑️ `/clear\\_queue` — ᴄʟᴇᴀʀ\n"
            "📊 `/stats` — sᴛᴀᴛɪsᴛɪᴄs\n"
            "ℹ️ `/info` — ɢʀᴏᴜᴘ ɪɴғᴏ\n"
            "👑 `/admin\\_add` \\<id\\>\n"
            "🚫 `/ban` \\<id\\>"
        )
        kb = [
            [InlineKeyboardButton("▶️ ᴘʟᴀʏ", switch_inline_query_current_chat="/play "), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_howto":
        text = (
            "❓ *ʜᴏᴡ ᴛᴏ ᴜsᴇ*\n\n"
            "𝗦𝘁𝗲𝗽 𝟭 ➤ ᴀᴅᴅ ʙᴏᴛ ᴛᴏ ɢʀᴏᴜᴘ\n"
            "𝗦𝘁𝗲𝗽 𝟮 ➤ sᴛᴀʀᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\n"
            "𝗦𝘁𝗲𝗽 𝟯 ➤ `/play Tum Hi Aana`\n"
            "𝗦𝘁𝗲𝗽 𝟰 ➤ ʙᴏᴛ ᴊᴏɪɴs & ᴘʟᴀʏs ✅\n\n"
            "💡 *ᴛɪᴘs:*\n"
            "┣ ᴜsᴇ ғᴜʟʟ sᴏɴɢ ɴᴀᴍᴇ\n"
            "┣ ᴀᴅᴅ ᴀʀᴛɪsᴛ ɴᴀᴍᴇ\n"
            "┣ ᴀssɪsᴛᴀɴᴛ ᴍᴜsᴛ ʙᴇ ɪɴ ɢʀᴏᴜᴘ\n"
            "┗ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴍᴜsᴛ ʙᴇ ᴀᴄᴛɪᴠᴇ"
        )
        kb = [
            [InlineKeyboardButton("🎵 ᴛʀʏ ᴘʟᴀʏɪɴɢ", switch_inline_query_current_chat="/play ")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_stats":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.mongo_group_manager import MongoGroupManager
        from utils.voice_chat import get_now_playing
        qm = MongoQueueManager()
        gm = MongoGroupManager()
        chat_id = query.message.chat_id
        settings = await gm.get_group_settings(chat_id)
        queue_len = await qm.get_queue_length(chat_id)
        now = get_now_playing(chat_id)

        now_text = f"\n🔊 *ɴᴏᴡ:* {esc(now.get('title','')[:35])}" if now else ""
        text = (
            f"📊 *sᴛᴀᴛɪsᴛɪᴄs*{now_text}\n\n"
            f"🎵 ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
            f"➕ ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
            f"📻 ɪɴ ǫᴜᴇᴜᴇ ➤ `{queue_len}`\n"
            f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
            f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`"
        )
        kb = [
            [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_about":
        text = (
            "ℹ️ *ᴀʙᴏᴜᴛ*\n\n"
            "𝙄 𝙖𝙢 𝙖 𝙈𝙪𝙨𝙞𝙘 𝘽𝙤𝙩\n"
            "𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙙 𝙗𝙮 [secret\\_fetcher](tg://resolve?domain=secret_fetcher)"
        )
        kb = [
            [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT), dev_btn()],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back")],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_queue":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import get_now_playing
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        queue = await qm.get_queue(chat_id)
        now = get_now_playing(chat_id)

        if not queue and not now:
            text = "📭 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*\n\nᴜsᴇ `/play song name`"
        else:
            text = ""
            if now:
                text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 {esc(now.get('title','')[:40])}\n\n"
            if queue:
                text += f"📋 *ǫᴜᴇᴜᴇ \\({len(queue)}\\):*\n\n"
                for i, s in enumerate(queue[:8], 1):
                    d = int(s.get("duration", 0))
                    text += f"`{i}.` {esc(s.get('title','')[:35])} ┃ `{d//60}:{d%60:02d}`\n"
                if len(queue) > 8:
                    text += f"\n_\\+{len(queue)-8} ᴍᴏʀᴇ_"

        kb = [
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
                InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_queue"),
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"),
                dev_btn(),
            ],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_skip":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import voice_play, is_voice_available
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        next_song = await qm.get_next_song(chat_id)
        if next_song:
            title = next_song.get("title", "Unknown")
            d = int(next_song.get("duration", 0))
            vc_text = ""
            if is_voice_available():
                vc = await voice_play(chat_id, title, next_song)
                vc_text = " 🔊" if vc["success"] else ""
            text = f"⏭️ *sᴋɪᴘᴘᴇᴅ\\!*{vc_text}\n\n🎵 *{esc(title[:55])}*\n⏱ `{d//60}:{d%60:02d}`"
        else:
            text = "📭 *ǫᴜᴇᴜᴇ ᴇᴍᴘᴛʏ\\!*"
        kb = [
            [InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="util_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "util_shuffle":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        if await qm.shuffle_queue(query.message.chat_id):
            await query.answer("🔀 Queue shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    elif query.data == "util_clear":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import voice_leave
        qm = MongoQueueManager()
        chat_id = query.message.chat_id
        count = await qm.clear_queue(chat_id)
        await voice_leave(chat_id)
        kb = [
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play ")],
            [InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back"), dev_btn()],
        ]
        await query.edit_message_text(
            f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif query.data == "util_back":
        user = query.from_user
        user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"
        text = (
            f"✨ *ʜᴇʏ {user_mention}* ✨\n"
            f"🎵 *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {esc(BOT_NAME)}* 🎵\n\n"
            "╔══════════════════╗\n"
            "║  🎧 𝗬𝗢𝗨𝗥 𝗠𝗨𝗦𝗜𝗖 𝗣𝗔𝗥𝗧𝗡𝗘𝗥  ║\n"
            "╚══════════════════╝\n\n"
            "🌟 *ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ:*\n"
            "┣ 🎵 ᴘʟᴀʏ ғʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ\n"
            "┣ 🔊 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛʀᴇᴀᴍɪɴɢ\n"
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
            [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT), dev_btn()],
        ]
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: /ask your question")
        return
    await update.message.chat.send_action("typing")
    response = await gpt_assistant.get_response(" ".join(context.args))
    await update.message.reply_text(response)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from utils.mongo_queue_manager import MongoQueueManager
    from utils.mongo_group_manager import MongoGroupManager
    from utils.voice_chat import get_now_playing
    qm = MongoQueueManager()
    gm = MongoGroupManager()
    group_id = update.effective_chat.id
    settings = await gm.get_group_settings(group_id)
    queue_length = await qm.get_queue_length(group_id)
    now = get_now_playing(group_id)

    now_text = f"\n🔊 *ɴᴏᴡ:* {esc(now.get('title','')[:35])}" if now else ""
    keyboard = [[InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"), dev_btn()]]
    await update.message.reply_text(
        f"📊 *sᴛᴀᴛɪsᴛɪᴄs*{now_text}\n\n"
        f"🎵 ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
        f"➕ ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
        f"📻 ɪɴ ǫᴜᴇᴜᴇ ➤ `{queue_length}`\n"
        f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
        f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT), dev_btn()]
    ]
    await update.message.reply_text(
        "ℹ️ *ᴀʙᴏᴜᴛ*\n\n"
        "𝙄 𝙖𝙢 𝙖 𝙈𝙪𝙨𝙞𝙘 𝘽𝙤𝙩\n"
        "𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙙 𝙗𝙮 [secret\\_fetcher](tg://resolve?domain=secret_fetcher)",
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    try:
        await update.message.reply_text(
            "❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ\\. ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴜsᴇ /help",
            parse_mode="MarkdownV2"
        )
    except Exception:
        pass
