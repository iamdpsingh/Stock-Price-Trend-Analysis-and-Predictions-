from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.crud import follow_stock, unfollow_stock

router = APIRouter(prefix="/follow", tags=["follow"])

@router.post("/{stock_symbol}")
async def follow(stock_symbol: str, current_user=Depends(get_current_user)):
    success = await follow_stock(current_user["username"], stock_symbol)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to follow stock")
    return {"msg": f"Now following {stock_symbol}"}

@router.delete("/{stock_symbol}")
async def unfollow(stock_symbol: str, current_user=Depends(get_current_user)):
    success = await unfollow_stock(current_user["username"], stock_symbol)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to unfollow stock")
    return {"msg": f"Unfollowed {stock_symbol}"}
