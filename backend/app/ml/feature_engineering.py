import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a comprehensive list of technical indicators to the DataFrame.
    """

    # --- Moving Averages ---
    df['SMA_14'] = df['close'].rolling(window=14).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['EMA_14'] = df['close'].ewm(span=14, adjust=False).mean()
    df['EMA_50'] = df['close'].ewm(span=50, adjust=False).mean()

    # Weighted Moving Average (WMA)
    def weighted_moving_average(series, window):
        weights = np.arange(1, window + 1)
        return series.rolling(window).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    df['WMA_14'] = weighted_moving_average(df['close'], 14)

    # --- Momentum Indicators ---
    # Relative Strength Index (RSI)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # Stochastic Oscillator
    low_14 = df['low'].rolling(window=14).min()
    high_14 = df['high'].rolling(window=14).max()
    df['Stoch_K'] = 100 * ((df['close'] - low_14) / (high_14 - low_14))
    df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()

    # --- Trend Indicators ---
    # MACD
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Average Directional Index (ADX)
    def calc_adx(data, n=14):
        high = data['high']
        low = data['low']
        close = data['close']

        plus_dm = high.diff()
        minus_dm = low.diff().abs()
        plus_dm = plus_dm.where((plus_dm > minus_dm) & (plus_dm > 0), 0.0)
        minus_dm = minus_dm.where((minus_dm > plus_dm) & (minus_dm > 0), 0.0)

        tr1 = pd.Series(high - low)
        tr2 = pd.Series((high - close.shift()).abs())
        tr3 = pd.Series((low - close.shift()).abs())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(window=n).mean()

        plus_di = 100 * (plus_dm.rolling(window=n).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=n).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(window=n).mean()

        return adx
    df['ADX_14'] = calc_adx(df)

    # Commodity Channel Index (CCI)
    tp = (df['high'] + df['low'] + df['close']) / 3
    cci = (tp - tp.rolling(window=20).mean()) / (0.015 * tp.rolling(window=20).std())
    df['CCI_20'] = cci

    # Bollinger Bands
    sma_20 = df['close'].rolling(window=20).mean()
    std_20 = df['close'].rolling(window=20).std()
    df['Bollinger_upper'] = sma_20 + 2 * std_20
    df['Bollinger_lower'] = sma_20 - 2 * std_20

    # Average True Range (ATR)
    high_low = df['high'] - df['low']
    high_close_prev = (df['high'] - df['close'].shift()).abs()
    low_close_prev = (df['low'] - df['close'].shift()).abs()
    tr = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
    df['ATR_14'] = tr.rolling(window=14).mean()
    
    # On-Balance Volume (OBV)
    obv = []
    obv.append(0)
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            obv.append(obv[-1] + df['volume'].iloc[i])
        elif df['close'].iloc[i] < df['close'].iloc[i-1]:
            obv.append(obv[-1] - df['volume'].iloc[i])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv

    # Volume Rate of Change (VROC)
    df['VROC'] = df['volume'].pct_change(periods=14)

    # Ichimoku Cloud Components
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()

    df['Tenkan_sen'] = (high_9 + low_9) / 2
    df['Kijun_sen'] = (high_26 + low_26) / 2
    df['Senkou_span_A'] = ((df['Tenkan_sen'] + df['Kijun_sen']) / 2).shift(26)
    df['Senkou_span_B'] = ((high_52 + low_52) / 2).shift(26)
    df['Chikou_span'] = df['close'].shift(-26)

    # Fill nans
    df.fillna(method='bfill', inplace=True)

    return df

# --- Candlestick Pattern Detection ---

def detect_candlestick_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns detecting major candlestick patterns.
    Patterns included:
        - Doji
        - Hammer / Hanging Man
        - Engulfing (Bullish/Bearish)
        - Morning Star / Evening Star
        - Shooting Star
        - Marubozu
    """

    def is_doji(row):
        body = abs(row['close'] - row['open'])
        candle_range = row['high'] - row['low']
        return body <= candle_range * 0.1

    def is_hammer(row):
        body = abs(row['close'] - row['open'])
        lower_shadow = min(row['open'], row['close']) - row['low']
        upper_shadow = row['high'] - max(row['open'], row['close'])
        return (lower_shadow > 2 * body) and (upper_shadow <= 0.1 * body)

    def is_hanging_man(row):
        # Same as hammer but appears after an uptrend normally; here just pattern detection
        return is_hammer(row)

    def is_shooting_star(row):
        body = abs(row['close'] - row['open'])
        upper_shadow = row['high'] - max(row['open'], row['close'])
        lower_shadow = min(row['open'], row['close']) - row['low']
        return (upper_shadow > 2 * body) and (lower_shadow <= 0.1 * body)

    def is_bullish_engulfing(prev, curr):
        return (prev['close'] < prev['open']) and (curr['close'] > curr['open']) and \
               (curr['close'] > prev['open']) and (curr['open'] < prev['close'])

    def is_bearish_engulfing(prev, curr):
        return (prev['close'] > prev['open']) and (curr['close'] < curr['open']) and \
               (curr['open'] > prev['close']) and (curr['close'] < prev['open'])

    def is_marubozu(row):
        body = abs(row['close'] - row['open'])
        upper_shadow = row['high'] - max(row['open'], row['close'])
        lower_shadow = min(row['open'], row['close']) - row['low']
        return (upper_shadow <= 0.05 * body) and (lower_shadow <= 0.05 * body)

    df['pattern_doji'] = df.apply(is_doji, axis=1).astype(int)
    df['pattern_hammer'] = df.apply(is_hammer, axis=1).astype(int)
    df['pattern_hanging_man'] = df.apply(is_hanging_man, axis=1).astype(int)
    df['pattern_shooting_star'] = df.apply(is_shooting_star, axis=1).astype(int)
    df['pattern_marubozu'] = df.apply(is_marubozu, axis=1).astype(int)

    # Engulfing patterns - need to compare current and previous rows
    df['pattern_bullish_engulfing'] = 0
    df['pattern_bearish_engulfing'] = 0
    for i in range(1, len(df)):
        if is_bullish_engulfing(df.iloc[i-1], df.iloc[i]):
            df.at[df.index[i], 'pattern_bullish_engulfing'] = 1
        elif is_bearish_engulfing(df.iloc[i-1], df.iloc[i]):
            df.at[df.index[i], 'pattern_bearish_engulfing'] = 1

    # Morning Star / Evening Star (3-candle pattern)
    df['pattern_morning_star'] = 0
    df['pattern_evening_star'] = 0
    for i in range(2, len(df)):
        c1 = df.iloc[i-2]
        c2 = df.iloc[i-1]
        c3 = df.iloc[i]

        # Morning Star (bullish reversal)
        cond1 = c1['close'] < c1['open']  # first candle bearish
        cond2 = abs(c2['close'] - c2['open']) < (c2['high'] - c2['low']) * 0.3  # small body (star)
        cond3 = c3['close'] > c3['open'] and c3['close'] > (c1['open'] + c1['close']) / 2  # bullish candle closing on top half of first bear candle
        if cond1 and cond2 and cond3:
            df.at[df.index[i], 'pattern_morning_star'] = 1

        # Evening Star (bearish reversal)
        cond1 = c1['close'] > c1['open']  # first candle bullish
        cond2 = abs(c2['close'] - c2['open']) < (c2['high'] - c2['low']) * 0.3
        cond3 = c3['close'] < c3['open'] and c3['close'] < (c1['open'] + c1['close']) / 2
        if cond1 and cond2 and cond3:
            df.at[df.index[i], 'pattern_evening_star'] = 1

    return df

