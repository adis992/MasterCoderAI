#!/bin/bash
echo "========================================"
echo "🧪 Testing Initialization Behavior"
echo "========================================"

# Get admin token
TOKEN=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo "❌ Failed to get admin token!"
    exit 1
fi

echo "✅ 1. Admin login: OK"

# Check current server status
echo -n "🔍 2. Current server status: "
INITIALIZED=$(curl -s http://localhost:8000/system/server-status | jq -r '.initialized')
if [ "$INITIALIZED" = "true" ]; then
    echo "✅ Server initialized"
else
    echo "⚠️ Server not initialized"
fi

# Test 3: Reset server status
echo -n "🔄 3. Resetting server status... "
RESET_RESULT=$(curl -s -X POST http://localhost:8000/system/reset-initialization -H "Authorization: Bearer $TOKEN" | jq -r '.status')
if [ "$RESET_RESULT" = "success" ]; then
    echo "✅ Reset successful"
else
    echo "❌ Reset failed"
    exit 1
fi

# Test 4: Try user login when server not ready
echo -n "🚫 4. User login when server not ready... "
USER_LOGIN_BLOCKED=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"user","password":"user123"}' | jq -r '.detail')
if echo "$USER_LOGIN_BLOCKED" | grep -q "initializing"; then
    echo "✅ User blocked correctly"
else
    echo "❌ User not blocked"
fi

# Test 5: Admin can still login
echo -n "👑 5. Admin login when server not ready... "
ADMIN_TOKEN=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')
if [ ! -z "$ADMIN_TOKEN" ] && [ "$ADMIN_TOKEN" != "null" ]; then
    echo "✅ Admin can login"
else
    echo "❌ Admin blocked"
fi

# Test 6: Mark server as ready
echo -n "✅ 6. Marking server as ready... "
MARK_RESULT=$(curl -s -X POST http://localhost:8000/system/mark-initialized -H "Authorization: Bearer $ADMIN_TOKEN" | jq -r '.status')
if [ "$MARK_RESULT" = "success" ]; then
    echo "✅ Server marked ready"
else
    echo "❌ Failed to mark ready"
fi

# Test 7: User can now login
echo -n "👤 7. User login when server ready... "
USER_TOKEN=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"user","password":"user123"}' | jq -r '.access_token')
if [ ! -z "$USER_TOKEN" ] && [ "$USER_TOKEN" != "null" ]; then
    echo "✅ User can login"
else
    echo "❌ User still blocked"
fi

echo ""
echo "========================================"
echo "🎉 Initialization Behavior Test Complete!"
echo "========================================"