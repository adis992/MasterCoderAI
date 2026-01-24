#!/bin/bash
# ============================================================
# MasterCoderAI - Auto Install Script
# Full installation with NVIDIA/CUDA support
# ============================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

PROJECT_DIR="/root/MasterCoderAI"
LOG_FILE="/tmp/mastercoderAI_install.log"

# Detect IP
SERVER_IP=$(hostname -I | awk '{print $1}')
if [ -z "$SERVER_IP" ]; then
    SERVER_IP="127.0.0.1"
fi

print_header() {
    clear
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║         🤖 MasterCoderAI Auto Installer v2.0             ║"
    echo "║              Full Panel + GPU Support                     ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${CYAN}Server IP: ${SERVER_IP}${NC}"
    echo -e "${CYAN}Log file: ${LOG_FILE}${NC}"
    echo ""
}

log() {
    echo -e "$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

check_installed() {
    # Check if command exists
    command -v "$1" &> /dev/null
}

check_python_package() {
    python3 -c "import $1" 2>/dev/null
}

# ============================================================
# INSTALLATION FUNCTIONS
# ============================================================

install_system_packages() {
    log "${YELLOW}[1/8] Checking system packages...${NC}"
    
    PACKAGES_TO_INSTALL=""
    
    # Check each package
    for pkg in python3 python3-pip nodejs npm curl sqlite3 git build-essential cmake; do
        if ! dpkg -l | grep -q "^ii  $pkg "; then
            PACKAGES_TO_INSTALL="$PACKAGES_TO_INSTALL $pkg"
        fi
    done
    
    if [ -n "$PACKAGES_TO_INSTALL" ]; then
        log "${BLUE}  Installing: $PACKAGES_TO_INSTALL${NC}"
        apt-get update -qq >> "$LOG_FILE" 2>&1
        apt-get install -y -qq $PACKAGES_TO_INSTALL >> "$LOG_FILE" 2>&1
        log "${GREEN}  ✓ System packages installed${NC}"
    else
        log "${GREEN}  ✓ All system packages already installed${NC}"
    fi
}

install_nvidia_driver() {
    log "${YELLOW}[2/8] Checking NVIDIA driver...${NC}"
    
    if check_installed nvidia-smi; then
        DRIVER_VERSION=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
        log "${GREEN}  ✓ NVIDIA driver already installed (v${DRIVER_VERSION})${NC}"
    else
        log "${BLUE}  Installing NVIDIA driver...${NC}"
        apt-get install -y -qq nvidia-driver-535 >> "$LOG_FILE" 2>&1 || {
            log "${RED}  ✗ Failed to install NVIDIA driver. Please install manually.${NC}"
            return 1
        }
        log "${GREEN}  ✓ NVIDIA driver installed (reboot may be required)${NC}"
    fi
}

install_cuda_toolkit() {
    log "${YELLOW}[3/8] Checking CUDA Toolkit...${NC}"
    
    if check_installed nvcc; then
        CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | tr -d ',')
        log "${GREEN}  ✓ CUDA Toolkit already installed (v${CUDA_VERSION})${NC}"
    else
        log "${BLUE}  Installing CUDA Toolkit...${NC}"
        
        # Try to install from Ubuntu repos first
        apt-get install -y -qq nvidia-cuda-toolkit >> "$LOG_FILE" 2>&1 || {
            # If that fails, try manual installation
            log "${YELLOW}  Trying alternative CUDA installation...${NC}"
            wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb -O /tmp/cuda-keyring.deb >> "$LOG_FILE" 2>&1
            dpkg -i /tmp/cuda-keyring.deb >> "$LOG_FILE" 2>&1
            apt-get update -qq >> "$LOG_FILE" 2>&1
            apt-get install -y -qq cuda-toolkit-12-0 >> "$LOG_FILE" 2>&1
        }
        
        # Add to PATH
        echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
        export PATH=/usr/local/cuda/bin:$PATH
        
        log "${GREEN}  ✓ CUDA Toolkit installed${NC}"
    fi
}

