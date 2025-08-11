from fastapi import FastAPI
from app.core.events import register_startup_event, register_shutdown_event

app = FastAPI(title="Smart Stock Analysis & Prediction API", version="1.0")

# Register events
register_startup_event(app)
register_shutdown_event(app)

# Mount API routers here later (e.g., app.include_router(auth.router, prefix="/auth", tags=["Auth"]))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
