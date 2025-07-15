#!/bin/bash

# Run this script from the project root to set up and launch the full stack
set -e
PROJECT_ROOT="$(pwd)"
cd "$(dirname "$0")"

# --- BACKEND SETUP ---
echo "[1/4] Setting up backend..."
cd BACKEND/fooddeliver

# Create virtualenv if not exists
echo "Checking Python venv..."
if [ ! -d "../myvenv" ]; then
  echo "Creating Python virtual environment..."
  python -m venv ../myvenv
fi

# Activate venv
../myvenv/Scripts/activate

# Install backend dependencies
pip install -r requirements.txt

# Migrate DB if needed
echo "Running migrations..."
python manage.py migrate

# Seed DB if needed (only if no users)
USER_COUNT=$(echo "from django.contrib.auth.models import User; print(User.objects.count())" | python manage.py shell | grep -Eo '^[0-9]+$' | head -n 1)
if [ "$USER_COUNT" = "0" ] || [ -z "$USER_COUNT" ]; then
  echo "Seeding database..."
  python manage.py seed_db
else
  echo "Database already seeded."
fi

cd "$PROJECT_ROOT"

# --- FRONTEND SETUP ---
echo "[2/4] Setting up frontend and running both servers..."

# Find the frontend directory case-insensitively in the current directory
FRONTEND_DIR=$(find . -maxdepth 1 -type d -iname 'frontend' | head -n 1)
if [ -z "$FRONTEND_DIR" ]; then
  echo "ERROR: FRONTEND directory not found!" >&2
  exit 1
fi
echo "[DEBUG] Using frontend directory: $FRONTEND_DIR"

# Install frontend dependencies if needed
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi
cd "$PROJECT_ROOT"

# Use concurrently to run both backend and frontend with logs
npx concurrently -k -n BACKEND,FRONTEND -c blue,green \
  "\"C:/Users/nitro/OneDrive/Desktop/5th sem project/BACKEND/myvenv/Scripts/python.exe\" \"C:/Users/nitro/OneDrive/Desktop/5th sem project/BACKEND/fooddeliver/manage.py\" runserver 0.0.0.0:8000" \
  "cd $FRONTEND_DIR && npm run dev -- --host"

echo "[3/4] All servers started!"
echo "- Backend: http://localhost:8000/"
echo "- Frontend: http://localhost:5173/"
echo "[4/4] Use 'ps' and 'kill' to stop servers if needed."