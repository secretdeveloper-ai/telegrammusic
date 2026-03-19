import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID, LOGGER_ID

logger = logging.getLogger(__name__)


async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast message to all groups (Owner only)"""
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Only owner can use this command!")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: `/broadcast <message>`\n"
            "Example: `/broadcast Bot is being maintained`",
            parse_mode="Markdown"
        )
        return

    message = " ".join(context.args)
    
    try:
        from utils.mongodb_manager import mongo_manager

        # Get all groups
        groups = await mongo_manager.find_documents("groups", {})
        
        success_count = 0
        error_count = 0

        for group in groups:
            try:
                await context.bot.send_message(
                    chat_id=group["group_id"],
                    text=f"📢 **Broadcast Message:**\n\n{message}",
                    parse_mode="Markdown"
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error sending to group {group['group_id']}: {e}")
                error_count += 1

        result = (
            f"✅ Broadcast sent!\n\n"
            f"📊 Success: {success_count}\n"
            f"❌ Failed: {error_count}"
        )
        
        await update.message.reply_text(result, parse_mode="Markdown")
        
        # Log to logger channel
        if LOGGER_ID:
            await context.bot.send_message(
                chat_id=LOGGER_ID,
                text=f"📢 **Broadcast Sent**\n\nMessage: {message}\n\n✅ {success_count} groups\n❌ {error_count} failed",
                parse_mode="Markdown"
            )

    except Exception as e:
        logger.error(f"Broadcast error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def send_to_logger(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Send message to logger channel"""
    if LOGGER_ID:
        try:
            await context.bot.send_message(
                chat_id=LOGGER_ID,
                text=message,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Error sending to logger: {e}")
