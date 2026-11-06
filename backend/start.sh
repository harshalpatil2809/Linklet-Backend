
#!/bin/sh
set -eu

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Linklet Backend — Starting up..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "▶ Running database migrations..."
python manage.py migrate --noinput

echo "▶ Collecting static files..."
python manage.py collectstatic --noinput

echo "▶ Starting notification cleanup scheduler..."
python manage.py run_notification_cleanup &

PORT="${PORT:-8000}"

echo "▶ Starting ASGI server with Daphne on port ${PORT}..."

exec python -m daphne \
    -b 0.0.0.0 \
    -p "$PORT" \
    backend.asgi:application
