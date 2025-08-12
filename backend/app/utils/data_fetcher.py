import os
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import finnhub

from app.ml.feature_engineering import full_feature_engineering

# ---------------------------
# Load API key from environment
# ---------------------------
FINNHUB_API_KEY = os.getenv("FINNHUB_KEY")
if not FINNHUB_API_KEY:
    raise RuntimeError("❌ FINNHUB_KEY environment variable not set in ENV/.env.")

# Initialize Finnhub client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# ---------------------------
# Fetch data for a single stock
# ---------------------------
def fetch_single_stock_data(symbol: str,
                            resolution: str = 'D',
                            days: int = 365,
                            apply_features: bool = True) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV candle data for a single stock from Finnhub and optionally add features.
    """
    try:
        to_ts = int(time.time())
        from_ts = to_ts - days * 24 * 60 * 60

        res = finnhub_client.stock_candles(symbol, resolution, from_ts, to_ts)
        if res.get("s") != "ok":
            print(f"⚠️ Data fetch failed for {symbol}: Status={res.get('s')}")
            return None

        df = pd.DataFrame({
            "date": pd.to_datetime(res["t"], unit="s"),
            "open": res["o"],
            "high": res["h"],
            "low": res["l"],
            "close": res["c"],
            "volume": res["v"]
        })
        df["symbol"] = symbol

        # Add technical indicators, patterns, and signals
        if apply_features:
            df = full_feature_engineering(df)

        return df

    except Exception as e:
        print(f"❌ Exception fetching {symbol}: {e}")
        return None


# ---------------------------
# Fetch data for all stocks
# ---------------------------
def fetch_all_stocks_data(symbols: List[str],
                          resolution: str = 'D',
                          days: int = 365,
                          apply_features: bool = True,
                          max_workers: int = 5) -> Dict[str, pd.DataFrame]:
    """
    Fetch OHLCV data for all given symbols concurrently.
    Returns dict mapping symbol -> DataFrame (enriched if apply_features=True).
    """
    results: Dict[str, pd.DataFrame] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(fetch_single_stock_data, sym, resolution, days, apply_features): sym
            for sym in symbols
        }
        for future in as_completed(future_to_symbol):
            sym = future_to_symbol[future]
            try:
                df = future.result()
                if df is not None and not df.empty:
                    results[sym] = df
                else:
                    print(f"⚠️ No data for {sym}")
            except Exception as e:
                print(f"❌ Error retrieving {sym}: {e}")
    return results


# ---------------------------
# Standalone usage for testing
# ---------------------------
if __name__ == "__main__":
    from app.db.connection import mongodb_sync_client  # ✅ synchronous client for scripts

    # Fetch all symbols from DB
    stocks_collection = mongodb_sync_client["stocks"]
    STOCKS = [doc["symbol"] for doc in stocks_collection.find({}, {"symbol": 1})]

    if not STOCKS:
        raise RuntimeError("❌ No stock symbols found in MongoDB collection 'stocks'.")

    print(f"🔎 Found {len(STOCKS)} stocks in DB: {STOCKS}")

    # Fetch & enrich all data
    data_map = fetch_all_stocks_data(STOCKS, resolution='D', days=365, apply_features=True)

    # Preview results
    for sym, df in data_map.items():
        print(f"\n📊 {sym}: {len(df)} rows, {len(df.columns)} columns")
        print(df.tail(2))
