import logging
from typing import Optional
from config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class GPTAssistant:
    """ChatGPT AI Assistant - optional, works without API key"""

    def __init__(self):
        self.enabled = bool(OPENAI_API_KEY and OPENAI_API_KEY.strip())
        self.client = None

        if self.enabled:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
                self.model = OPENAI_MODEL
                logger.info("ChatGPT assistant enabled")
            except Exception as e:
                logger.warning(f"OpenAI init failed: {e}")
                self.enabled = False
        else:
            logger.info("OpenAI API key not set - AI features disabled")

    async def get_response(self, user_message: str, context: Optional[str] = None) -> str:
        if not self.enabled or not self.client:
            return "AI assistant is not enabled. Add OPENAI_API_KEY to use this feature."

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful music bot assistant. Be concise and friendly."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"ChatGPT error: {e}")
            return "AI assistant is currently unavailable."

    async def suggest_song_search(self, user_query: str) -> str:
        """Return query as-is if no API key"""
        if not self.enabled or not self.client:
            return user_query

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a music search expert. Return only the best search query for finding this song, nothing else."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=50,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Song suggestion error: {e}")
            return user_query

    async def get_song_info(self, song_data: dict) -> str:
        """Return basic info if no API key"""
        if not self.enabled or not self.client:
            return "🎵 Added to queue!"

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Give a one-line fun fact about this song. Use one emoji."},
                    {"role": "user", "content": f"Song: {song_data.get('title', 'Unknown')}"}
                ],
                max_tokens=80,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Song info error: {e}")
            return "🎵 Added to queue!"

    async def analyze_user_preference(self, interactions: list) -> str:
        return "Keep exploring different music styles!"
