#!/bin/bash
# Quick fix script za MasterCoderAI

echo "🔧 MasterCoderAI Quick Fix"
echo ""

# Kill sve
echo "1. Zaustavljam sve procese..."
pkill -9 -f "uvicorn" 2>/dev/null
pkill -9 -f "react-scripts" 2>/dev/null 
pkill -9 -f "node.*3000" 2>/dev/null
pkill -9 -f "python3.*8080" 2>/dev/null
sleep 1

# Free portovi
echo "2. Oslobađam portove..."
fuser -k 3000/tcp 2>/dev/null
fuser -k 8000/tcp 2>/dev/null
fuser -k 8080/tcp 2>/dev/null
sleep 1

# Clear cache
echo "3. Čistim cache..."
rm -rf /tmp/backend.log /tmp/frontend.log 2>/dev/null
rm -rf frontend/.next 2>/dev/null
rm -rf frontend/node_modules/.cache 2>/dev/null

# Pokreni ponovo
echo "4. Pokrećem aplikaciju..."
cd /root/MasterCoderAI

# Backend
nohup /root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug > /tmp/backend.log 2>&1 &
BACKEND_PID=$!

sleep 3

# Frontend
cd frontend
export REACT_APP_API_URL="http://172.16.20.104:8000"
export PORT=3000
nohup npm start > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

cd ..

sleep 5

echo ""
echo "✅ Gotovo!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Testiranje..."

# Test backend
if curl -s http://localhost:8000/system/health | grep -q "ok"; then
    echo "✅ Backend: OK"
else 
    echo "❌ Backend: PROBLEM"
fi

# Test frontend
if curl -s http://localhost:3000 | grep -q "MasterCoderAI"; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: PROBLEM"
fi

echo ""
echo "🌐 Otvori u browseru:"
echo "   http://172.16.20.104:3000"
echo ""
echo "👤 Login: admin / admin123"