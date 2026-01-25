#!/bin/bash
# ================================================
# MasterCoderAI - Setup Script
# Priprema sistema za instalaciju
# ================================================

set -e

echo "=============================================="
echo "   MasterCoderAI Setup Script"
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (sudo)"
    exit 1
fi

# Check NVIDIA driver
echo ""
echo "[1/4] Checking NVIDIA driver..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
    echo "✅ NVIDIA driver OK"
else
    echo "❌ NVIDIA driver not found!"
    echo "Install with: apt install nvidia-driver-535"
    exit 1
fi

# Check CUDA
echo ""
echo "[2/4] Checking CUDA..."
if [ -d "/usr/local/cuda" ] || [ -d "/usr/lib/cuda" ]; then
    echo "✅ CUDA found"
else
    echo "⚠️ CUDA not found in standard locations"
    echo "llama-cpp-python will try to use GPU anyway"
fi

# Check Python
echo ""
echo "[3/4] Checking Python..."
python3 --version
if [ $? -eq 0 ]; then
    echo "✅ Python OK"
else
    echo "❌ Python3 not found!"
    exit 1
fi

# Check Node.js
echo ""
echo "[4/4] Checking Node.js..."
if command -v node &> /dev/null; then
    node --version
    echo "✅ Node.js OK"
else
    echo "⚠️ Node.js not found, will be installed"
fi

echo ""
echo "=============================================="
echo "   ✅ System Ready for Installation"
echo "=============================================="
echo ""
echo "Next step: Run ./install.sh"
echo ""
