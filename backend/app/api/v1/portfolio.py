from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.dependencies import get_database, get_current_user
from app.db.crud import add_to_portfolio, get_portfolio, remove_from_portfolio

router = APIRouter()

# ---------------------
# Pydantic Models
# ---------------------

class StockHolding(BaseModel):
    symbol: str = Field(..., max_length=10, description="Stock symbol, e.g. AAPL")
    quantity: float = Field(..., gt=0, description="Number of shares held")

class PortfolioUpdateRequest(BaseModel):
    holdings: List[StockHolding] = Field(..., description="List of stock holdings")

class PortfolioOut(BaseModel):
    holdings: List[StockHolding] = Field(..., description="Current portfolio holdings")


# ---------------------
# API Endpoints
# ---------------------

@router.get("/", response_model=PortfolioOut, tags=["Portfolio"])
async def read_portfolio(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get the current logged-in user's portfolio.
    """
    portfolio = await get_portfolio(db, current_user["_id"])
    return {"holdings": portfolio or []}


@router.put("/", response_model=PortfolioOut, tags=["Portfolio"])
async def update_portfolio(
    update_req: PortfolioUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Replace the user's entire portfolio with the provided holdings list.
    """
    await add_to_portfolio(db, current_user["_id"], update_req.holdings)
    updated_portfolio = await get_portfolio(db, current_user["_id"])
    return {"holdings": updated_portfolio}


@router.delete("/{symbol}", response_model=PortfolioOut, tags=["Portfolio"])
async def delete_holding(
    symbol: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Remove a stock holding from the user's portfolio by symbol.
    """
    await remove_from_portfolio(db, current_user["_id"], symbol.upper())
    updated_portfolio = await get_portfolio(db, current_user["_id"])
    return {"holdings": updated_portfolio}
