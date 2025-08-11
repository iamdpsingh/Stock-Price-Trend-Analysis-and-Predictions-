#!/bin/bash
# ==========================================
# Backend Folder/File Structure Creator (MongoDB Version)
# Run this file inside the "backend" folder
# ==========================================

echo "📂 Creating backend folder structure..."

# ----- Main app structure -----
mkdir -p app/api/v1
mkdir -p app/core
mkdir -p app/db
mkdir -p app/ml
mkdir -p app/tasks
mkdir -p app/utils
mkdir -p app/websocket

# ----- Tests -----
mkdir -p tests/unit
mkdir -p tests/integration

# ----- Scripts, Docs -----
mkdir -p scripts
mkdir -p docs

# ----- Files in app/api/v1 -----
touch app/api/v1/auth.py
touch app/api/v1/stocks.py
touch app/api/v1/portfolio.py
touch app/api/v1/predict.py
touch app/api/v1/recommendations.py
touch app/api/v1/__init__.py

# ----- File in app/api root -----
touch app/api/__init__.py

# ----- Files in app/core -----
touch app/core/config.py
touch app/core/security.py
touch app/core/dependencies.py
touch app/core/middleware.py
touch app/core/events.py
touch app/core/__init__.py

# ----- Files in app/db (MongoDB) -----
touch app/db/connection.py
touch app/db/collections.py
touch app/db/schemas.py
touch app/db/crud.py
touch app/db/__init__.py

# ----- Files in app/ml -----
touch app/ml/feature_engineering.py
touch app/ml/train.py
touch app/ml/predict.py
touch app/ml/trend_detection.py
touch app/ml/__init__.py

# ----- Files in app/tasks -----
touch app/tasks/data_fetch.py
touch app/tasks/model_retrain.py
touch app/tasks/cleanup.py
touch app/tasks/__init__.py

# ----- Files in app/utils -----
touch app/utils/indicators.py
touch app/utils/logger.py
touch app/utils/cache.py
touch app/utils/notifications.py
touch app/utils/helpers.py

# ----- Files in app/websocket -----
touch app/websocket/live_updates.py
touch app/websocket/__init__.py

# ----- Root app files -----
touch app/main.py
touch app/requirements.txt
touch app/Dockerfile

# ----- Tests -----
touch tests/conftest.py

# ----- Scripts -----
touch scripts/seed_db.py
touch scripts/backup.py
touch scripts/migrate.py

# ----- Docs -----
touch docs/api_reference.md
touch docs/architecture.md
touch docs/deployment.md

# ----- Root-level files -----
touch .env.example
touch docker-compose.yml
touch Makefile

echo "✅ Backend folder structure created successfully!"
