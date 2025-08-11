from typing import Generator
from app.db.connection import mongodb_client
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_database() -> Generator[AsyncIOMotorDatabase, None, None]:
    """
    Yield a MongoDB database instance for dependency injection.
    """
    yield mongodb_client.db
