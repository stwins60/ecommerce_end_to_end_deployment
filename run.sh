#!/bin/bash
# Run DB migration and start Flask app
set -e

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi



# Run migration (create tables)
PYTHONPATH=$(pwd)/app python3 -c "from app import app, db; ctx = app.app_context(); ctx.push(); db.create_all(); ctx.pop()"

# Start the Flask app
exec python3 app/app.py
