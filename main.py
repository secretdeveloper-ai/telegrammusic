import logging
import os
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_WEBHOOK_URL,
    WEBHOOK_PORT,
    DEBUG,
    LOGGER_ID,
    OWNER_ID,
    SUPPORT_CHAT
)

from handlers.music_commands import (
    play,
    play_next,
    skip,
    queue_display,
    clear_queue_cmd,
    shuffle_queue_cmd,
    remove_song,
    music_button_callback,
)

from handlers.group_commands import (
    init_group,
    group_info,
    add_admin,
    remove_admin,
    ban_user_cmd,
    unban_user_cmd,
    set_prefix_cmd,
    set_queue_limit_cmd,
)

from handlers.utility_commands import (
    start,
    help_cmd,
    ask_assistant,
    stats,
    about,
    error_handler,
    util_button_callback,
)

from handlers.broadcast_commands import broadcast_message
from utils.mongodb_manager import mongo_manager
from utils.pyrogram_client import pyrogram_client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if DEBUG else logging.INFO,
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    try:
        await mongo_manager.connect()
        await mongo_manager.create_indexes()
        logger.info("✅ MongoDB initialized")
    except Exception as e:
        logger.error(f"❌ MongoDB initialization failed: {e}")
        sys.exit(1)

    try:
        connected = await pyrogram_client.connect()
        if connected:
            logger.info("✅ Pyrogram assistant account ready for music streaming")
    except Exception as e:
        logger.warning(f"⚠️  Pyrogram client not available: {e}")

    logger.info("✅ Bot initialization complete!")


async def shutdown(application: Application) -> None:
    try:
        await mongo_manager.disconnect()
        await pyrogram_client.disconnect()
        logger.info("✅ All connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
        return

    logger.info(f"🎵 Starting {os.getenv('BOT_NAME', 'MUSIC BOT')}...")
    logger.info(f"📊 Debug Mode: {DEBUG}")
    logger.info(f"📍 Owner ID: {OWNER_ID}")
    logger.info(f"📢 Support: {SUPPORT_CHAT}")

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Music commands
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("next", play_next))
    application.add_handler(CommandHandler("skip", skip))
    application.add_handler(CommandHandler("queue", queue_display))
    application.add_handler(CommandHandler("shuffle", shuffle_queue_cmd))
    application.add_handler(CommandHandler("clear_queue", clear_queue_cmd))
    application.add_handler(CommandHandler("remove", remove_song))

    # Group commands
    application.add_handler(CommandHandler("init", init_group))
    application.add_handler(CommandHandler("info", group_info))
    application.add_handler(CommandHandler("admin_add", add_admin))
    application.add_handler(CommandHandler("admin_remove", remove_admin))
    application.add_handler(CommandHandler("ban", ban_user_cmd))
    application.add_handler(CommandHandler("unban", unban_user_cmd))
    application.add_handler(CommandHandler("set_prefix", set_prefix_cmd))
    application.add_handler(CommandHandler("queue_limit", set_queue_limit_cmd))

    # Utility commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))
    application.add_handler(CommandHandler("ask", ask_assistant))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("about", about))

    # Owner command
    application.add_handler(CommandHandler("broadcast", broadcast_message))

    # Button callbacks
    application.add_handler(CallbackQueryHandler(music_button_callback, pattern="^btn_"))
    application.add_handler(CallbackQueryHandler(util_button_callback, pattern="^util_"))
    application.add_handler(CallbackQueryHandler(util_button_callback, pattern="^(show_|back_|how_to_play)"))

    # Debug log
    async def log_all_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.getLogger("__main__").info(f"[DEBUG] Received update: {update}")
    application.add_handler(MessageHandler(filters.ALL, log_all_updates), group=-100)

    # Error handler
    application.add_error_handler(error_handler)

    # Lifecycle
    application.post_init = post_init
    application.post_stop = shutdown

    if TELEGRAM_WEBHOOK_URL:
        webhook_url = TELEGRAM_WEBHOOK_URL
        if not webhook_url.startswith("https://"):
            webhook_url = f"https://{webhook_url}"
        logger.info(f"🌐 Starting with webhook: {webhook_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=WEBHOOK_PORT,
            url_path="",
            webhook_url=webhook_url,
        )
    else:
        logger.info("🔄 Starting with polling...")
        application.run_polling()


if __name__ == "__main__":
    main()
