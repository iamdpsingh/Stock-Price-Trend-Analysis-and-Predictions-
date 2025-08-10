from fastapi import APIRouter, Query
from typing import List
from app.db.schemas import Stock
from app.db.crud import list_stocks_by_search

router = APIRouter(prefix="/stocks", tags=["stocks"])

@router.get("/", response_model=List[Stock])
async def search_stocks(q: str = Query(..., min_length=1)):
    stocks = await list_stocks_by_search(q)
    return stocks
