#!/bin/bash
# MasterCoderAI - Universal Start Script
# Ubija sve procese, cisti portove i pokrece backend + frontend

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

clear
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════╗"
echo "║     🤖 MasterCoderAI Launcher 🚀     ║"
echo "╔═══════════════════════════════════════╝"
echo -e "${NC}"

# 1. KILL ALL PROCESSES
echo -e "${YELLOW}[1/5] Ubijam sve procese...${NC}"
pkill -9 -f "uvicorn" 2>/dev/null && echo -e "${GREEN}  ✓ Backend stopped${NC}" || echo -e "${BLUE}  ℹ Backend wasn't running${NC}"
pkill -9 -f "react-scripts" 2>/dev/null && echo -e "${GREEN}  ✓ Frontend stopped${NC}" || echo -e "${BLUE}  ℹ Frontend wasn't running${NC}"
pkill -9 -f "node.*3000" 2>/dev/null && echo -e "${GREEN}  ✓ Node processes killed${NC}" || true
sleep 1

# 2. KILL PORTS
echo -e "${YELLOW}[2/5] Oslobađam portove 3000 i 8000...${NC}"
fuser -k 3000/tcp 2>/dev/null && echo -e "${GREEN}  ✓ Port 3000 freed${NC}" || echo -e "${BLUE}  ℹ Port 3000 was free${NC}"
fuser -k 8000/tcp 2>/dev/null && echo -e "${GREEN}  ✓ Port 8000 freed${NC}" || echo -e "${BLUE}  ℹ Port 8000 was free${NC}"
sleep 1

# 3. DETECT IP
echo -e "${YELLOW}[3/5] Detektujem IP adresu...${NC}"
SERVER_IP=$(hostname -I | awk '{print $1}')
if [ -z "$SERVER_IP" ]; then
    SERVER_IP="127.0.0.1"
fi
echo -e "${GREEN}  ✓ Server IP: ${SERVER_IP}${NC}"

# 4. START BACKEND
echo -e "${YELLOW}[4/5] Pokrećem Backend...${NC}"
cd /root/MasterCoderAI/backend
nohup /root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
sleep 3

# Check if backend started
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Backend running on http://${SERVER_IP}:8000 (PID: ${BACKEND_PID})${NC}"
else
    echo -e "${RED}  ✗ Backend failed to start! Check /tmp/backend.log${NC}"
    tail -20 /tmp/backend.log
    exit 1
fi

# 5. START FRONTEND
echo -e "${YELLOW}[5/5] Pokrećem Frontend...${NC}"
cd /root/MasterCoderAI/frontend
export REACT_APP_API_URL="http://${SERVER_IP}:8000"
export PORT=3000
nohup npm start > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
sleep 5

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          ✅ MasterCoderAI POKRENUT! ✅         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${PURPLE}📊 System Info:${NC}"
echo -e "   Backend:  ${BLUE}http://${SERVER_IP}:8000${NC} (PID: ${BACKEND_PID})"
echo -e "   Frontend: ${BLUE}http://${SERVER_IP}:3000${NC} (PID: ${FRONTEND_PID})"
echo -e "   API URL:  ${BLUE}${REACT_APP_API_URL}${NC}"
echo ""
echo -e "${PURPLE}👤 Login Credentials:${NC}"
echo -e "   Admin:  ${GREEN}username=admin${NC}, ${GREEN}password=admin123${NC}"
echo -e "   User:   ${GREEN}username=user${NC}, ${GREEN}password=user123${NC}"
echo ""
echo -e "${YELLOW}📝 Logs:${NC}"
echo -e "   Backend:  tail -f /tmp/backend.log"
echo -e "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo -e "${RED}🛑 Za zaustavljanje: ./stop.sh${NC}"
echo ""
