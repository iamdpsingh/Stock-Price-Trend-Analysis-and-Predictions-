from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_database, get_current_user
from app.db.crud import create_stock, list_stocks, get_stock_by_symbol

router = APIRouter()

# ---------------------
# Pydantic Models
# ---------------------

class StockCreate(BaseModel):
    symbol: str = Field(..., max_length=10, description="Stock symbol, e.g. AAPL")
    name: Optional[str] = Field(None, description="Full company name")
    category: Optional[str] = Field(None, description="Stock category or sector")
    price: Optional[float] = Field(None, description="Latest stock price")

class StockOut(BaseModel):
    symbol: str
    name: Optional[str]
    category: Optional[str]
    price: Optional[float]

# ---------------------
# API Routes
# ---------------------

@router.get("/", response_model=List[StockOut], tags=["Stocks"])
async def get_stocks(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Retrieve list of all stocks.
    """
    stocks = await list_stocks(db)
    return stocks


@router.get("/{symbol}", response_model=StockOut, tags=["Stocks"])
async def get_stock(symbol: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    Get details for a stock by its symbol.
    """
    stock = await get_stock_by_symbol(db, symbol.upper())
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stock not found")
    return stock


@router.post("/", response_model=StockOut, status_code=status.HTTP_201_CREATED, tags=["Stocks"])
async def add_stock(
    stock: StockCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_user),  # Protect route: only logged in users can add
):
    """
    Create a new stock entry.
    """
    existing = await get_stock_by_symbol(db, stock.symbol.upper())
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock already exists")

    stock_data = stock.dict()
    stock_data["symbol"] = stock_data["symbol"].upper()
    created = await create_stock(db, stock_data)
    return created
