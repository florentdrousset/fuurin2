#!/bin/sh
set -e

# Ensure Python can import local packages
export PYTHONPATH="/app:${PYTHONPATH}"

# Run migrations
alembic upgrade head

# Start API
exec uvicorn main:app --host 0.0.0.0 --port 8000
