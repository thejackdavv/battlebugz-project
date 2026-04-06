#!/bin/bash

# Kill any existing processes on exit
trap 'kill $(jobs -p)' EXIT

echo "Starting Redis server..."
redis-server --daemonize yes

echo "Starting Celery worker..."
source .venv/bin/activate
celery -A BattleBugz worker --loglevel=info &

echo "Starting Django development server..."
python3 manage.py runserver &

echo "All services started. Press Ctrl+C to stop."
wait
