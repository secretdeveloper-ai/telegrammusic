import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.claude_assistant import GPTAssistant
from config import SUPPORT_CHAT, BOT_NAME

logger = logging.getLogger(__name__)
gpt_assistant = GPTAssistant()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    logger.info(f"/start command received from user_id={update.effective_user.id}, chat_id={update.effective_chat.id}")
    welcome_message = (
        f"🎵 **Welcome to {BOT_NAME}!**\n\n"
        "I can play music in your group from YouTube and Spotify using ChatGPT AI!\n\n"
        "**Quick Commands:**\n"
        "• `/play <song name>` - Play a song\n"
        "• `/queue` - Show queue\n"
        "• `/skip` - Skip current song\n"
        "• `/help` - Full command list\n\n"
        f"💬 **Support**: {SUPPORT_CHAT}\n"
        "Use `/help` to see all available commands!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = (
        "🎵 **Music Commands:**\n"
        "`/play <song>` - Play a song\n"
        "`/next` - Show next song\n"
        "`/skip` - Skip current song\n"
        "`/queue` - Show current queue\n"
        "`/shuffle` - Shuffle queue\n"
        "`/remove <pos>` - Remove song at position\n"
        "`/clear_queue` - Clear entire queue\n\n"
        
        "👥 **Group Management (Admin Only):**\n"
        "`/info` - Show group info\n"
        "`/admin_add <user_id>` - Add admin\n"
        "`/admin_remove <user_id>` - Remove admin\n"
        "`/ban <user_id>` - Ban user\n"
        "`/unban <user_id>` - Unban user\n"
        "`/set_prefix <char>` - Change command prefix\n"
        "`/queue_limit <num>` - Set queue limit (1-100)\n\n"
        
        "❓ **Other:**\n"
        "`/help` - Show this message\n"
        "`/ask <question>` - Ask the AI assistant\n"
        "`/broadcast <msg>` - Send message to all groups (Owner only)"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def ask_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask ChatGPT AI assistant"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/ask <your question>`",
            parse_mode="Markdown"
        )
        return

    question = " ".join(context.args)
    await update.message.chat.send_action("typing")

    response = await gpt_assistant.get_response(question)
    await update.message.reply_text(response, parse_mode="Markdown", max_length=4096)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    from utils.mongo_queue_manager import MongoQueueManager
    from utils.mongo_group_manager import MongoGroupManager

    queue_manager = MongoQueueManager()
    group_manager = MongoGroupManager()

    group_id = update.effective_chat.id
    settings = await group_manager.get_group_settings(group_id)

    queue_length = await queue_manager.get_queue_length(group_id)

    stats_message = (
        f"📊 **Group Statistics:**\n\n"
        f"🎵 Songs Played: {settings['stats']['total_songs_played']}\n"
        f"➕ Songs Queued: {settings['stats']['total_queue_added']}\n"
        f"📻 Queue Length: {queue_length}\n"
        f"👥 Total Admins: {len(settings['admins'])}\n"
        f"🚫 Banned Users: {len(settings['banned_users'])}"
    )
    await update.message.reply_text(stats_message, parse_mode="Markdown")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About the bot"""
    about_text = (
        f"🎵 **{BOT_NAME}**\n\n"
        "A powerful Telegram music bot with ChatGPT AI integration!\n\n"
        "**Features:**\n"
        "✅ Play music from YouTube & Spotify\n"
        "✅ AI-powered assistant (ChatGPT/GPT-4)\n"
        "✅ Advanced queue management\n"
        "✅ Group management & permissions\n"
        "✅ Music statistics & analytics\n"
        "✅ Pyrogram string session for assistant account\n\n"
        "**Tech Stack:**\n"
        "• Python + Telegram Bot API\n"
        "• OpenAI ChatGPT\n"
        "• MongoDB (Data storage)\n"
        "• Pyrogram (Music streaming assistant)\n\n"
        "**Hosted on:** 🚂 Railway\n\n"
        "Use `/help` for command list."
    )
    await update.message.reply_text(about_text, parse_mode="Markdown")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(
        "❌ An error occurred. Please try again or use `/help` for assistance."
    )
