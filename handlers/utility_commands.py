import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()

DEV_URL = "tg://resolve?domain=secret_fetcher"

WELCOME_REACTIONS = ["👋", "🎵", "✨", "🔥", "💫", "🎶", "🎸", "🎤"]
MUSIC_REACTIONS = ["🎵", "🎶", "🔥", "✨", "💫", "🎸", "🎤", "🎧", "💥", "❤️"]


def dev_btn():
    return InlineKeyboardButton("👨‍💻 ᴅᴇᴠ", url=DEV_URL)


def home_btn():
    return InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="util_back")


def esc(text: str) -> str:
    for c in ['_','*','[',']','(',')','>','#','+','-','=','|','{','}','.','!','~','`']:
        text = text.replace(c, f'\\{c}')
    return text


async def auto_react(update: Update, emoji: str):
    try:
        await update.message.set_reaction(emoji)
    except Exception:
        pass


def _home_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 ᴘʟᴀʏ", switch_inline_query_current_chat="/play "),
            InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
        ],
        [
            InlineKeyboardButton("🎮 ᴄᴏɴᴛʀᴏʟs", callback_data="util_controls"),
            InlineKeyboardButton("📖 ʜᴇʟᴘ", callback_data="util_help_menu"),
        ],
        [
            InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
            InlineKeyboardButton("⚙️ sᴇᴛᴛɪɴɢs", callback_data="util_settings"),
        ],
        [
            InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
            dev_btn(),
        ],
    ])


def _home_text(user_mention):
    return (
        f"✨ *ʜᴇʏ {user_mention}* ✨\n"
        f"🎵 *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {esc(BOT_NAME)}* 🎵\n\n"
        "┌─────────────────────┐\n"
        "│  🎧 *ʏᴏᴜʀ ᴍᴜsɪᴄ ᴘᴀʀᴛɴᴇʀ*  │\n"
        "└─────────────────────┘\n\n"
        "🌟 *ᴡʜᴀᴛ ɪ ᴄᴀɴ ᴅᴏ:*\n"
        "┣ 🎵 ʏᴏᴜᴛᴜʙᴇ ᴍᴜsɪᴄ\n"
        "┣ 🔊 ᴠᴏɪᴄᴇ ᴄʜᴀᴛ sᴛʀᴇᴀᴍɪɴɢ\n"
        "┣ 📋 sᴍᴀʀᴛ ǫᴜᴇᴜᴇ\n"
        "┣ 🔀 sʜᴜғғʟᴇ & sᴋɪᴘ\n"
        "┣ 👥 ɢʀᴏᴜᴘ ᴀᴅᴍɪɴ\n"
        "┗ 📊 sᴛᴀᴛɪsᴛɪᴄs\n\n"
        "👇 *sᴇʟᴇᴄᴛ ᴀɴ ᴏᴘᴛɪᴏɴ:*"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"/start from user_id={user.id}, chat_id={update.effective_chat.id}")
    asyncio.create_task(auto_react(update, random.choice(WELCOME_REACTIONS)))
    user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"
    await update.message.reply_text(
        _home_text(user_mention),
        parse_mode="MarkdownV2",
        reply_markup=_home_keyboard()
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    asyncio.create_task(auto_react(update, "📖"))
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 ᴍᴜsɪᴄ ᴄᴍᴅs", callback_data="util_help_music"),
            InlineKeyboardButton("👥 ɢʀᴏᴜᴘ ᴄᴍᴅs", callback_data="util_help_group"),
        ],
        [
            InlineKeyboardButton("👑 ᴀᴅᴍɪɴ ᴄᴍᴅs", callback_data="util_help_admin"),
            InlineKeyboardButton("❓ ʜᴏᴡ ᴛᴏ ᴜsᴇ", callback_data="util_howto"),
        ],
        [home_btn(), dev_btn()],
    ])
    await update.message.reply_text(
        "📖 *ʜᴇʟᴘ ᴍᴇɴᴜ*\n\n"
        "sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ ʙᴇʟᴏᴡ ⬇️",
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )


