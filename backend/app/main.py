from fastapi import FastAPI
from app.core.events import register_startup_event, register_shutdown_event
from app.db.connection import connect_to_mongo, close_mongo_connection
from app.api.v1 import auth, stocks, portfolio, predict


app = FastAPI(title="Smart Stock Analysis & Prediction API", version="1.0")

# Register events
register_startup_event(app)
register_shutdown_event(app)

@app.get("/")
async def root():
    return {"message": "Backend Check"}

# Mount API routers here later (e.g., app.include_router(auth.router, prefix="/auth", tags=["Auth"]))

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/auth")
async def auth_index():
    return {"message": "Auth API works"}


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(stocks.router, prefix="/stocks", tags=["Stocks"])

app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])

app.include_router(predict.router, prefix="/api/v1", tags=["Predictions"])
