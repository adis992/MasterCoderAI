#!/usr/bin/env python3
"""Test chat endpoint response structure"""
import requests
import jwt
import json

# Generate token
token = jwt.encode(
    {"sub": "admin", "id": 1, "is_admin": True},
    "your-secret-key-change-this-in-production",
    algorithm="HS256"
)

print("🔑 Token:", token[:50], "...")

# Test chat
url = "http://localhost:8000/ai/chat"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
data = {
    "message": "Hello, test message!",
    "save_to_history": False
}

print(f"\n📡 Sending POST to {url}")
print(f"📦 Data: {data}")

try:
    response = requests.post(url, headers=headers, json=data, timeout=60)
    print(f"\n✅ Status: {response.status_code}")
    print(f"\n📄 Response JSON:")
    print(json.dumps(response.json(), indent=2))
    
    # Check if response field exists
    resp_data = response.json()
    if "response" in resp_data:
        print(f"\n🟢 RESPONSE FIELD EXISTS: {resp_data['response'][:100]}...")
    else:
        print(f"\n🔴 RESPONSE FIELD MISSING! Available fields: {list(resp_data.keys())}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
