#!/usr/bin/env python3
import requests

BASE_URL = "http://localhost:8000"

# Login
r = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = r.json()["access_token"]
print(f"Token: {token[:20]}...")

# Test chat
headers = {"Authorization": f"Bearer {token}"}
r = requests.post(f"{BASE_URL}/ai/chat", headers=headers, json={
    "message": "Say only 'Hello World' and nothing else."
})

print(f"Status: {r.status_code}")
print(f"Response: {r.text}")

if r.status_code == 200:
    data = r.json()
    print(f"Keys: {data.keys()}")
    print(f"Response text: {data.get('response', 'NO RESPONSE KEY')[:100]}")
