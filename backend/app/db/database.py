import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"  # Or your MongoDB Atlas URI

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client['stock_price_trend_analysis_and_predictions']

user_collection = database.get_collection("users")
stock_collection = database.get_collection("stocks")
# Add future collections: transactions, notes, models, recommendations, etc.
