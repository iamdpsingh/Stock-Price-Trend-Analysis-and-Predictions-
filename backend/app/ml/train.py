import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from app.utils.data_fetcher import fetch_all_stocks_data
from app.db.connection import mongodb_sync_client

MODEL_SAVE_PATH = "data/models/global_stock_trend_model.joblib"

# ----------------------------------
# Training function
# ----------------------------------
def train_global_model(resolution='D', days=365):
    """
    Train a single global classification model for price movement
    using enriched multi-stock data.
    """

    # 1. Get all symbols from DB
    stocks_collection = mongodb_sync_client["stocks"]
    symbols = [doc["symbol"] for doc in stocks_collection.find({}, {"symbol": 1})]

    if not symbols:
        raise RuntimeError("❌ No stock symbols found in DB.")

    print(f"🔎 Found {len(symbols)} stock symbols to train on")

    # 2. Fetch & enrich all stock data
    all_data_map = fetch_all_stocks_data(symbols,
                                         resolution=resolution,
                                         days=days,
                                         apply_features=True)

    # 3. Combine all stock DataFrames into one
    all_dfs = []
    for sym, df in all_data_map.items():
        df = df.copy()
        # Label: price up after 1 period
        df['future_close'] = df['close'].shift(-1)
        df['price_up'] = (df['future_close'] > df['close']).astype(int)
        df['symbol'] = sym
        df.dropna(inplace=True)
        all_dfs.append(df)

    if not all_dfs:
        raise RuntimeError("❌ No valid data to train on.")

    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"📊 Combined dataset shape: {combined_df.shape}")

    # 4. Select features & target
    exclude_cols = ['date', 'symbol', 'future_close', 'price_up']
    feature_cols = [col for col in combined_df.columns if col not in exclude_cols]
    target_col = 'price_up'

    X = combined_df[feature_cols].values
    y = combined_df[target_col].values

    print(f"🧮 Features: {len(feature_cols)}, Target: {target_col}")

    # 5. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 6. Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # 7. Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    # 8. Save model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump((model, feature_cols), MODEL_SAVE_PATH)
    print(f"💾 Model + features saved to {MODEL_SAVE_PATH}")


# ----------------------------------
# Script entry point
# ----------------------------------
if __name__ == "__main__":
    train_global_model(resolution='D', days=365)
