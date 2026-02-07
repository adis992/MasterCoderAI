#!/bin/bash
# ================================================
# MasterCoderAI - Complete Installation Script
# Run this once to set up everything
# ================================================

set -e

PROJECT_DIR="/root/MasterCoderAI"
cd "$PROJECT_DIR"

echo "=============================================="
echo "   MasterCoderAI Installation Script"
echo "=============================================="

# Update system packages
echo ""
echo "[1/7] Updating system packages..."
apt-get update -qq

# Install system dependencies
echo ""
echo "[2/7] Installing system dependencies..."
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm curl sqlite3 tesseract-ocr

# Install Python packages globally
echo ""
echo "[3/7] Installing Python packages..."
pip3 install --break-system-packages \
    fastapi \
    uvicorn \
    python-jose[cryptography] \
    passlib \
    werkzeug \
    pydantic \
    databases \
    aiosqlite \
    psutil \
    GPUtil \
    requests \
    python-multipart \
    pillow \
    pytesseract \
    numpy \
    setuptools

# Install llama-cpp-python with CUDA support
echo ""
echo "[4/7] Installing llama-cpp-python with CUDA..."
CMAKE_ARGS="-DGGML_CUDA=on" pip3 install --break-system-packages llama-cpp-python --force-reinstall --no-cache-dir 2>/dev/null || \
pip3 install --break-system-packages llama-cpp-python

# Install frontend dependencies
echo ""
echo "[5/7] Installing frontend (React) dependencies..."
cd "$PROJECT_DIR/frontend"
npm install --silent

# Initialize database
echo ""
echo "[6/7] Initializing database..."
cd "$PROJECT_DIR/backend"
python3 -c "
import sys
sys.path.insert(0, '.')
from api.init_db import init_database
import asyncio
asyncio.run(init_database())
print('Database initialized successfully')
"

# Create systemd services
echo ""
echo "[7/7] Creating systemd services..."

# Backend service
cat > /etc/systemd/system/mastercoderAI-backend.service << 'EOF'
[Unit]
Description=MasterCoderAI Backend API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/MasterCoderAI/backend
ExecStart=/usr/bin/python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Frontend service
cat > /etc/systemd/system/mastercoderAI-frontend.service << 'EOF'
[Unit]
Description=MasterCoderAI Frontend React
After=network.target mastercoderAI-backend.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/MasterCoderAI/frontend
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=5
Environment=PORT=3000
Environment=BROWSER=none

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable services
systemctl daemon-reload
systemctl enable mastercoderAI-backend.service
systemctl enable mastercoderAI-frontend.service

echo ""
echo "=============================================="
echo "   ✅ Installation Complete!"
echo "=============================================="
echo ""
echo "Services created and enabled:"
echo "  - mastercoderAI-backend.service (port 8000)"
echo "  - mastercoderAI-frontend.service (port 3000)"
echo ""
echo "To start now:"
echo "  systemctl start mastercoderAI-backend"
echo "  systemctl start mastercoderAI-frontend"
echo ""
echo "Or use: ./run_all.sh"
echo ""
echo "Default login: admin / admin"
echo "=============================================="
