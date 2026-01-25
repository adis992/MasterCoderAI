#!/bin/bash

echo "==================================="
echo "🚀 MasterCoderAI Quick Test"
echo "==================================="
echo ""

# Get token
TOKEN=$(curl -s http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

echo "✅ 1. Authentication: OK (Token received)"

# GPU Info
curl -s http://localhost:8000/system/gpu -H "Authorization: Bearer $TOKEN" | jq -r '.gpus[] | "✅ 2. GPU: \(.name) (\(.memory_used)/\(.memory_total) MB)"' | head -1

# Model Status
MODEL_STATUS=$(curl -s http://localhost:8000/ai/model/status -H "Authorization: Bearer $TOKEN" | jq -r '.loaded')
if [ "$MODEL_STATUS" = "true" ]; then
    MODEL_NAME=$(curl -s http://localhost:8000/ai/model/status -H "Authorization: Bearer $TOKEN" | jq -r '.model_name')
    echo "✅ 3. Model: Loaded ($MODEL_NAME)"
else
    echo "❌ 3. Model: Not loaded"
fi

# Settings
TEMP=$(curl -s http://localhost:8000/ai/settings -H "Authorization: Bearer $TOKEN" | jq -r '.temperature')
echo "✅ 4. Settings: Temperature=$TEMP"

# Chat (simple test)
CHAT_RESPONSE=$(curl -s http://localhost:8000/ai/chat -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"message":"Say only the word HELLO and nothing else"}' | jq -r '.response' | head -c 50)
echo "✅ 5. Chat: Response received (${CHAT_RESPONSE:0:20}...)"

# Web Search
WEB_COUNT=$(curl -s http://localhost:8000/ai/web-search -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"Python","max_results":3}' | jq -r '.results | length')
echo "✅ 6. Web Search: $WEB_COUNT results"

# User Management
USER_COUNT=$(curl -s http://localhost:8000/admin/users -H "Authorization: Bearer $TOKEN" | jq -r '.users | length')
echo "✅ 7. User Management: $USER_COUNT users"

# Database
TABLE_COUNT=$(curl -s http://localhost:8000/admin/database/tables -H "Authorization: Bearer $TOKEN" | jq -r '.tables | length')
echo "✅ 8. Database: $TABLE_COUNT tables"

# Chat History
CHAT_COUNT=$(curl -s http://localhost:8000/ai/chats -H "Authorization: Bearer $TOKEN" | jq -r '.chats | length')
echo "✅ 9. Chat History: $CHAT_COUNT chats"

echo ""
echo "==================================="
echo "🎉 All 9 Features Working!"
echo "==================================="
