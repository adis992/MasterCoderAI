#!/bin/bash
# cleanup.sh - Ubuntu/Linux: provjeri i instaliraj NVIDIA drivere i docker-nvidia runtime ako treba

# Provjeri ima li NVIDIA GPU
if lspci | grep -i nvidia > /dev/null; then
  echo "[INFO] NVIDIA GPU detected."
  # Provjeri je li driver instaliran
  if ! nvidia-smi > /dev/null 2>&1; then
    echo "[INFO] NVIDIA driver not found. Installing..."
    sudo apt-get update && sudo apt-get install -y nvidia-driver-535
  else
    echo "[INFO] NVIDIA driver already installed."
  fi
  # Provjeri je li nvidia-docker instaliran
  if ! docker info | grep -i nvidia > /dev/null; then
    echo "[INFO] nvidia-docker runtime not found. Installing..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
      sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt-get update && sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
  else
    echo "[INFO] nvidia-docker runtime already installed."
  fi
else
  echo "[INFO] No NVIDIA GPU detected. Skipping GPU driver and nvidia-docker install."
fi

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