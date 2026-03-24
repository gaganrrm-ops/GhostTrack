#!/bin/bash
# GhostTrack Web Interface Startup Script

cd "$(dirname "$0")"

echo "========================================"
echo "  GhostTrack Web Interface"
echo "========================================"

# Install dependencies if needed
pip3 install -r requirements.txt -q

echo ""
echo "  Starting server on http://0.0.0.0:5000"
echo "  Access it at: http://localhost:5000"
echo ""
echo "  Press Ctrl+C to stop"
echo "========================================"
echo ""

python3 app.py
