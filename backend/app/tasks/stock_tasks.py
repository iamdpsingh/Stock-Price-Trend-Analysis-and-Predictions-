import os
from app.tasks.celery_app import celery_app
from app.db.crud import update_or_create_stock
import finnhub

api_key = os.getenv("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=api_key)

@celery_app.task
def fetch_and_store_stock_data():
    try:
        # Fetch all US stock symbols
        stock_list = finnhub_client.stock_symbols('US')
        for stock in stock_list:
            symbol = stock.get("symbol")
            if not symbol:
                continue
            profile = finnhub_client.company_profile2(symbol=symbol)
            stock_data = {
                "symbol": symbol,
                "name": profile.get("name", ""),
                "sector": profile.get("finnhubIndustry", ""),
            }
            update_or_create_stock(stock_data)
    except Exception as e:
        print(f"Error fetching stock data: {e}")
