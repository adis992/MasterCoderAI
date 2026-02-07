#!/usr/bin/env python3
"""Test if login returns token with 'id' field"""
import requests
import json
import jwt

API_URL = "http://localhost:8000"

# Login
print("🔐 Testing login...")
response = requests.post(f"{API_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})

if response.status_code != 200:
    print(f"❌ Login failed: {response.text}")
    exit(1)

token = response.json()["access_token"]
print(f"✅ Token received: {token[:50]}...")

# Decode token WITHOUT verification (just to see payload)
try:
    # Decode without verification to see what's inside
    decoded = jwt.decode(token, options={"verify_signature": False})
    print("\n📦 TOKEN PAYLOAD:")
    print(json.dumps(decoded, indent=2))
    
    print("\n🔍 CHECKING REQUIRED FIELDS:")
    print(f"  'id' field: {decoded.get('id')} {'✅' if decoded.get('id') else '❌ MISSING'}")
    print(f"  'sub' field: {decoded.get('sub')} {'✅' if decoded.get('sub') else '❌ MISSING'}")
    print(f"  'is_admin' field: {decoded.get('is_admin')} {'✅' if 'is_admin' in decoded else '❌ MISSING'}")
    
except Exception as e:
    print(f"❌ Failed to decode token: {e}")