# --- Strategy Signals ---

def generate_strategy_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate popular trading strategy signals:
    - Golden Cross: SMA_50 crosses above SMA_200
    - Death Cross: SMA_50 crosses below SMA_200
    - Overbought/Oversold signals (RSI > 70 or < 30)
    - Price Breakouts above Bollinger Bands upper/lower
    - Volume spikes relative to average
    
    Make sure SMA_200 exists or create it here
    """

    # Add SMA_200 if not present
    if 'SMA_200' not in df.columns:
        df['SMA_200'] = df['close'].rolling(window=200).mean()

    # Golden Cross: SMA_50 crosses above SMA_200
    df['golden_cross'] = ((df['SMA_50'] > df['SMA_200']) &
                         (df['SMA_50'].shift(1) <= df['SMA_200'].shift(1))).astype(int)

    # Death Cross: SMA_50 crosses below SMA_200
    df['death_cross'] = ((df['SMA_50'] < df['SMA_200']) &
                        (df['SMA_50'].shift(1) >= df['SMA_200'].shift(1))).astype(int)

    # Overbought / Oversold signals using RSI
    df['rsi_overbought'] = (df['RSI_14'] > 70).astype(int)
    df['rsi_oversold'] = (df['RSI_14'] < 30).astype(int)

    # Bollinger Band breakout
    df['bb_breakout_upper'] = (df['close'] > df['Bollinger_upper']).astype(int)
    df['bb_breakout_lower'] = (df['close'] < df['Bollinger_lower']).astype(int)

    # Volume spike: Volume > 1.5 * 20-day moving average volume
    avg_volume_20 = df['volume'].rolling(window=20).mean()
    df['volume_spike'] = (df['volume'] > 1.5 * avg_volume_20).astype(int)

    return df

# --- Combine All Feature Engineering ---

def full_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all feature engineering steps: indicators, patterns, and strategy signals.
    """
    df = add_technical_indicators(df)
    df = detect_candlestick_patterns(df)
    df = generate_strategy_signals(df)

    # Final fill for any remaining NaNs or infinite values
    df = df.replace([np.inf, -np.inf], np.nan).fillna(method='bfill').fillna(method='ffill')

    return df
