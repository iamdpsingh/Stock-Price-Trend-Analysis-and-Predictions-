from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "stock_price_trend_analysis_and_predictions"

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

user_collection = db.get_collection("users")
stock_collection = db.get_collection("stocks")
group_collection = db["groups"]                   # Placeholder, extend as needed
# Add more collections as required
