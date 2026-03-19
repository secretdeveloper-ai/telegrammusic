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


def format_duration(seconds: int) -> str:
    """Format seconds to mm:ss"""
    if not seconds:
        return "0:00"
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes}:{secs:02d}"


async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play a song"""
    if not context.args:
        await update.message.reply_text(
            "🎵 Usage: /play song name\n\n"
            "Examples:\n"
            "• /play Tum Hi Aana\n"
            "• /play Humsafar\n"
            "• /play Shape of You"
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    # Get better search query from AI (falls back to original if no key)
    search_query = await gpt_assistant.suggest_song_search(query)

    # Search for song
    song_data = await music_fetcher.search_music(search_query)

    if not song_data:
        await update.message.reply_text(
            f"❌ Could not find: {query}\n\nTry a different search term."
        )
        return

    # Add to queue
    group_id = update.effective_chat.id
    requester_id = update.effective_user.id

    added = await queue_manager.add_song(group_id, song_data, requester_id)

    if added:
        duration = song_data.get("duration", 0)
        duration_str = format_duration(duration)
        queue_length = await queue_manager.get_queue_length(group_id)
        song_info = await gpt_assistant.get_song_info(song_data)

        title = song_data.get("title", "Unknown")[:80]
        source = song_data.get("source", "YouTube")
        webpage_url = song_data.get("webpage_url", "")

        message = (
            f"✅ Added to queue!\n\n"
            f"🎵 {title}\n"
            f"⏱ Duration: {duration_str}\n"
            f"📍 Source: {source}\n"
            f"📊 Position: #{queue_length}\n"
        )
        if webpage_url:
            message += f"🔗 {webpage_url}\n"
        message += f"\n{song_info}"

        await update.message.reply_text(message)
    else:
        await update.message.reply_text(
            "❌ Queue is full! Use /skip or /clear_queue first."
        )


async def play_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show next song in queue"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.peek_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 Queue is empty!")
        return

    duration = next_song.get("duration", 0)
    duration_str = format_duration(duration)
    title = next_song.get("title", "Unknown")[:80]

    message = (
        f"▶️ Next Song:\n\n"
        f"🎵 {title}\n"
        f"⏱ Duration: {duration_str}\n"
        f"📍 Source: {next_song.get('source', 'YouTube')}"
    )
    await update.message.reply_text(message)


async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Skip current song"""
    group_id = update.effective_chat.id
    next_song = await queue_manager.get_next_song(group_id)

    if not next_song:
        await update.message.reply_text("🎵 No songs in queue!")
        return

    duration = next_song.get("duration", 0)
    duration_str = format_duration(duration)
    title = next_song.get("title", "Unknown")[:80]

    message = (
        f"⏭️ Skipped!\n\n"
        f"🎵 {title}\n"
        f"⏱ Duration: {duration_str}\n"
        f"📍 Source: {next_song.get('source', 'YouTube')}"
    )
    await update.message.reply_text(message)


async def queue_display(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display current queue"""
    group_id = update.effective_chat.id
    queue = await queue_manager.get_queue(group_id)

    if not queue:
        await update.message.reply_text("🎵 Queue is empty!\n\nUse /play to add songs.")
        return

    display = f"🎵 Queue ({len(queue)} songs):\n\n"
    for i, song in enumerate(queue[:10], 1):
        title = song.get("title", "Unknown")[:50]
        duration = song.get("duration", 0)
        duration_str = format_duration(duration)
        display += f"{i}. {title} ({duration_str})\n"

    if len(queue) > 10:
        display += f"\n... and {len(queue) - 10} more songs"

    await update.message.reply_text(display)


async def clear_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear entire queue"""
    group_id = update.effective_chat.id
    count = await queue_manager.clear_queue(group_id)
    await update.message.reply_text(f"🗑️ Cleared {count} songs from queue!")


async def shuffle_queue_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shuffle queue"""
    group_id = update.effective_chat.id

    if await queue_manager.shuffle_queue(group_id):
        await update.message.reply_text("🔀 Queue shuffled!")
    else:
        await update.message.reply_text("❌ Not enough songs to shuffle!")


async def remove_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove specific song from queue"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /remove position\n"
            "Example: /remove 2"
        )
        return

    try:
        position = int(context.args[0]) - 1
        if position < 0:
            await update.message.reply_text("❌ Position must be 1 or higher!")
            return

        group_id = update.effective_chat.id
        song = await queue_manager.remove_song(group_id, position)

        if song:
            title = song.get("title", "Unknown")[:60]
            await update.message.reply_text(f"❌ Removed: {title}")
        else:
            await update.message.reply_text("❌ Invalid position! Use /queue to see positions.")
    except ValueError:
        await update.message.reply_text("❌ Please provide a valid number!")
