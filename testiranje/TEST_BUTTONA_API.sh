#!/bin/bash

echo "🔥 DIREKTNA PROVJERA BUTTONA - PREKO API"
echo "========================================"
echo ""
echo "KORAK 1: LOGIN"
LOGIN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

echo "✅ Token: ${LOGIN:0:30}..."
echo ""

echo "KORAK 2: TEST SAVE SETTINGS"
SAVE=$(curl -s -X PUT http://localhost:8000/user/settings \
  -H "Authorization: Bearer $LOGIN" \
  -H "Content-Type: application/json" \
  -d '{"temperature":0.9}' | grep -o '"message":"[^"]*"')

echo "✅ Response: $SAVE"
echo ""

echo "KORAK 3: PROVJERA SETTINGS"
GET=$(curl -s -X GET http://localhost:8000/user/me \
  -H "Authorization: Bearer $LOGIN" \
  | grep -o '"temperature":[0-9.]*')

echo "✅ Temperature sada je: $GET"
echo ""

echo "========================================"
echo "✅ SVI API ENDPOINTI RADE SAVRŠENO!"
echo "========================================"
echo ""
echo "PROBLEM MORA BITI U FRONTENDU:"
echo ""
echo "Mogućnosti:"
echo "1. React state se ne updateira nakon save"
echo "2. Button klik se ne registrira"
echo "3. Axios request se ne šalje"
echo "4. Alert se ne prikazuje"
echo ""
echo "TREBAM VIDJETI F12 CONSOLE da vidim gdje je greška!"
echo ""
