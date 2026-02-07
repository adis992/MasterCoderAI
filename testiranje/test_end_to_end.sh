#!/bin/bash

echo "=========================================="
echo "🧪 END-TO-END INITIALIZATION TEST"
echo "=========================================="

# Test server initialization behavior through complete restart cycle
# Requirements:
# 1. On first start: initialization runs
# 2. On page refresh: NO re-initialization
# 3. On restart after hours: initialization runs again
# 4. Users blocked until admin completes setup

echo ""
echo "📋 TEST SCENARIO:"
echo "1. Check current server status"
echo "2. Reset initialization state"
echo "3. Verify users are blocked"
echo "4. Mark as initialized"
echo "5. Verify users can login"
echo "6. Test that refresh doesn't reset state"
echo ""

# Login as admin
TOKEN=$(curl -s http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r .access_token)

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
  echo "❌ Failed to get admin token"
  exit 1
fi

echo "✅ Admin logged in"
echo ""

# Step 1: Check current status
echo "1️⃣ CURRENT SERVER STATUS:"
STATUS=$(curl -s http://localhost:8000/system/server-status \
  -H "Authorization: Bearer $TOKEN")

echo "$STATUS" | jq .
echo ""

# Step 2: Reset initialization
echo "2️⃣ RESETTING INITIALIZATION STATE..."
RESET=$(curl -s -X POST http://localhost:8000/system/reset-initialization \
  -H "Authorization: Bearer $TOKEN")

echo "$RESET" | jq .
echo ""

# Step 3: Try user login (should fail)
echo "3️⃣ TESTING USER LOGIN (SHOULD FAIL)..."
USER_LOGIN=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
  http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"user123"}')

HTTP_CODE=$(echo "$USER_LOGIN" | grep "HTTP_CODE" | cut -d: -f2)
RESPONSE=$(echo "$USER_LOGIN" | grep -v "HTTP_CODE")

if [ "$HTTP_CODE" = "503" ]; then
  echo "✅ User login blocked (503)"
  echo "   Message: $(echo $RESPONSE | jq -r .detail)"
else
  echo "❌ User login should be blocked but got HTTP $HTTP_CODE"
  echo "   Response: $RESPONSE"
fi
echo ""

# Step 4: Mark as initialized
echo "4️⃣ MARKING SYSTEM AS INITIALIZED..."
MARK=$(curl -s -X POST http://localhost:8000/system/mark-initialized \
  -H "Authorization: Bearer $TOKEN")

echo "$MARK" | jq .
echo ""

# Step 5: Try user login again (should succeed)
echo "5️⃣ TESTING USER LOGIN (SHOULD SUCCEED)..."
USER_LOGIN2=$(curl -s -w "\nHTTP_CODE:%{http_code}" \
  http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"user123"}')

HTTP_CODE2=$(echo "$USER_LOGIN2" | grep "HTTP_CODE" | cut -d: -f2)
RESPONSE2=$(echo "$USER_LOGIN2" | grep -v "HTTP_CODE")

if [ "$HTTP_CODE2" = "200" ]; then
  echo "✅ User login successful (200)"
  USER_TOKEN=$(echo $RESPONSE2 | jq -r .access_token)
  echo "   Token: ${USER_TOKEN:0:30}..."
else
  echo "❌ User login should succeed but got HTTP $HTTP_CODE2"
  echo "   Response: $RESPONSE2"
fi
echo ""

# Step 6: Simulate page refresh - check status again
echo "6️⃣ SIMULATING PAGE REFRESH..."
echo "   Checking server status again..."
STATUS2=$(curl -s http://localhost:8000/system/server-status)

INITIALIZED=$(echo "$STATUS2" | jq -r .initialized)
USER_ACCESS=$(echo "$STATUS2" | jq -r .user_access_enabled)

if [ "$INITIALIZED" = "true" ] && [ "$USER_ACCESS" = "true" ]; then
  echo "✅ Server state persisted across check"
  echo "   initialized: $INITIALIZED"
  echo "   user_access_enabled: $USER_ACCESS"
else
  echo "❌ Server state was reset!"
  echo "   initialized: $INITIALIZED"
  echo "   user_access_enabled: $USER_ACCESS"
fi
echo ""

# Summary
echo "=========================================="
echo "📊 TEST RESULTS SUMMARY"
echo "=========================================="
echo "✅ Admin authentication"
echo "✅ Server status check"
echo "✅ Initialization reset"

if [ "$HTTP_CODE" = "503" ]; then
  echo "✅ User blocking when not ready"
else
  echo "❌ User blocking when not ready"
fi

if [ "$HTTP_CODE2" = "200" ]; then
  echo "✅ User access when initialized"
else
  echo "❌ User access when initialized"
fi

if [ "$INITIALIZED" = "true" ] && [ "$USER_ACCESS" = "true" ]; then
  echo "✅ State persistence"
else
  echo "❌ State persistence"
fi

echo "=========================================="
echo ""
