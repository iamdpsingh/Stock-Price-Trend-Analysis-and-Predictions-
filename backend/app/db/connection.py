# app/db/connection.py

import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.core.config import settings

# Async client holder for FastAPI
class MongoDBClient:
    client: Optional[AsyncIOMotorClient] = None
    db = None

mongodb_client = MongoDBClient()

async def connect_to_mongo():
    mongodb_client.client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    mongodb_client.db = mongodb_client.client[settings.MONGODB_DB_NAME]
    print("✅ Connected to MongoDB (async)")

async def close_mongo_connection():
    if mongodb_client.client:
        mongodb_client.client.close()
        print("🛑 Closed MongoDB connection (async)")

# Sync client for standalone scripts
sync_client = MongoClient(str(settings.MONGODB_URI))
mongodb_sync_client = sync_client[settings.MONGODB_DB_NAME]
