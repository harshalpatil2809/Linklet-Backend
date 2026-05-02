#!/usr/bin/env bash
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Linklet Backend — Starting up..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "▶ Running database migrations..."
python manage.py migrate --noinput

echo "▶ Collecting static files..."
python manage.py collectstatic --noinput

PORT="${PORT:-8000}"

echo "▶ Starting ASGI server with Uvicorn on port $PORT..."
uvicorn backend.asgi:application \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers 1 \
    --log-level info