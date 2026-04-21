#!/bin/bash
echo "Stopping AI Workflow processes..."
pkill -f "orchestrator.py" 2>/dev/null || true
lsof -ti :3000 | xargs kill -9 2>/dev/null || true
lsof -ti :3001 | xargs kill -9 2>/dev/null || true
echo "Done."
