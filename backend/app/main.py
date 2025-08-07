from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth


app = FastAPI()
app.include_router(auth.router)

origins = [
    "http://localhost",
    "http://localhost:3000",  # React dev server usually runs on 3000
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    # Add any other domains or IPs as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allow these origins to access backend
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods: GET, POST, etc.
    allow_headers=["*"],            # Allow all headers (Authorization, Content-Type, etc.)
)
@app.get("/")
async def root():
    return {"msg": "Welcome to Stock Price Trend Analysis and Predictions backend."}

    