install_python_packages() {
    log "${YELLOW}[4/8] Checking Python packages...${NC}"
    
    PYTHON_PACKAGES="fastapi uvicorn python-jose passlib werkzeug pydantic databases aiosqlite psutil GPUtil requests python-multipart"
    
    for pkg in $PYTHON_PACKAGES; do
        pkg_import=$(echo $pkg | tr '-' '_' | cut -d'[' -f1)
        if ! check_python_package "$pkg_import" 2>/dev/null; then
            log "${BLUE}  Installing $pkg...${NC}"
            pip3 install --break-system-packages -q "$pkg" >> "$LOG_FILE" 2>&1
        fi
    done
    
    log "${GREEN}  ✓ Python packages ready${NC}"
}

install_llama_cpp() {
    log "${YELLOW}[5/8] Checking llama-cpp-python (CUDA)...${NC}"
    
    # Check if llama-cpp is installed with CUDA support
    CUDA_SUPPORT=$(python3 -c "
try:
    from llama_cpp import Llama
    import llama_cpp.llama_cpp as lib
    # Check if GPU offload exists
    if hasattr(lib, 'llama_supports_gpu_offload'):
        print('cuda')
    else:
        print('cpu')
except:
    print('missing')
" 2>/dev/null)
    
    if [ "$CUDA_SUPPORT" = "cuda" ]; then
        log "${GREEN}  ✓ llama-cpp-python already installed with CUDA${NC}"
        return 0
    elif [ "$CUDA_SUPPORT" = "cpu" ]; then
        log "${YELLOW}  ⚠ llama-cpp-python found but WITHOUT CUDA - reinstalling...${NC}"
    else
        log "${BLUE}  llama-cpp-python not found - installing...${NC}"
    fi
    
    log "${BLUE}  Installing llama-cpp-python with CUDA support...${NC}"
    log "${BLUE}  This will take 3-5 minutes - LIVE OUTPUT BELOW:${NC}"
    echo ""
    
    # Uninstall old version (silent)
    pip3 uninstall llama-cpp-python -y --break-system-packages > /dev/null 2>&1 || true
    
    # Install with CUDA - SHOW LIVE OUTPUT
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip3 install llama-cpp-python \
        --force-reinstall --no-cache-dir --no-deps --break-system-packages 2>&1 | tee -a "$LOG_FILE"
    INSTALL_STATUS=${PIPESTATUS[0]}
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if [ $INSTALL_STATUS -eq 0 ]; then
        log "${GREEN}  ✓ llama-cpp-python installed with CUDA support${NC}"
        
        # Verify CUDA support
        log "${BLUE}  Verifying CUDA support...${NC}"
        python3 -c "
from llama_cpp import Llama
import llama_cpp.llama_cpp as lib
if hasattr(lib, 'llama_supports_gpu_offload'):
    print('✅ CUDA support confirmed!')
else:
    print('⚠️  Warning: CUDA support not detected')
" 2>/dev/null
        return 0
    else
        log "${RED}  ✗ CUDA installation failed - check output above${NC}"
        return 1
    fi
}

install_frontend() {
    log "${YELLOW}[6/8] Checking frontend dependencies...${NC}"
    
    cd "$PROJECT_DIR/frontend"
    
    if [ -d "node_modules" ] && [ -f "package-lock.json" ]; then
        # Check if node_modules is actually populated
        MODULE_COUNT=$(find node_modules -maxdepth 1 -type d | wc -l)
        if [ "$MODULE_COUNT" -gt 10 ]; then
            log "${GREEN}  ✓ Frontend dependencies already installed${NC}"
            return 0
        fi
    fi
    
    log "${BLUE}  Installing npm packages (this may take 2-3 minutes)...${NC}"
    npm install >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        log "${GREEN}  ✓ Frontend dependencies installed${NC}"
    else
        log "${RED}  ✗ npm install failed - check $LOG_FILE${NC}"
        return 1
    fi
}

init_database() {
    log "${YELLOW}[7/8] Initializing database...${NC}"
    
    cd "$PROJECT_DIR/backend"
    
    if [ -f "data.db" ]; then
        log "${GREEN}  ✓ Database already exists${NC}"
    else
        python3 -c "
import sys
sys.path.insert(0, '.')
from api.init_db import init_database
import asyncio
asyncio.run(init_database())
" >> "$LOG_FILE" 2>&1
        log "${GREEN}  ✓ Database initialized${NC}"
    fi
}

create_systemd_services() {
    log "${YELLOW}[8/8] Creating systemd services...${NC}"
    
    # Backend service
    cat > /etc/systemd/system/mastercoderAI-backend.service << EOF
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
    cat > /etc/systemd/system/mastercoderAI-frontend.service << EOF
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

    systemctl daemon-reload
    systemctl enable mastercoderAI-backend.service >> "$LOG_FILE" 2>&1
    systemctl enable mastercoderAI-frontend.service >> "$LOG_FILE" 2>&1
    
    log "${GREEN}  ✓ Systemd services created and enabled${NC}"
}

start_services() {
    log "${YELLOW}Starting services...${NC}"
    
    # Stop if running
    systemctl stop mastercoderAI-backend.service 2>/dev/null || true
    systemctl stop mastercoderAI-frontend.service 2>/dev/null || true
    
    # Kill any remaining processes
    pkill -9 -f "uvicorn api.main" 2>/dev/null || true
    pkill -9 -f "react-scripts" 2>/dev/null || true
    fuser -k 3000/tcp 2>/dev/null || true
    fuser -k 8000/tcp 2>/dev/null || true
    sleep 2
    
    # Start backend
    cd "$PROJECT_DIR/backend"
    nohup python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &
    sleep 3
    
    # Start frontend
    cd "$PROJECT_DIR/frontend"
    export BROWSER=none
    export PORT=3000
    nohup npm start > /tmp/frontend.log 2>&1 &
    sleep 5
    
    log "${GREEN}  ✓ Services started${NC}"
}

# ============================================================
# MAIN MENU
# ============================================================

show_menu() {
    print_header
    echo -e "${YELLOW}Choose an option:${NC}"
    echo ""
    echo "  1) Full Install (recommended for first time)"
    echo "  2) Install System Packages only"
    echo "  3) Install NVIDIA Driver only"
    echo "  4) Install CUDA Toolkit only"
    echo "  5) Install Python packages only"
    echo "  6) Install llama-cpp-python (CUDA) only"
    echo "  7) Install Frontend only"
    echo "  8) Initialize Database only"
    echo "  9) Create Systemd Services only"
    echo "  10) Start Services"
    echo "  11) Check Installation Status"
    echo "  0) Exit"
    echo ""
    read -p "Enter choice [0-11]: " choice
}

check_status() {
    print_header
    echo -e "${YELLOW}Installation Status:${NC}"
    echo ""
    
    # Python
    if check_installed python3; then
        echo -e "  Python3:        ${GREEN}✓ $(python3 --version)${NC}"
    else
        echo -e "  Python3:        ${RED}✗ Not installed${NC}"
    fi
    
    # Node
    if check_installed node; then
        echo -e "  Node.js:        ${GREEN}✓ $(node --version)${NC}"
    else
        echo -e "  Node.js:        ${RED}✗ Not installed${NC}"
    fi
    
    # NVIDIA Driver
    if check_installed nvidia-smi; then
        DRIVER=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -1)
        echo -e "  NVIDIA Driver:  ${GREEN}✓ v${DRIVER}${NC}"
    else
        echo -e "  NVIDIA Driver:  ${RED}✗ Not installed${NC}"
    fi
    
    # CUDA
    if check_installed nvcc; then
        CUDA=$(nvcc --version | grep "release" | awk '{print $5}' | tr -d ',')
        echo -e "  CUDA Toolkit:   ${GREEN}✓ v${CUDA}${NC}"
    else
        echo -e "  CUDA Toolkit:   ${RED}✗ Not installed${NC}"
    fi
    
    # llama-cpp-python
    if python3 -c "import llama_cpp" 2>/dev/null; then
        echo -e "  llama-cpp:      ${GREEN}✓ Installed${NC}"
    else
        echo -e "  llama-cpp:      ${RED}✗ Not installed${NC}"
    fi
    
    # GPU
    if check_installed nvidia-smi; then
        GPU_COUNT=$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)
        GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
        echo -e "  GPUs:           ${GREEN}✓ ${GPU_COUNT}x ${GPU_NAME}${NC}"
    fi
    
    # Database
    if [ -f "$PROJECT_DIR/backend/data.db" ]; then
        echo -e "  Database:       ${GREEN}✓ Exists${NC}"
    else
        echo -e "  Database:       ${RED}✗ Not initialized${NC}"
    fi
    
    # Services
    echo ""
    echo -e "${YELLOW}Service Status:${NC}"
    if systemctl is-active --quiet mastercoderAI-backend 2>/dev/null; then
        echo -e "  Backend:        ${GREEN}✓ Running${NC}"
    elif pgrep -f "uvicorn api.main" > /dev/null; then
        echo -e "  Backend:        ${GREEN}✓ Running (manual)${NC}"
    else
        echo -e "  Backend:        ${RED}✗ Stopped${NC}"
    fi
    
    if systemctl is-active --quiet mastercoderAI-frontend 2>/dev/null; then
        echo -e "  Frontend:       ${GREEN}✓ Running${NC}"
    elif pgrep -f "react-scripts" > /dev/null; then
        echo -e "  Frontend:       ${GREEN}✓ Running (manual)${NC}"
    else
        echo -e "  Frontend:       ${RED}✗ Stopped${NC}"
    fi
    
    echo ""
    read -p "Press Enter to continue..."
}

