import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# Simple file-based storage for queues
QUEUES_FILE = "queues_data.json"


class QueueManager:
    def __init__(self):
        self.queues: Dict[int, List[Dict]] = self.load_queues()

    def load_queues(self) -> Dict:
        """Load queue data from file"""
        if os.path.exists(QUEUES_FILE):
            try:
                with open(QUEUES_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading queues: {e}")
        return {}

    def save_queues(self):
        """Save queue data to file"""
        try:
            with open(QUEUES_FILE, "w") as f:
                json.dump(self.queues, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving queues: {e}")

    def get_queue(self, group_id: int) -> List[Dict]:
        """Get queue for group"""
        group_id_str = str(group_id)
        return self.queues.get(group_id_str, [])

    def add_song(self, group_id: int, song: Dict, requester_id: int, max_queue: int = 50) -> bool:
        """Add song to queue"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues:
            self.queues[group_id_str] = []

        if len(self.queues[group_id_str]) >= max_queue:
            return False

        song["requester_id"] = requester_id
        song["added_at"] = datetime.now().isoformat()
        song["position"] = len(self.queues[group_id_str])

        self.queues[group_id_str].append(song)
        self.save_queues()
        return True

    def remove_song(self, group_id: int, position: int) -> Optional[Dict]:
        """Remove song from queue"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues or position >= len(
            self.queues[group_id_str]
        ):
            return None

        song = self.queues[group_id_str].pop(position)
        self.save_queues()
        return song

    def get_next_song(self, group_id: int) -> Optional[Dict]:
        """Get and remove next song from queue"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues or len(self.queues[group_id_str]) == 0:
            return None

        song = self.queues[group_id_str].pop(0)
        self.save_queues()
        return song

    def peek_next_song(self, group_id: int) -> Optional[Dict]:
        """Peek at next song without removing"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues or len(self.queues[group_id_str]) == 0:
            return None

        return self.queues[group_id_str][0]

    def clear_queue(self, group_id: int) -> int:
        """Clear entire queue, returns number of songs removed"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues:
            return 0

        count = len(self.queues[group_id_str])
        self.queues[group_id_str] = []
        self.save_queues()
        return count

    def get_queue_length(self, group_id: int) -> int:
        """Get queue length"""
        group_id_str = str(group_id)
        return len(self.queues.get(group_id_str, []))

    def get_queue_display(self, group_id: int, limit: int = 10) -> str:
        """Get formatted queue display"""
        group_id_str = str(group_id)
        queue = self.queues.get(group_id_str, [])

        if not queue:
            return "🎵 Queue is empty!"

        display = "🎵 **Current Queue:**\n"
        for i, song in enumerate(queue[:limit] if limit else queue, 1):
            title = song.get("title", "Unknown")[:50]
            duration = song.get("duration", 0)
            minutes = duration // 60
            seconds = duration % 60
            display += f"{i}. {title} ({minutes}:{seconds:02d})\n"

        if len(queue) > limit:
            display += f"\n... and {len(queue) - limit} more"

        return display

    def shuffle_queue(self, group_id: int) -> bool:
        """Shuffle queue"""
        import random

        group_id_str = str(group_id)

        if group_id_str not in self.queues or len(self.queues[group_id_str]) < 2:
            return False

        random.shuffle(self.queues[group_id_str])
        self.save_queues()
        return True

    def reorder_song(self, group_id: int, from_pos: int, to_pos: int) -> bool:
        """Move song to different position in queue"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues:
            return False

        queue = self.queues[group_id_str]
        if from_pos >= len(queue) or to_pos >= len(queue):
            return False

        song = queue.pop(from_pos)
        queue.insert(to_pos, song)
        self.save_queues()
        return True

    def get_requester_queued_songs(self, group_id: int, requester_id: int) -> List[Dict]:
        """Get all songs queued by a specific user"""
        group_id_str = str(group_id)
        queue = self.queues.get(group_id_str, [])
        return [song for song in queue if song.get("requester_id") == requester_id]

    def remove_user_songs(self, group_id: int, requester_id: int) -> int:
        """Remove all songs from a user, returns count"""
        group_id_str = str(group_id)

        if group_id_str not in self.queues:
            return 0

        original_length = len(self.queues[group_id_str])
        self.queues[group_id_str] = [
            song
            for song in self.queues[group_id_str]
            if song.get("requester_id") != requester_id
        ]
        self.save_queues()
        return original_length - len(self.queues[group_id_str])
