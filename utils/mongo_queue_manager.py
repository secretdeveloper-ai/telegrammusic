import logging
from typing import Dict, List, Optional
from datetime import datetime
from utils.mongodb_manager import mongo_manager

logger = logging.getLogger(__name__)


class MongoQueueManager:
    """Queue management using MongoDB"""

    async def get_queue(self, group_id: int) -> List[Dict]:
        """Get queue for group"""
        queue_doc = await mongo_manager.find_document(
            "queues", {"group_id": group_id}
        )
        return queue_doc.get("songs", []) if queue_doc else []

    async def add_song(
        self, group_id: int, song: Dict, requester_id: int, max_queue: int = 50
    ) -> bool:
        """Add song to queue"""
        current_queue = await self.get_queue(group_id)

        if len(current_queue) >= max_queue:
            return False

        song["requester_id"] = requester_id
        song["added_at"] = datetime.now().isoformat()
        song["position"] = len(current_queue)

        queue_doc = await mongo_manager.find_document(
            "queues", {"group_id": group_id}
        )

        if queue_doc:
            current_queue.append(song)
            await mongo_manager.update_document(
                "queues",
                {"group_id": group_id},
                {"songs": current_queue}
            )
        else:
            await mongo_manager.insert_document(
                "queues",
                {
                    "group_id": group_id,
                    "songs": [song],
                    "created_at": datetime.now().isoformat()
                }
            )

        return True

    async def remove_song(self, group_id: int, position: int) -> Optional[Dict]:
        """Remove song from queue"""
        current_queue = await self.get_queue(group_id)

        if position >= len(current_queue):
            return None

        song = current_queue.pop(position)
        await mongo_manager.update_document(
            "queues",
            {"group_id": group_id},
            {"songs": current_queue}
        )
        return song

    async def get_next_song(self, group_id: int) -> Optional[Dict]:
        """Get and remove next song from queue"""
        current_queue = await self.get_queue(group_id)

        if not current_queue:
            return None

        song = current_queue.pop(0)
        await mongo_manager.update_document(
            "queues",
            {"group_id": group_id},
            {"songs": current_queue}
        )
        return song

    async def peek_next_song(self, group_id: int) -> Optional[Dict]:
        """Peek at next song without removing"""
        current_queue = await self.get_queue(group_id)
        return current_queue[0] if current_queue else None

    async def clear_queue(self, group_id: int) -> int:
        """Clear entire queue, returns number of songs removed"""
        current_queue = await self.get_queue(group_id)
        count = len(current_queue)

        if count > 0:
            await mongo_manager.update_document(
                "queues",
                {"group_id": group_id},
                {"songs": []}
            )

        return count

    async def get_queue_length(self, group_id: int) -> int:
        """Get queue length"""
        current_queue = await self.get_queue(group_id)
        return len(current_queue)

    async def get_queue_display(self, group_id: int, limit: int = 10) -> str:
        """Get formatted queue display"""
        current_queue = await self.get_queue(group_id)

        if not current_queue:
            return "🎵 Queue is empty!"

        display = "🎵 **Current Queue:**\n"
        for i, song in enumerate(current_queue[:limit] if limit else current_queue, 1):
            title = song.get("title", "Unknown")[:50]
            duration = song.get("duration", 0)
            minutes = duration // 60
            seconds = duration % 60
            display += f"{i}. {title} ({minutes}:{seconds:02d})\n"

        if len(current_queue) > limit:
            display += f"\n... and {len(current_queue) - limit} more"

        return display

    async def shuffle_queue(self, group_id: int) -> bool:
        """Shuffle queue"""
        import random

        current_queue = await self.get_queue(group_id)

        if len(current_queue) < 2:
            return False

        random.shuffle(current_queue)
        await mongo_manager.update_document(
            "queues",
            {"group_id": group_id},
            {"songs": current_queue}
        )
        return True

    async def reorder_song(self, group_id: int, from_pos: int, to_pos: int) -> bool:
        """Move song to different position in queue"""
        current_queue = await self.get_queue(group_id)

        if from_pos >= len(current_queue) or to_pos >= len(current_queue):
            return False

        song = current_queue.pop(from_pos)
        current_queue.insert(to_pos, song)

        await mongo_manager.update_document(
            "queues",
            {"group_id": group_id},
            {"songs": current_queue}
        )
        return True

    async def get_requester_queued_songs(self, group_id: int, requester_id: int) -> List[Dict]:
        """Get all songs queued by a specific user"""
        current_queue = await self.get_queue(group_id)
        return [song for song in current_queue if song.get("requester_id") == requester_id]

    async def remove_user_songs(self, group_id: int, requester_id: int) -> int:
        """Remove all songs from a user, returns count"""
        current_queue = await self.get_queue(group_id)
        original_length = len(current_queue)

        filtered_queue = [
            song for song in current_queue
            if song.get("requester_id") != requester_id
        ]

        await mongo_manager.update_document(
            "queues",
            {"group_id": group_id},
            {"songs": filtered_queue}
        )

        return original_length - len(filtered_queue)