async def util_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user = query.from_user
    user_mention = f"[{esc(user.first_name)}](tg://user?id={user.id})"

    # ═══ HOME ═══
    if query.data == "util_back":
        await query.edit_message_text(
            _home_text(user_mention),
            parse_mode="MarkdownV2",
            reply_markup=_home_keyboard()
        )

    # ═══ CONTROLS ═══
    elif query.data == "util_controls":
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸ ᴘᴀᴜsᴇ", callback_data="util_pause"),
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
                InlineKeyboardButton("▶️ ʀᴇsᴜᴍᴇ", callback_data="util_resume"),
            ],
            [
                InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
                InlineKeyboardButton("🔇 ʟᴇᴀᴠᴇ", callback_data="util_leave"),
            ],
            [
                InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue"),
                InlineKeyboardButton("➕ ᴀᴅᴅ sᴏɴɢ", switch_inline_query_current_chat="/play "),
            ],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(
            "🎮 *ᴘʟᴀʏᴇʀ ᴄᴏɴᴛʀᴏʟs*\n\n"
            "ᴜsᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴍᴜsɪᴄ 🎵",
            parse_mode="MarkdownV2",
            reply_markup=kb
        )

    # ═══ HELP MENU ═══
    elif query.data == "util_help_menu":
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 ᴍᴜsɪᴄ", callback_data="util_help_music"),
                InlineKeyboardButton("👥 ɢʀᴏᴜᴘ", callback_data="util_help_group"),
            ],
            [
                InlineKeyboardButton("👑 ᴀᴅᴍɪɴ", callback_data="util_help_admin"),
                InlineKeyboardButton("❓ ʜᴏᴡ ᴛᴏ", callback_data="util_howto"),
            ],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(
            "📖 *ʜᴇʟᴘ ᴍᴇɴᴜ*\n\nsᴇʟᴇᴄᴛ ᴄᴀᴛᴇɢᴏʀʏ ⬇️",
            parse_mode="MarkdownV2",
            reply_markup=kb
        )

    # ═══ HELP MUSIC ═══
    elif query.data == "util_help_music":
        text = (
            "🎵 *ᴍᴜsɪᴄ ᴄᴏᴍᴍᴀɴᴅs*\n\n"
            "▶️ `/play` \\<song\\> — ᴘʟᴀʏ sᴏɴɢ\n"
            "⏭️ `/skip` — sᴋɪᴘ ᴄᴜʀʀᴇɴᴛ\n"
            "⏩ `/next` — ɴᴇxᴛ sᴏɴɢ ɪɴғᴏ\n"
            "📋 `/queue` — ᴠɪᴇᴡ ǫᴜᴇᴜᴇ\n"
            "🔀 `/shuffle` — sʜᴜғғʟᴇ\n"
            "❌ `/remove` \\<pos\\> — ʀᴇᴍᴏᴠᴇ\n"
            "🗑️ `/clear\\_queue` — ᴄʟᴇᴀʀ ᴀʟʟ\n"
            "📊 `/stats` — sᴛᴀᴛɪsᴛɪᴄs"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴏᴡ", switch_inline_query_current_chat="/play ")],
            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="util_help_menu"), home_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ HELP GROUP ═══
    elif query.data == "util_help_group":
        text = (
            "👥 *ɢʀᴏᴜᴘ ᴄᴏᴍᴍᴀɴᴅs*\n\n"
            "⚙️ `/init` — sᴇᴛᴜᴘ ɢʀᴏᴜᴘ\n"
            "ℹ️ `/info` — ɢʀᴏᴜᴘ ɪɴғᴏ\n"
            "🔤 `/set\\_prefix` \\<char\\> — ᴘʀᴇғɪx\n"
            "🔢 `/queue\\_limit` \\<num\\> — ʟɪᴍɪᴛ\n"
            "📢 `/broadcast` \\<msg\\> — ʙʀᴏᴀᴅᴄᴀsᴛ"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="util_help_menu"), home_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ HELP ADMIN ═══
    elif query.data == "util_help_admin":
        text = (
            "👑 *ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs*\n\n"
            "👑 `/admin\\_add` \\<id\\> — ᴀᴅᴅ\n"
            "🔻 `/admin\\_remove` \\<id\\> — ʀᴇᴍᴏᴠᴇ\n"
            "🚫 `/ban` \\<id\\> — ʙᴀɴ ᴜsᴇʀ\n"
            "✅ `/unban` \\<id\\> — ᴜɴʙᴀɴ\n\n"
            "⚠️ _ᴀᴅᴍɪɴ ᴏɴʟʏ_"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="util_help_menu"), home_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ HOW TO ═══
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
            "┣ ᴀssɪsᴛᴀɴᴛ ɪɴ ɢʀᴏᴜᴘ\n"
            "┗ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀᴄᴛɪᴠᴇ"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 ᴛʀʏ ɴᴏᴡ", switch_inline_query_current_chat="/play ")],
            [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="util_help_menu"), home_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ SETTINGS ═══
    elif query.data == "util_settings":
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📊 sᴛᴀᴛs", callback_data="util_stats"),
                InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="util_about"),
            ],
            [
                InlineKeyboardButton("❓ ʜᴏᴡ ᴛᴏ", callback_data="util_howto"),
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT),
            ],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(
            "⚙️ *sᴇᴛᴛɪɴɢs & ɪɴғᴏ*",
            parse_mode="MarkdownV2",
            reply_markup=kb
        )

    # ═══ STATS ═══
    elif query.data == "util_stats":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.mongo_group_manager import MongoGroupManager
        from utils.voice_chat import get_now_playing
        qm = MongoQueueManager()
        gm = MongoGroupManager()
        settings = await gm.get_group_settings(chat_id)
        queue_len = await qm.get_queue_length(chat_id)
        now = get_now_playing(chat_id)
        now_text = f"\n🔊 *ɴᴏᴡ:* _{esc(now.get('title','')[:35])}_" if now else ""
        text = (
            f"📊 *sᴛᴀᴛɪsᴛɪᴄs*{now_text}\n\n"
            f"🎵 ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
            f"➕ ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
            f"📻 ɪɴ ǫᴜᴇᴜᴇ ➤ `{queue_len}`\n"
            f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
            f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ ABOUT ═══
    elif query.data == "util_about":
        text = (
            "ℹ️ *ᴀʙᴏᴜᴛ ʙᴏᴛ*\n\n"
            "🎵 *ᴍᴜsɪᴄ ʙᴏᴛ* — ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ᴍᴜsɪᴄ ᴘᴀʀᴛɴᴇʀ\n\n"
            "⚡ *ғᴇᴀᴛᴜʀᴇs:*\n"
            "┣ ʏᴏᴜᴛᴜʙᴇ sᴛʀᴇᴀᴍɪɴɢ\n"
            "┣ sᴍᴀʀᴛ ǫᴜᴇᴜᴇ\n"
            "┣ ᴀᴜᴛᴏ ʀᴇᴀᴄᴛɪᴏɴs\n"
            "┗ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n\n"
            "👨‍💻 *ᴅᴇᴠ:* [secret\\_fetcher](tg://resolve?domain=secret_fetcher)"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT), dev_btn()],
            [home_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ QUEUE ═══
    elif query.data == "util_queue":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import get_now_playing
        qm = MongoQueueManager()
        queue = await qm.get_queue(chat_id)
        now = get_now_playing(chat_id)
        if not queue and not now:
            text = "📭 *ǫᴜᴇᴜᴇ ɪs ᴇᴍᴘᴛʏ\\!*\n\n`/play song name` ᴛᴏ ᴀᴅᴅ"
        else:
            text = ""
            if now:
                text += f"🔊 *ɴᴏᴡ ᴘʟᴀʏɪɴɢ:*\n🎵 _{esc(now.get('title','')[:45])}_\n\n"
            if queue:
                text += f"📋 *ǫᴜᴇᴜᴇ — {len(queue)} sᴏɴɢs*\n\n"
                for i, s in enumerate(queue[:8], 1):
                    d = int(s.get("duration", 0))
                    text += f"`{i}.` _{esc(s.get('title','')[:35])}_ ┃ `{d//60}:{d%60:02d}`\n"
                if len(queue) > 8:
                    text += f"\n_\\+{len(queue)-8} ᴍᴏʀᴇ_"
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏭ sᴋɪᴘ", callback_data="util_skip"),
                InlineKeyboardButton("🔀 sʜᴜғғʟᴇ", callback_data="util_shuffle"),
                InlineKeyboardButton("🗑 ᴄʟᴇᴀʀ", callback_data="util_clear"),
            ],
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_queue"),
                InlineKeyboardButton("➕ ᴀᴅᴅ", switch_inline_query_current_chat="/play "),
            ],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ SKIP ═══
    elif query.data == "util_skip":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import voice_play, is_voice_available
        qm = MongoQueueManager()
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
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏭ sᴋɪᴘ ᴀɢᴀɪɴ", callback_data="util_skip"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(text, parse_mode="MarkdownV2", reply_markup=kb)

    # ═══ PAUSE ═══
    elif query.data == "util_pause":
        from utils.voice_chat import voice_pause
        ok = await voice_pause(chat_id)
        await query.answer("⏸ Paused!" if ok else "Not playing!", show_alert=not ok)

    # ═══ RESUME ═══
    elif query.data == "util_resume":
        from utils.voice_chat import voice_resume
        ok = await voice_resume(chat_id)
        await query.answer("▶️ Resumed!" if ok else "Not paused!", show_alert=not ok)

    # ═══ LEAVE ═══
    elif query.data == "util_leave":
        from utils.voice_chat import voice_leave
        await voice_leave(chat_id)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ ᴀɢᴀɪɴ", switch_inline_query_current_chat="/play ")],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(
            "🔇 *ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\\!*",
            parse_mode="MarkdownV2",
            reply_markup=kb
        )

    # ═══ SHUFFLE ═══
    elif query.data == "util_shuffle":
        from utils.mongo_queue_manager import MongoQueueManager
        qm = MongoQueueManager()
        if await qm.shuffle_queue(chat_id):
            await query.answer("🔀 Shuffled!", show_alert=False)
        else:
            await query.answer("Not enough songs!", show_alert=True)

    # ═══ CLEAR ═══
    elif query.data == "util_clear":
        from utils.mongo_queue_manager import MongoQueueManager
        from utils.voice_chat import voice_leave
        qm = MongoQueueManager()
        count = await qm.clear_queue(chat_id)
        await voice_leave(chat_id)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 ᴘʟᴀʏ ɴᴇᴡ", switch_inline_query_current_chat="/play ")],
            [home_btn(), dev_btn()],
        ])
        await query.edit_message_text(
            f"🗑️ *ᴄʟᴇᴀʀᴇᴅ {count} sᴏɴɢs\\!*",
            parse_mode="MarkdownV2",
            reply_markup=kb
        )


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("ᴜsᴀɢᴇ: `/ask your question`", parse_mode="MarkdownV2")
        return
    await update.message.chat.send_action(ChatAction.TYPING)
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
    now_text = f"\n🔊 *ɴᴏᴡ:* _{esc(now.get('title','')[:35])}_" if now else ""
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="util_stats"), InlineKeyboardButton("📋 ǫᴜᴇᴜᴇ", callback_data="util_queue")],
        [home_btn(), dev_btn()],
    ])
    await update.message.reply_text(
        f"📊 *sᴛᴀᴛɪsᴛɪᴄs*{now_text}\n\n"
        f"🎵 ᴘʟᴀʏᴇᴅ ➤ `{settings['stats']['total_songs_played']}`\n"
        f"➕ ǫᴜᴇᴜᴇᴅ ➤ `{settings['stats']['total_queue_added']}`\n"
        f"📻 ɪɴ ǫᴜᴇᴜᴇ ➤ `{queue_length}`\n"
        f"👥 ᴀᴅᴍɪɴs ➤ `{len(settings['admins'])}`\n"
        f"🚫 ʙᴀɴɴᴇᴅ ➤ `{len(settings['banned_users'])}`",
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=SUPPORT_CHAT), dev_btn()],
        [home_btn()],
    ])
    await update.message.reply_text(
        "ℹ️ *ᴀʙᴏᴜᴛ ʙᴏᴛ*\n\n"
        "🎵 *ᴍᴜsɪᴄ ʙᴏᴛ* — ʏᴏᴜʀ ᴜʟᴛɪᴍᴀᴛᴇ ᴍᴜsɪᴄ ᴘᴀʀᴛɴᴇʀ\n\n"
        "👨‍💻 *ᴅᴇᴠ:* [secret\\_fetcher](tg://resolve?domain=secret_fetcher)",
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    try:
        await update.message.reply_text(
            "❌ *ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ\\!*\n\nᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴜsᴇ /help",
            parse_mode="MarkdownV2"
        )
    except Exception:
        pass
