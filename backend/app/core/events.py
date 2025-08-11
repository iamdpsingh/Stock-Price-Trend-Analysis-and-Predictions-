from fastapi import FastAPI
from app.db.connection import connect_to_mongo, close_mongo_connection

def register_startup_event(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        await connect_to_mongo()

def register_shutdown_event(app: FastAPI):
    @app.on_event("shutdown")
    async def shutdown_event():
        await close_mongo_connection()
