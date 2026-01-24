#!/bin/bash
# MasterCoderAI - Stop Script

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🛑 Zaustavljam MasterCoderAI...${NC}\n"

# Stop backend
pkill -9 -f "uvicorn" && echo -e "${GREEN}✓ Backend stopped${NC}" || echo -e "${RED}✗ Backend wasn't running${NC}"

# Stop frontend
pkill -9 -f "react-scripts" && echo -e "${GREEN}✓ Frontend stopped${NC}" || echo -e "${RED}✗ Frontend wasn't running${NC}"
pkill -9 -f "node.*3000" && echo -e "${GREEN}✓ Node processes killed${NC}" || true

# Kill ports
fuser -k 3000/tcp 2>/dev/null && echo -e "${GREEN}✓ Port 3000 freed${NC}" || true
fuser -k 8000/tcp 2>/dev/null && echo -e "${GREEN}✓ Port 8000 freed${NC}" || true

echo -e "\n${GREEN}✅ MasterCoderAI zaustavljen!${NC}"
