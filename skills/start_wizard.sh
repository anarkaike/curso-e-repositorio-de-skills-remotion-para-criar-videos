#!/bin/bash
echo "Starting Video Wizard..."

# Start Backend
echo "Starting API..."
cd video_wizard_api
source .venv/bin/activate
uvicorn main:app --reload --port 35000 &
API_PID=$!
cd ..

# Start Frontend
echo "Starting UI..."
cd video_wizard_ui
npm run dev -- -p 3000 &
UI_PID=$!
cd ..

echo "Wizard running!"
echo "API: http://localhost:35000"
echo "UI: http://localhost:3000"
echo "Press CTRL+C to stop"

trap "kill $API_PID $UI_PID" EXIT

wait
