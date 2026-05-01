
set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Linklet Backend — Starting up..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "▶ Running database migrations..."
python manage.py migrate --noinput

echo "▶ Collecting static files..."
python manage.py collectstatic --noinput

echo "▶ Starting ASGI server with Uvicorn..."
uvicorn backend.asgi:application \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --log-level info