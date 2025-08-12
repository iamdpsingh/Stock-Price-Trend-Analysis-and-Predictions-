from fastapi import APIRouter, HTTPException
from typing import Optional
from app.ml.predict import predict_all_stocks, predict_single_stock

router = APIRouter()

@router.get("/predict/all")
async def get_all_predictions(resolution: str = 'D', days: int = 365):
    """
    Get predictions for all stocks stored in DB using the trained model.
    resolution: '1','5','15','30','60','D','W','M'
    days: number of past days to use for feature calculation
    """
    try:
        results = predict_all_stocks(resolution=resolution, days=days)
        return {
            "status": "success",
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict/{symbol}")
async def get_single_prediction(symbol: str, resolution: str = 'D', days: int = 365):
    """
    Get prediction for a specific stock symbol.
    """
    try:
        result = predict_single_stock(symbol.upper(), resolution=resolution, days=days)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
