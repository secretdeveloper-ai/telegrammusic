import logging
from typing import Optional
from openai import AsyncOpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class GPTAssistant:
    """ChatGPT AI Assistant using OpenAI"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.system_prompt = """You are a helpful Telegram music bot assistant. 
You can help users find music, manage their music queue, and provide information about songs.
Be concise and friendly in your responses. Use emoji when appropriate.
Your responses should be suitable for Telegram chat (under 4096 characters)."""

    async def get_response(self, user_message: str, context: Optional[str] = None) -> str:
        """Get response from ChatGPT"""
        try:
            if context:
                full_message = f"Context: {context}\n\nUser: {user_message}"
            else:
                full_message = user_message

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": full_message}
                ],
                max_tokens=1024,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"ChatGPT API error: {e}")
            return "Sorry, I couldn't process that request. Please try again."

    async def suggest_song_search(self, user_query: str) -> str:
        """Get AI suggestion for song search"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a music recommendation expert. Based on the user's request, suggest a good search query for finding music. Respond with just the search query, nothing else."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=200,
                temperature=0.5
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Song suggestion error: {e}")
            return user_query

    async def get_song_info(self, song_data: dict) -> str:
        """Get AI-generated info about a song"""
        try:
            prompt = f"""Based on this music information, provide a brief, interesting description:
Title: {song_data.get('title', 'Unknown')}
Duration: {song_data.get('duration', 0)} seconds
Source: {song_data.get('source', 'Unknown')}

Keep it to 1-2 sentences and use music-related emoji."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert music information provider."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Song info error: {e}")
            return "🎵 Song added to queue"

    async def analyze_user_preference(self, interactions: list) -> str:
        """Analyze user music preferences from their queue history"""
        try:
            context = f"""Analyze these user music interactions and summarize their music taste:
{chr(10).join([f'- {song}' for song in interactions[-10:]])}

Provide insights in 2-3 sentences."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a music taste analyzer."},
                    {"role": "user", "content": context}
                ],
                max_tokens=200,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Preference analysis error: {e}")
            return "Keep exploring different music styles!"

