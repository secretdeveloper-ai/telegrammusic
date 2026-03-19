import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils.music_fetcher import MusicFetcher
from utils.mongo_queue_manager import MongoQueueManager
from utils.claude_assistant import GPTAssistant

logger = logging.getLogger(__name__)
music_fetcher = MusicFetcher()
queue_manager = MongoQueueManager()
gpt_assistant = GPTAssistant()


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play a song"""
    if not context.args:
        await update.message.reply_text(
            "🎵 **Play Song**\n\n"
            "Usage: `/play <song name or URL>`\n\n"
            "Examples:\n"
            "• `/play Bohemian Rhapsody Queen`\n"
            "• `/play https://www.youtube.com/watch?v=...`\n"
            "• `/play https://open.spotify.com/track/...`",
            parse_mode="Markdown"
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    # Get AI suggestion for search
    search_query = await gpt_assistant.suggest_song_search(query)

    # Fetch music
    song_data = await music_fetcher.search_music(search_query, source="both")

    if not song_data:
        await update.message.reply_text(
            "❌ Could not find that song. Try a different search term."
        )
        return

    # Add to queue
    group_id = update.effective_chat.id
    requester_id = update.effective_user.id

    if await queue_manager.add_song(group_id, song_data, requester_id):
        # Get AI info about the song
        song_info = await gpt_assistant.get_song_info(song_data)

        queue_length = await queue_manager.get_queue_length(group_id)
        message = (
            f"✅ Added to queue:\n\n"
            f"🎵 **{song_data['title'][:100]}**\n"
            f"⏱️ Duration: {song_data['duration']}s\n"
            f"📍 Source: {song_data['source']}\n"
            f"📊 Queue position: {queue_length}\n\n"
            f"ℹ️ {song_info}"
        )
        await update.message.reply_text(message, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "❌ Queue is full! Please wait for some songs to finish."
        )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get next song that's about to play"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.peek_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 No songs in queue!")
        return

    duration = next_song.get("duration", 0)
    minutes = duration // 60
    seconds = duration % 60

    message = (
        f"▶️ **Next Song:**\n\n"
        f"🎵 {next_song['title']}\n"
        f"⏱️ Duration: {minutes}:{seconds:02d}\n"
        f"📍 Source: {next_song['source']}\n"
        f"👤 Requested by: User {next_song.get('requester_id', 'Unknown')}"
    )
    await update.message.reply_text(message, parse_mode="Markdown")


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip current song"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.get_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 No songs in queue to skip!")
        return

    duration = next_song.get("duration", 0)
    minutes = duration // 60
    seconds = duration % 60

    message = (
        f"⏭️ **Skipped!** Now playing:\n\n"
        f"🎵 {next_song['title']}\n"
        f"⏱️ Duration: {minutes}:{seconds:02d}\n"
        f"📍 Source: {next_song['source']}"
    )
    await update.message.reply_text(message, parse_mode="Markdown")


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display current queue"""
    group_id = update.effective_chat.id
    display = await queue_manager.get_queue_display(group_id, limit=10)
    await update.message.reply_text(display, parse_mode="Markdown")


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear entire queue"""
    group_id = update.effective_chat.id
    count = await queue_manager.clear_queue(group_id)
    await update.message.reply_text(
        f"🗑️ Cleared {count} songs from queue!"
    )


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shuffle queue"""
    group_id = update.effective_chat.id

    if await queue_manager.shuffle_queue(group_id):
        await update.message.reply_text("🔀 Queue shuffled!")
    else:
        await update.message.reply_text("❌ Can't shuffle empty queue!")


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove specific song from queue"""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/remove <position>`\n"
            "Example: `/remove 1` (removes first song)",
            parse_mode="Markdown"
        )
        return

    try:
        position = int(context.args[0]) - 1
        group_id = update.effective_chat.id

        song = await queue_manager.remove_song(group_id, position)
        if song:
            await update.message.reply_text(
                f"❌ Removed: **{song['title'][:100]}**",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Invalid position!")
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number!")

