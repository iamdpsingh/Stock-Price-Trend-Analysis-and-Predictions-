from app.db.connection import mongodb_sync_client

STOCKS_LIST = [
    # Technology
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology"},
    {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology"},
    {"symbol": "GOOGL", "name": "Alphabet Inc. Class A", "sector": "Technology"},
    {"symbol": "GOOG", "name": "Alphabet Inc. Class C", "sector": "Technology"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Communication Services"},
    {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Semiconductors"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Automotive"},
    {"symbol": "INTC", "name": "Intel Corporation", "sector": "Semiconductors"},
    {"symbol": "AMD", "name": "Advanced Micro Devices Inc.", "sector": "Semiconductors"},
    {"symbol": "IBM", "name": "International Business Machines Corp.", "sector": "Technology"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "sector": "Technology"},
    {"symbol": "ORCL", "name": "Oracle Corporation", "sector": "Technology"},
    {"symbol": "CSCO", "name": "Cisco Systems Inc.", "sector": "Technology"},

    # Financial
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial"},
    {"symbol": "BAC", "name": "Bank of America Corp", "sector": "Financial"},
    {"symbol": "WFC", "name": "Wells Fargo & Co", "sector": "Financial"},
    {"symbol": "C", "name": "Citigroup Inc.", "sector": "Financial"},
    {"symbol": "GS", "name": "Goldman Sachs Group Inc.", "sector": "Financial"},
    {"symbol": "MS", "name": "Morgan Stanley", "sector": "Financial"},
    {"symbol": "AXP", "name": "American Express Company", "sector": "Financial"},
    {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc. Class B", "sector": "Financial"},

    # Healthcare
    {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare"},
    {"symbol": "MRK", "name": "Merck & Co. Inc.", "sector": "Healthcare"},
    {"symbol": "ABT", "name": "Abbott Laboratories", "sector": "Healthcare"},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "sector": "Healthcare"},
    {"symbol": "UNH", "name": "UnitedHealth Group Incorporated", "sector": "Healthcare"},

    # Consumer Discretionary
    {"symbol": "HD", "name": "The Home Depot Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "LOW", "name": "Lowe's Companies Inc.", "sector": "Consumer Discretionary"},
    {"symbol": "NKE", "name": "Nike Inc. Class B", "sector": "Consumer Discretionary"},
    {"symbol": "SBUX", "name": "Starbucks Corporation", "sector": "Consumer Discretionary"},
    {"symbol": "MCD", "name": "McDonald's Corporation", "sector": "Consumer Discretionary"},

    # Communication Services
    {"symbol": "T", "name": "AT&T Inc.", "sector": "Communication Services"},
    {"symbol": "VZ", "name": "Verizon Communications Inc.", "sector": "Communication Services"},
    {"symbol": "CHTR", "name": "Charter Communications Inc.", "sector": "Communication Services"},

    # Energy
    {"symbol": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy"},
    {"symbol": "CVX", "name": "Chevron Corporation", "sector": "Energy"},
    {"symbol": "COP", "name": "ConocoPhillips", "sector": "Energy"},
    {"symbol": "SLB", "name": "Schlumberger Limited", "sector": "Energy"},

    # Industrials
    {"symbol": "CAT", "name": "Caterpillar Inc.", "sector": "Industrials"},
    {"symbol": "BA", "name": "The Boeing Company", "sector": "Industrials"},
    {"symbol": "LMT", "name": "Lockheed Martin Corporation", "sector": "Industrials"},
    {"symbol": "GE", "name": "General Electric Company", "sector": "Industrials"},
    {"symbol": "DE", "name": "Deere & Company", "sector": "Industrials"},

    # Utilities
    {"symbol": "NEE", "name": "NextEra Energy Inc.", "sector": "Utilities"},
    {"symbol": "DUK", "name": "Duke Energy Corporation", "sector": "Utilities"},
    {"symbol": "SO", "name": "Southern Company", "sector": "Utilities"},

    # Consumer Staples
    {"symbol": "PG", "name": "Procter & Gamble Company", "sector": "Consumer Staples"},
    {"symbol": "KO", "name": "Coca-Cola Company", "sector": "Consumer Staples"},
    {"symbol": "PEP", "name": "PepsiCo Inc.", "sector": "Consumer Staples"},
    {"symbol": "WMT", "name": "Walmart Inc.", "sector": "Consumer Staples"},
    {"symbol": "COST", "name": "Costco Wholesale Corporation", "sector": "Consumer Staples"},

    # Real Estate
    {"symbol": "PLD", "name": "Prologis Inc.", "sector": "Real Estate"},
    {"symbol": "AMT", "name": "American Tower Corporation", "sector": "Real Estate"},
    {"symbol": "CCI", "name": "Crown Castle Inc.", "sector": "Real Estate"},
    
    # Indian Stocks
    {"symbol": "RELIANCE", "name": "Reliance Industries Limited", "sector": "Energy"},
    {"symbol": "TCS", "name": "Tata Consultancy Services Limited", "sector": "Information Technology"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank Limited", "sector": "Financial Services"},
    {"symbol": "INFY", "name": "Infosys Limited", "sector": "Information Technology"},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever Limited", "sector": "Consumer Goods"},
    {"symbol": "ICICIBANK", "name": "ICICI Bank Limited", "sector": "Financial Services"},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Financial Services"},
    {"symbol": "KOTAKBANK", "name": "Kotak Mahindra Bank Limited", "sector": "Financial Services"},
    {"symbol": "AXISBANK", "name": "Axis Bank Limited", "sector": "Financial Services"},
    {"symbol": "BAJFINANCE", "name": "Bajaj Finance Limited", "sector": "Financial Services"},
    {"symbol": "LT", "name": "Larsen & Toubro Limited", "sector": "Industrials"},
    {"symbol": "MARUTI", "name": "Maruti Suzuki India Limited", "sector": "Automobiles"},
    {"symbol": "HCLTECH", "name": "HCL Technologies Limited", "sector": "Information Technology"},
    {"symbol": "ITC", "name": "ITC Limited", "sector": "Consumer Goods"},
    {"symbol": "POWERGRID", "name": "Power Grid Corporation of India Limited", "sector": "Utilities"},
    {"symbol": "ONGC", "name": "Oil and Natural Gas Corporation Limited", "sector": "Energy"},
    {"symbol": "ULTRACEMCO", "name": "UltraTech Cement Limited", "sector": "Materials"},
    {"symbol": "NESTLEIND", "name": "Nestle India Limited", "sector": "Consumer Goods"},
    {"symbol": "SUNPHARMA", "name": "Sun Pharmaceutical Industries Limited", "sector": "Pharmaceuticals"},
    {"symbol": "TITAN", "name": "Titan Company Limited", "sector": "Consumer Goods"},
    {"symbol": "DIVISLAB", "name": "Divi's Laboratories Limited", "sector": "Pharmaceuticals"},
    {"symbol": "TECHM", "name": "Tech Mahindra Limited", "sector": "Information Technology"},
    {"symbol": "JSWSTEEL", "name": "JSW Steel Limited", "sector": "Materials"},
    {"symbol": "GRASIM", "name": "Grasim Industries Limited", "sector": "Chemicals"},
    {"symbol": "EICHERMOT", "name": "Eicher Motors Limited", "sector": "Automobiles"},
    {"symbol": "BAJAJ-AUTO", "name": "Bajaj Auto Limited", "sector": "Automobiles"},
    {"symbol": "COALINDIA", "name": "Coal India Limited", "sector": "Energy"},
    {"symbol": "BRITANNIA", "name": "Britannia Industries Limited", "sector": "Consumer Goods"},
    {"symbol": "HDFCLIFE", "name": "HDFC Life Insurance Company Limited", "sector": "Financial Services"},
    {"symbol": "TATAMOTORS", "name": "Tata Motors Limited", "sector": "Automobiles"},
    {"symbol": "WIPRO", "name": "Wipro Limited", "sector": "Information Technology"},
    {"symbol": "INDUSINDBK", "name": "IndusInd Bank Limited", "sector": "Financial Services"},
    {"symbol": "BAJAJFINSV", "name": "Bajaj Finserv Limited", "sector": "Financial Services"},
    {"symbol": "CIPLA", "name": "Cipla Limited", "sector": "Pharmaceuticals"},
    {"symbol": "M&M", "name": "Mahindra & Mahindra Limited", "sector": "Automobiles"},
    {"symbol": "DRREDDY", "name": "Dr. Reddy's Laboratories Limited", "sector": "Pharmaceuticals"},
    {"symbol": "HINDALCO", "name": "Hindalco Industries Limited", "sector": "Materials"},
    {"symbol": "SHREECEM", "name": "Shree Cement Limited", "sector": "Materials"},
    {"symbol": "ICICIPRULI", "name": "ICICI Prudential Life Insurance Company Limited", "sector": "Financial Services"},
    {"symbol": "ADANIPORTS", "name": "Adani Ports and Special Economic Zone Limited", "sector": "Industrials"},
    {"symbol": "BPCL", "name": "Bharat Petroleum Corporation Limited", "sector": "Energy"},
    {"symbol": "HEROMOTOCO", "name": "Hero MotoCorp Limited", "sector": "Automobiles"},
    {"symbol": "NATIONALUM", "name": "National Aluminium Company Limited", "sector": "Materials"},
    {"symbol": "TATASTEEL", "name": "Tata Steel Limited", "sector": "Materials"},
    {"symbol": "TCS", "name": "Tata Consultancy Services Limited", "sector": "Information Technology"}
]

# Get the stocks collection
stocks_col = mongodb_sync_client["stocks"]

# Insert only if not already present
for stock in STOCKS_LIST:
    existing_stock = stocks_col.find_one({"symbol": stock["symbol"]})
    if not existing_stock:
        stocks_col.insert_one(stock)
        print(f"✅ Inserted {stock['symbol']}")
    else:
        print(f"ℹ️ {stock['symbol']} already exists in database")