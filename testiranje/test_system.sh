#!/bin/bash
# Quick test script - provjeri sve komponente sistema

echo "🧪 MasterCoderAI System Test"
echo "=============================="

# 1. Backend test
echo ""
echo "1️⃣ Testing Backend..."
if curl -s http://localhost:8000/docs | grep -q "Swagger"; then
    echo "   ✅ Backend is running"
else
    echo "   ❌ Backend NOT running!"
    echo "   Run: cd /root/MasterCoderAI/backend && /root/MasterCoderAI/.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
    exit 1
fi

# 2. Database test
echo ""
echo "2️⃣ Testing Database..."
if [ -f "/root/MasterCoderAI/backend/data.db" ]; then
    echo "   ✅ Database exists"
    TABLES=$(sqlite3 /root/MasterCoderAI/backend/data.db ".tables")
    if echo "$TABLES" | grep -q "user_settings"; then
        echo "   ✅ user_settings table exists"
    else
        echo "   ❌ user_settings table missing!"
    fi
else
    echo "   ❌ Database file not found!"
fi

# 3. Frontend build test
echo ""
echo "3️⃣ Testing Frontend Build..."
if [ -f "/root/MasterCoderAI/frontend/build/index.html" ]; then
    echo "   ✅ Frontend build exists"
    SIZE=$(du -sh /root/MasterCoderAI/frontend/build | cut -f1)
    echo "   📦 Build size: $SIZE"
else
    echo "   ❌ Frontend NOT built!"
    echo "   Run: cd /root/MasterCoderAI/frontend && npm run build"
fi

# 4. Python packages test
echo ""
echo "4️⃣ Testing Python Packages..."
REQUIRED_PACKAGES=("fastapi" "uvicorn" "pillow" "pytesseract" "numpy")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if /root/MasterCoderAI/.venv/bin/python -c "import $pkg" 2>/dev/null; then
        echo "   ✅ $pkg installed"
    else
        echo "   ❌ $pkg NOT installed!"
    fi
done

# 5. Tesseract OCR test
echo ""
echo "5️⃣ Testing Tesseract OCR..."
if command -v tesseract &>/dev/null; then
    VERSION=$(tesseract --version 2>&1 | head -1)
    echo "   ✅ Tesseract installed: $VERSION"
else
    echo "   ❌ Tesseract NOT installed!"
    echo "   Run: apt-get install -y tesseract-ocr"
fi

# 6. Model check
echo ""
echo "6️⃣ Checking AI Models..."
MODEL_DIR="/root/MasterCoderAI/modeli"
if [ -d "$MODEL_DIR" ]; then
    MODEL_COUNT=$(find "$MODEL_DIR" -name "*.gguf" | wc -l)
    echo "   ✅ Model directory exists"
    echo "   📊 Found $MODEL_COUNT GGUF models"
    if [ $MODEL_COUNT -gt 0 ]; then
        echo "   Models:"
        find "$MODEL_DIR" -name "*.gguf" -exec basename {} \; | sed 's/^/      - /'
    fi
else
    echo "   ⚠️ Model directory not found"
fi

# 7. Port check
echo ""
echo "7️⃣ Checking Ports..."
if lsof -i:8000 >/dev/null 2>&1; then
    echo "   ✅ Port 8000 (Backend) is ACTIVE"
else
    echo "   ⚠️ Port 8000 is FREE (backend not running)"
fi

if lsof -i:3000 >/dev/null 2>&1; then
    echo "   ✅ Port 3000 (Frontend) is ACTIVE"
else
    echo "   ⚠️ Port 3000 is FREE (frontend not running)"
fi

# 8. GPU check
echo ""
echo "8️⃣ Checking GPU..."
if command -v nvidia-smi &>/dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1)
    echo "   ✅ GPU detected: $GPU_INFO"
else
    echo "   ⚠️ nvidia-smi not found (CPU mode?)"
fi

# Summary
echo ""
echo "=============================="
echo "✅ Test Complete!"
echo ""
echo "📌 Next Steps:"
echo "   1. Access: http://$(hostname -I | awk '{print $1}'):3000"
echo "   2. Login: admin / admin123"
echo "   3. Load model from Models tab"
echo "   4. Test chat with image upload"
echo ""
