from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.core.config import settings

class MongoDBClient:
    client: Optional[AsyncIOMotorClient] = None
    db = None

mongodb_client = MongoDBClient()

async def connect_to_mongo():
    """
    Connect to MongoDB client and select database.
    Call this on app startup.
    """
    mongodb_client.client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    mongodb_client.db = mongodb_client.client[settings.MONGODB_DB_NAME]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    """
    Close MongoDB connection properly.
    Call this on app shutdown.
    """
    if mongodb_client.client:
        mongodb_client.client.close()
        print("🛑 Closed MongoDB connection")