full_install() {
    print_header
    echo -e "${YELLOW}Starting Full Installation...${NC}"
    echo -e "${BLUE}This may take 10-15 minutes${NC}"
    echo ""
    
    install_system_packages
    install_nvidia_driver
    install_cuda_toolkit
    install_python_packages
    install_llama_cpp
    install_frontend
    init_database
    create_systemd_services
    start_services
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ✅ Installation Complete!                       ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Access the panel:${NC}"
    echo -e "  Frontend: ${BLUE}http://${SERVER_IP}:3000${NC}"
    echo -e "  Backend:  ${BLUE}http://${SERVER_IP}:8000${NC}"
    echo ""
    echo -e "${CYAN}Default login:${NC}"
    echo -e "  Username: ${GREEN}admin${NC}"
    echo -e "  Password: ${GREEN}admin${NC}"
    echo ""
    echo -e "${CYAN}Logs:${NC}"
    echo -e "  Backend:  tail -f /tmp/backend.log"
    echo -e "  Frontend: tail -f /tmp/frontend.log"
    echo -e "  Install:  cat ${LOG_FILE}"
    echo ""
}

# ============================================================
# MAIN
# ============================================================

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Clear log
> "$LOG_FILE"

# Check for --full flag for non-interactive install
if [ "$1" = "--full" ] || [ "$1" = "-f" ]; then
    full_install
    exit 0
fi

# Interactive menu
while true; do
    show_menu
    case $choice in
        1) full_install; read -p "Press Enter to continue..." ;;
        2) install_system_packages; read -p "Press Enter..." ;;
        3) install_nvidia_driver; read -p "Press Enter..." ;;
        4) install_cuda_toolkit; read -p "Press Enter..." ;;
        5) install_python_packages; read -p "Press Enter..." ;;
        6) install_llama_cpp; read -p "Press Enter..." ;;
        7) install_frontend; read -p "Press Enter..." ;;
        8) init_database; read -p "Press Enter..." ;;
        9) create_systemd_services; read -p "Press Enter..." ;;
        10) start_services; read -p "Press Enter..." ;;
        11) check_status ;;
        0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}"; sleep 1 ;;
    esac
done
