#!/bin/bash
# Docker entrypoint script for StratslabAPI

set -e

echo "Starting StratslabAPI..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if pg_isready -h "${POSTGRES_HOST:-postgres}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}" > /dev/null 2>&1; then
        echo "PostgreSQL is ready!"
        break
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "PostgreSQL not ready yet. Attempt $RETRY_COUNT/$MAX_RETRIES"
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "Failed to connect to PostgreSQL after $MAX_RETRIES attempts"
    exit 1
fi

# Run database migrations
echo "Running database migrations..."
cd /app
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uvicorn stratslabapi.web_servers.asgi:app --host 0.0.0.0 --port 8000
