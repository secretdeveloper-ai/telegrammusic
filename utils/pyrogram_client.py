import logging
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from config import API_ID, API_HASH, STRING_SESSION, BOT_NAME

logger = logging.getLogger(__name__)


class PyrogramClientManager:
    """Pyrogram client for assistant account using string session"""

    def __init__(self):
        self.client: Client = None

    async def connect(self):
        """Initialize and connect Pyrogram client with string session"""
        try:
            if not STRING_SESSION or not API_ID or not API_HASH:
                logger.warning("⚠️  String session credentials not fully provided. Skipping Pyrogram client.")
                return False

            self.client = Client(
                name="music_bot_assistant",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=STRING_SESSION,
            )

            await self.client.start()
            me = await self.client.get_me()
            logger.info(f"✅ Pyrogram client connected as @{me.username}")
            return True

        except SessionPasswordNeeded:
            logger.error("❌ Session password needed. Please re-create your string session.")
            return False
        except Exception as e:
            logger.error(f"❌ Pyrogram connection error: {e}")
            return False

    async def disconnect(self):
        """Disconnect Pyrogram client"""
        if self.client:
            try:
                await self.client.stop()
                logger.info("✅ Pyrogram client disconnected")
            except Exception as e:
                logger.error(f"Error disconnecting Pyrogram: {e}")

    async def send_message(self, chat_id: int, text: str, **kwargs):
        """Send message using assistant account"""
        if not self.client:
            return None

        try:
            message = await self.client.send_message(chat_id, text, **kwargs)
            return message
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None

    async def edit_message(self, chat_id: int, message_id: int, text: str, **kwargs):
        """Edit existing message"""
        if not self.client:
            return None

        try:
            message = await self.client.edit_message_text(
                chat_id, message_id, text, **kwargs
            )
            return message
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            return None

    async def delete_message(self, chat_id: int, message_id: int):
        """Delete message"""
        if not self.client:
            return False

        try:
            await self.client.delete_messages(chat_id, message_id)
            return True
        except Exception as e:
            logger.error(f"Error deleting message: {e}")
            return False

    async def send_photo(self, chat_id: int, photo: str, **kwargs):
        """Send photo"""
        if not self.client:
            return None

        try:
            message = await self.client.send_photo(chat_id, photo, **kwargs)
            return message
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            return None

    async def get_chat(self, chat_id: int):
        """Get chat information"""
        if not self.client:
            return None

        try:
            chat = await self.client.get_chat(chat_id)
            return chat
        except Exception as e:
            logger.error(f"Error getting chat: {e}")
            return None

    async def join_chat(self, invite_link: str):
        """Join chat using invite link"""
        if not self.client:
            return False

        try:
            await self.client.join_chat(invite_link)
            logger.info(f"✅ Bot assistant joined chat via: {invite_link}")
            return True
        except Exception as e:
            logger.error(f"Error joining chat: {e}")
            return False

    async def leave_chat(self, chat_id: int):
        """Leave chat"""
        if not self.client:
            return False

        try:
            await self.client.leave_chat(chat_id)
            logger.info(f"✅ Bot assistant left chat: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error leaving chat: {e}")
            return False


# Global instance
pyrogram_client = PyrogramClientManager()
