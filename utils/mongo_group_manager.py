import logging
from typing import Dict, Optional
from datetime import datetime
from utils.mongodb_manager import mongo_manager

logger = logging.getLogger(__name__)


class MongoGroupManager:
    """Group management using MongoDB"""

    async def initialize_group(self, group_id: int, group_name: str = "Unknown") -> Dict:
        """Initialize a new group with default settings"""
        existing = await mongo_manager.find_document(
            "groups", {"group_id": group_id}
        )

        if existing:
            return existing

        group_data = {
            "group_id": group_id,
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

        await mongo_manager.insert_document("groups", group_data)
        return group_data

    async def get_group_settings(self, group_id: int) -> Dict:
        """Get group settings"""
        group = await mongo_manager.find_document("groups", {"group_id": group_id})
        if not group:
            return await self.initialize_group(group_id)
        return group

    async def add_admin(self, group_id: int, user_id: int) -> bool:
        """Add user as group admin"""
        group = await self.get_group_settings(group_id)
        if user_id in group.get("admins", []):
            return False

        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"admins": group.get("admins", []) + [user_id]}
        )
        return True

    async def remove_admin(self, group_id: int, user_id: int) -> bool:
        """Remove user from admins"""
        group = await self.get_group_settings(group_id)
        admins = group.get("admins", [])
        
        if user_id not in admins:
            return False

        admins.remove(user_id)
        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"admins": admins}
        )
        return True

    async def is_admin(self, group_id: int, user_id: int) -> bool:
        """Check if user is admin"""
        group = await self.get_group_settings(group_id)
        return user_id in group.get("admins", [])

    async def ban_user(self, group_id: int, user_id: int) -> bool:
        """Ban user from group"""
        group = await self.get_group_settings(group_id)
        banned = group.get("banned_users", [])
        
        if user_id in banned:
            return False

        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"banned_users": banned + [user_id]}
        )
        return True

    async def unban_user(self, group_id: int, user_id: int) -> bool:
        """Unban user from group"""
        group = await self.get_group_settings(group_id)
        banned = group.get("banned_users", [])
        
        if user_id not in banned:
            return False

        banned.remove(user_id)
        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"banned_users": banned}
        )
        return True

    async def is_banned(self, group_id: int, user_id: int) -> bool:
        """Check if user is banned"""
        group = await self.get_group_settings(group_id)
        return user_id in group.get("banned_users", [])

    async def set_queue_limit(self, group_id: int, limit: int) -> bool:
        """Set queue limit for group"""
        if not (1 <= limit <= 100):
            return False

        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"queue_limit": limit}
        )
        return True

    async def set_prefix(self, group_id: int, prefix: str) -> bool:
        """Set command prefix for group"""
        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"prefix": prefix}
        )
        return True

    async def get_prefix(self, group_id: int) -> str:
        """Get command prefix for group"""
        group = await self.get_group_settings(group_id)
        return group.get("prefix", "/")

    async def update_stats(self, group_id: int, songs_played: int = 0, queue_added: int = 0):
        """Update group statistics"""
        group = await self.get_group_settings(group_id)
        stats = group.get("stats", {})
        stats["total_songs_played"] += songs_played
        stats["total_queue_added"] += queue_added

        await mongo_manager.update_document(
            "groups",
            {"group_id": group_id},
            {"stats": stats}
        )

    async def get_group_info(self, group_id: int) -> str:
        """Get formatted group information"""
        settings = await self.get_group_settings(group_id)
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
