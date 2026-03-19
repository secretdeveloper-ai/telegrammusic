import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Dict, List
from config import MONGO_DB_URI, MONGO_DB_NAME

logger = logging.getLogger(__name__)


class MongoDBManager:
    """MongoDB connection and operations manager"""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(MONGO_DB_URI)
            self.db = self.client[MONGO_DB_NAME]
            # Verify connection
            await self.db.command("ping")
            logger.info("✅ Connected to MongoDB")
        except Exception as e:
            logger.error(f"❌ MongoDB connection error: {e}")
            raise

    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ Disconnected from MongoDB")

    async def insert_document(self, collection: str, document: Dict) -> str:
        """Insert document and return ID"""
        try:
            result = await self.db[collection].insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            raise

    async def find_document(self, collection: str, filter: Dict) -> Optional[Dict]:
        """Find single document"""
        try:
            return await self.db[collection].find_one(filter)
        except Exception as e:
            logger.error(f"Error finding document: {e}")
            return None

    async def find_documents(self, collection: str, filter: Dict = None) -> List[Dict]:
        """Find multiple documents"""
        try:
            cursor = self.db[collection].find(filter or {})
            return await cursor.to_list(None)
        except Exception as e:
            logger.error(f"Error finding documents: {e}")
            return []

    async def update_document(self, collection: str, filter: Dict, update: Dict) -> bool:
        """Update document"""
        try:
            result = await self.db[collection].update_one(
                filter, {"$set": update}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            return False

    async def delete_document(self, collection: str, filter: Dict) -> bool:
        """Delete document"""
        try:
            result = await self.db[collection].delete_one(filter)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

    async def create_indexes(self):
        """Create necessary indexes"""
        try:
            # Groups collection
            await self.db["groups"].create_index("group_id", unique=True)
            
            # Queues collection
            await self.db["queues"].create_index("group_id")
            
            # User preferences
            await self.db["users"].create_index("user_id", unique=True)
            
            logger.info("✅ Indexes created")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")


# Global instance
mongo_manager = MongoDBManager()
