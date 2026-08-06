#!/bin/bash
# Start backend
PORT="${PORT:-8000}"
PYTHONPATH=. python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT > backend.log 2>&1 &
BACKEND_PID=$!

# Start frontend
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
