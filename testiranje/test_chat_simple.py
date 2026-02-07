#!/usr/bin/env python3
"""Simple chat test script"""
import requests
import json

# Login
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = login_response.json()["access_token"]

print("✅ Logged in successfully")
print(f"Token: {token[:50]}...")

# Check model status
model_status = requests.get(
    "http://localhost:8000/ai/models/current",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"\n📦 Model Status: {model_status.json()}")

# Send chat message
print("\n💬 Sending chat message...")
chat_response = requests.post(
    "http://localhost:8000/ai/chat",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "message": "Tell me a very short joke about programming.",
        "uncensored": True
    },
    timeout=120
)

print(f"\n🤖 AI Response:")
print(json.dumps(chat_response.json(), indent=2))

# Check chats
chats = requests.get(
    "http://localhost:8000/user/chats",
    headers={"Authorization": f"Bearer {token}"}
)
print(f"\n💾 Total chats: {len(chats.json())}")
