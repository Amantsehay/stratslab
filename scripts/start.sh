#!/bin/bash
# Start development environment
# Starts the FastAPI server with auto-reload

set -e

echo "Starting development server..."
poetry run uvicorn stratslabapi.web_servers.asgi:app --reload --host 0.0.0.0 --port 8000
