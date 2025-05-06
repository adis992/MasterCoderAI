#!/bin/bash
# Cleanup script for MasterCoderAI: remove caches and log files

echo "=== Cleaning project caches and log files ==="
# Remove Python __pycache__ directories
find . -type d -name "__pycache__" -print -exec rm -rf {} +
# Remove .pyc files
find . -type f -name "*.pyc" -print -delete
# Remove Python log files
find . -type f -name "*.log" -print -delete
# Remove pytest cache directories
find . -type d -name ".pytest_cache" -print -exec rm -rf {} +
# Remove frontend node_modules
if [ -d "frontend/webui/node_modules" ]; then
  echo "Removing frontend/webui/node_modules..."
  rm -rf frontend/webui/node_modules
fi

echo "=== Cleanup complete ==="