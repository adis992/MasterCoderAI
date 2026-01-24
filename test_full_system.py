#!/usr/bin/env python3
"""Comprehensive test: Load model + Chat"""
import requests
import json
import time

API_URL = "http://localhost:8000"

# Step 1: Login
print("🔐 Step 1: Logging in...")
login_resp = requests.post(
    f"{API_URL}/auth/login",
    json={"username": "admin", "password": "admin"}
)
token = login_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Logged in! Token: {token[:30]}...")

# Step 2: Check current model
print("\n📦 Step 2: Checking model status...")
model_status = requests.get(f"{API_URL}/ai/models/current", headers=headers).json()
print(f"Model status: {model_status}")

# Step 3: Load model if not loaded
if model_status.get("status") != "loaded":
    print("\n⏳ Step 3: Loading model DarkIdol-Lama3.1.gguf...")
    print("This will take ~1-2 minutes for the 30GB model...")
    
    try:
        load_resp = requests.post(
            f"{API_URL}/ai/models/load",
            headers=headers,
            json={"model_name": "DarkIdol-Lama3.1.gguf"},
            timeout=600  # 10 minute timeout
        )
        print(f"✅ Model loaded: {load_resp.json()}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        exit(1)
else:
    print("✅ Model already loaded!")

# Step 4: Wait a bit for model to be ready
print("\n⏳ Waiting 2 seconds for model to be ready...")
time.sleep(2)

# Step 5: Send test chat message
print("\n💬 Step 4: Sending test message...")
try:
    chat_resp = requests.post(
        f"{API_URL}/ai/chat",
        headers=headers,
        json={
            "message": "Hello! Say only 'Hi there!' and nothing else.",
            "uncensored": True,
            "save_to_history": True
        },
        timeout=60  # 60 second timeout for generation
    )
    
    if chat_resp.status_code == 200:
        response_data = chat_resp.json()
        print(f"\n✅ Chat successful!")
        print(f"📝 User message: Hello! Say only 'Hi there!' and nothing else.")
        print(f"🤖 AI response: {response_data.get('response', 'No response')}")
    else:
        print(f"❌ Chat failed: {chat_resp.status_code}")
        print(f"Error: {chat_resp.text}")
except requests.exceptions.Timeout:
    print("❌ Chat request timed out after 60 seconds")
except Exception as e:
    print(f"❌ Chat error: {e}")

# Step 6: Check chat history
print("\n📚 Step 5: Checking chat history...")
chats = requests.get(f"{API_URL}/user/chats", headers=headers).json()
print(f"Total chats in history: {len(chats)}")
if chats:
    print(f"Latest chat: {chats[-1]}")

print("\n✅ Test complete!")
