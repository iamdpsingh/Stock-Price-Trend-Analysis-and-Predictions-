from celery import Celery

celery_app = Celery(
    "smart_stock_tasks",
    broker="redis://localhost:6379/0",  # Redis broker URL
    backend="redis://localhost:6379/1",
)

celery_app.conf.beat_schedule = {
    "fetch_stock_data": {
        "task": "app.tasks.stock_tasks.fetch_and_store_stock_data",
        "schedule": 900.0,  # every 15 minutes
    }
}

celery_app.conf.timezone = "UTC"
