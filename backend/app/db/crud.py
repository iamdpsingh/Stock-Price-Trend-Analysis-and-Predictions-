from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict


# Collection name constant for clarity
STOCKS_COLLECTION = "stocks"

async def create_stock(db: AsyncIOMotorDatabase, stock_data: dict) -> dict:
    """
    Insert new stock document into MongoDB and return the inserted stock.
    """
    result = await db[STOCKS_COLLECTION].insert_one(stock_data)
    stock = await db[STOCKS_COLLECTION].find_one({"_id": result.inserted_id})
    if stock:
        stock["id"] = str(stock["_id"])
        del stock["_id"]
    return stock

async def list_stocks(db: AsyncIOMotorDatabase) -> list[dict]:
    """
    Retrieve a list of all stocks in the collection.
    """
    cursor = db[STOCKS_COLLECTION].find({})
    stocks = []
    async for stock in cursor:
        stock["id"] = str(stock["_id"])
        del stock["_id"]
        stocks.append(stock)
    return stocks

async def get_stock_by_symbol(db: AsyncIOMotorDatabase, symbol: str) -> dict | None:
    """
    Retrieve one stock document by its symbol (case-insensitive).
    """
    stock = await db[STOCKS_COLLECTION].find_one({"symbol": symbol.upper()})
    if stock:
        stock["id"] = str(stock["_id"])
        del stock["_id"]
    return stock


# Collection name for portfolios
PORTFOLIO_COLLECTION = "portfolios"

async def get_portfolio(db: AsyncIOMotorDatabase, user_id) -> List[Dict]:
    """
    Retrieve the stock holdings list for a given user_id.
    Returns empty list if none found.
    """
    portfolio_doc = await db[PORTFOLIO_COLLECTION].find_one({"user_id": user_id})
    if portfolio_doc and "holdings" in portfolio_doc:
        return portfolio_doc["holdings"]
    return []

async def add_to_portfolio(db: AsyncIOMotorDatabase, user_id, holdings: List[Dict]):
    """
    Replace or create the portfolio document for the user with new holdings list.
    """
    await db[PORTFOLIO_COLLECTION].update_one(
        {"user_id": user_id},
        {"$set": {"holdings": [dict(symbol=h["symbol"].upper(), quantity=h["quantity"]) for h in holdings]}},
        upsert=True
    )

async def remove_from_portfolio(db: AsyncIOMotorDatabase, user_id, symbol: str):
    """
    Remove a stock holding by symbol from the user's portfolio document.
    """
    await db[PORTFOLIO_COLLECTION].update_one(
        {"user_id": user_id},
        {"$pull": {"holdings": {"symbol": symbol.upper()}}}
    )
