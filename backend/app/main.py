from fastapi import FastAPI
from app.db.database import user_collection
from app.api import auth

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"msg": "Welcome to Stock Price Trend Analysis and Predictions backend."}

@app.get("/dbtest")
async def dbtest():
    users = await user_collection.find().to_list(1)
    return {
        "db_connected": True, 
        "first_user": users[0] if users else None
        }
    

