#!/bin/bash
# ============================================================
# ROBUST llama-cpp-python CUDA Installation
# This script CANNOT be interrupted and shows live progress
# ============================================================

set -e  # Exit on error

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${YELLOW}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║  🚀 Installing llama-cpp-python with CUDA support     ║${NC}"
echo -e "${YELLOW}║     This will take 5-10 minutes - DO NOT INTERRUPT    ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check CUDA
if ! command -v nvcc &> /dev/null; then
    echo -e "${RED}❌ CUDA Toolkit not found! Install it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ CUDA Toolkit found: $(nvcc --version | grep release | awk '{print $5}')${NC}"

# Check GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}❌ NVIDIA driver not found! Install it first.${NC}"
    exit 1
fi

GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)
GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
echo -e "${GREEN}✓ Found ${GPU_COUNT}x ${GPU_NAME}${NC}"
echo ""

# Uninstall old version
echo -e "${BLUE}[1/3] Removing old llama-cpp-python...${NC}"
pip3 uninstall llama-cpp-python -y --break-system-packages 2>/dev/null || true
echo -e "${GREEN}✓ Old version removed${NC}"
echo ""

# Install with CUDA - SHOW LIVE OUTPUT
echo -e "${BLUE}[2/3] Compiling llama-cpp-python with CUDA...${NC}"
echo -e "${YELLOW}⚠️  This will take 5-10 minutes - you will see compilation output${NC}"
echo -e "${YELLOW}⚠️  DO NOT press Ctrl+C or close terminal!${NC}"
echo ""
sleep 2

CMAKE_ARGS="-DGGML_CUDA=on" \
FORCE_CMAKE=1 \
pip3 install llama-cpp-python \
    --force-reinstall \
    --no-cache-dir \
    --no-deps \
    --break-system-packages \
    --verbose

echo ""
echo -e "${GREEN}✓ Compilation finished${NC}"
echo ""

# Verify installation
echo -e "${BLUE}[3/3] Verifying CUDA support...${NC}"
python3 << 'EOF'
try:
    from llama_cpp import Llama
    import llama_cpp.llama_cpp as lib
    
    if hasattr(lib, 'llama_supports_gpu_offload'):
        print("✅ CUDA SUPPORT CONFIRMED!")
        print("   llama-cpp-python is ready to use GPU")
    else:
        print("❌ WARNING: GPU offload functions NOT found")
        print("   Installation may have failed")
        exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║        ✅ INSTALLATION SUCCESSFUL!                     ║${NC}"
    echo -e "${GREEN}║   llama-cpp-python is ready to use GPU acceleration   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║           ❌ INSTALLATION FAILED                       ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 1
fi
