import json
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
import os

logger = logging.getLogger(__name__)

# Simple file-based storage (can be replaced with database)
GROUPS_FILE = "groups_data.json"


class GroupManager:
    def __init__(self):
        self.groups: Dict[int, Dict] = self.load_groups()

    def load_groups(self) -> Dict:
        """Load group settings from file"""
        if os.path.exists(GROUPS_FILE):
            try:
                with open(GROUPS_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading groups: {e}")
        return {}

    def save_groups(self):
        """Save group settings to file"""
        try:
            with open(GROUPS_FILE, "w") as f:
                json.dump(self.groups, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving groups: {e}")

    def initialize_group(self, group_id: int, group_name: str) -> Dict:
        """Initialize a new group with default settings"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            self.groups[group_id_str] = {
                "name": group_name,
                "created_at": datetime.now().isoformat(),
                "admins": [],
                "banned_users": [],
                "queue_limit": 50,
                "max_duration": 3600,
                "prefix": "/",
                "language": "en",
                "stats": {
                    "total_songs_played": 0,
                    "total_queue_added": 0,
                },
            }
            self.save_groups()
        return self.groups.get(group_id_str, {})

    def get_group_settings(self, group_id: int) -> Dict:
        """Get group settings"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return self.initialize_group(group_id, "Unknown")
        return self.groups[group_id_str]

    def add_admin(self, group_id: int, user_id: int) -> bool:
        """Add user as group admin"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        if user_id not in self.groups[group_id_str]["admins"]:
            self.groups[group_id_str]["admins"].append(user_id)
            self.save_groups()
            return True
        return False

    def remove_admin(self, group_id: int, user_id: int) -> bool:
        """Remove user from admins"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        if user_id in self.groups[group_id_str]["admins"]:
            self.groups[group_id_str]["admins"].remove(user_id)
            self.save_groups()
            return True
        return False

    def is_admin(self, group_id: int, user_id: int) -> bool:
        """Check if user is admin"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False
        return user_id in self.groups[group_id_str]["admins"]

    def ban_user(self, group_id: int, user_id: int) -> bool:
        """Ban user from group"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        if user_id not in self.groups[group_id_str]["banned_users"]:
            self.groups[group_id_str]["banned_users"].append(user_id)
            self.save_groups()
            return True
        return False

    def unban_user(self, group_id: int, user_id: int) -> bool:
        """Unban user from group"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        if user_id in self.groups[group_id_str]["banned_users"]:
            self.groups[group_id_str]["banned_users"].remove(user_id)
            self.save_groups()
            return True
        return False

    def is_banned(self, group_id: int, user_id: int) -> bool:
        """Check if user is banned"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False
        return user_id in self.groups[group_id_str]["banned_users"]

    def set_queue_limit(self, group_id: int, limit: int) -> bool:
        """Set queue limit for group"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        if 1 <= limit <= 100:
            self.groups[group_id_str]["queue_limit"] = limit
            self.save_groups()
            return True
        return False

    def set_prefix(self, group_id: int, prefix: str) -> bool:
        """Set command prefix for group"""
        group_id_str = str(group_id)
        if group_id_str not in self.groups:
            return False

        self.groups[group_id_str]["prefix"] = prefix
        self.save_groups()
        return True

    def get_prefix(self, group_id: int) -> str:
        """Get command prefix for group"""
        group_id_str = str(group_id)
        return self.groups.get(group_id_str, {}).get("prefix", "/")

    def update_stats(self, group_id: int, songs_played: int = 0, queue_added: int = 0):
        """Update group statistics"""
        group_id_str = str(group_id)
        if group_id_str in self.groups:
            stats = self.groups[group_id_str]["stats"]
            stats["total_songs_played"] += songs_played
            stats["total_queue_added"] += queue_added
            self.save_groups()

    def get_group_info(self, group_id: int) -> str:
        """Get formatted group information"""
        settings = self.get_group_settings(group_id)
        stats = settings.get("stats", {})

        info = f"📊 **Group Info: {settings['name']}**\n"
        info += f"🔗 ID: `{group_id}`\n"
        info += f"👥 Admins: {len(settings['admins'])}\n"
        info += f"🚫 Banned: {len(settings['banned_users'])}\n"
        info += f"📻 Queue Limit: {settings['queue_limit']}\n"
        info += f"⏱️ Max Duration: {settings['max_duration']}s\n"
        info += f"📝 Prefix: `{settings['prefix']}`\n"
        info += f"🎵 Songs Played: {stats.get('total_songs_played', 0)}\n"
        info += f"➕ Songs Queued: {stats.get('total_queue_added', 0)}\n"

        return info
