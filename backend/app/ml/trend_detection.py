# ml/trend_detection.py

import pandas as pd
from app.ml.feature_engineering import add_technical_indicators

def detect_trend(df: pd.DataFrame) -> str:
    """
    Basic trend detection logic using moving averages and RSI:
    - Bullish if short-term SMA_14 > EMA_14 and RSI_14 > 50
    - Bearish if short-term SMA_14 < EMA_14 and RSI_14 < 50
    - Sideways otherwise
    Assumes indicators exist in DataFrame.
    """
    df = add_technical_indicators(df)
    last = df.iloc[-1]

    if last['SMA_14'] > last['EMA_14'] and last['RSI_14'] > 50:
        return "bullish"
    elif last['SMA_14'] < last['EMA_14'] and last['RSI_14'] < 50:
        return "bearish"
    else:
        return "sideways"

def detect_trend_extended(df: pd.DataFrame) -> dict:
    """
    Extended trend detection:
    Combines basic trend with MACD crossover and Bollinger Band position.
    Returns a dictionary including:
    - trend classification,
    - MACD trend ("positive" if MACD > MACD_signal else "negative"),
    - close price position relative to Bollinger Bands,
    - RSI value.
    """
    df = add_technical_indicators(df)
    last = df.iloc[-1]

    trend = detect_trend(df)

    macd_trend = "positive" if last['MACD'] > last['MACD_signal'] else "negative"

    if last['close'] > last['Bollinger_upper']:
        close_vs_bollinger = "above_upper"
    elif last['close'] < last['Bollinger_lower']:
        close_vs_bollinger = "below_lower"
    else:
        close_vs_bollinger = "within_bands"

    return {
        "trend": trend,
        "macd_trend": macd_trend,
        "close_vs_bollinger": close_vs_bollinger,
        "rsi": last['RSI_14']
    }

if __name__ == "__main__":
    import sys
    import pandas as pd

    if len(sys.argv) != 2:
        print("Usage: python trend_detection.py <path_to_stock_data.csv>")
        sys.exit(1)

    df = pd.read_csv(sys.argv[1], parse_dates=['date'])
    result = detect_trend_extended(df)
    print(result)
