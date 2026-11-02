
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

echo "▶ Starting ASGI server with Daphne on port ${PORT}..."

exec python -m daphne \
    -b 0.0.0.0 \
    -p "$PORT" \
    backend.asgi:application
