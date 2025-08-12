import os
import joblib
from typing import Dict, Any
from app.utils.data_fetcher import fetch_single_stock_data
from app.db.connection import mongodb_sync_client
from app.ml.trend_detection import detect_trend_extended

MODEL_PATH = "data/models/global_stock_trend_model.joblib"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"❌ Model file not found at {MODEL_PATH}. Please train first.")
    model, feature_cols = joblib.load(MODEL_PATH)
    return model, feature_cols

def predict_all_stocks(resolution='D', days=365) -> Dict[str, Any]:
    from app.utils.data_fetcher import fetch_all_stocks_data
    model, feature_cols = load_model()
    symbols = [doc["symbol"] for doc in mongodb_sync_client["stocks"].find({}, {"symbol": 1})]
    data_map = fetch_all_stocks_data(symbols, resolution=resolution, days=days, apply_features=True)
    results = {}
    for sym, df in data_map.items():
        try:
            X_latest = df[feature_cols].values[-1:]
            prob_up = model.predict_proba(X_latest)[0][1]
            label_up = int(model.predict(X_latest)[0])
            trend_info = detect_trend_extended(df)
            results[sym] = {
                "predicted_label": label_up,
                "predicted_probability_up": round(float(prob_up), 4),
                "trend_analysis": trend_info,
                "latest_date": str(df.iloc[-1]["date"])
            }
        except Exception as e:
            results[sym] = {"error": str(e)}
    return results

def predict_single_stock(symbol: str, resolution='D', days=365) -> Dict[str, Any]:
    model, feature_cols = load_model()
    df = fetch_single_stock_data(symbol, resolution=resolution, days=days, apply_features=True)
    if df is None or df.empty:
        return {"error": f"No data available for {symbol}"}
    try:
        X_latest = df[feature_cols].values[-1:]
        prob_up = model.predict_proba(X_latest)[0][1]
        label_up = int(model.predict(X_latest)[0])
        trend_info = detect_trend_extended(df)
        return {
            "predicted_label": label_up,
            "predicted_probability_up": round(float(prob_up), 4),
            "trend_analysis": trend_info,
            "latest_date": str(df.iloc[-1]["date"])
        }
    except Exception as e:
        return {"error": str(e)}
