#!/usr/bin/env python3
"""Test chat sa fiksovanim user_id"""
import requests
import time

API = "http://localhost:8000"

# 1. Login
print("🔐 Login...")
login = requests.post(f"{API}/auth/login", json={"username": "admin", "password": "admin123"})
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Token: {token[:30]}...")

# 2. Check model
print("\n📦 Checking model status...")
status = requests.get(f"{API}/ai/models/current", headers=headers).json()
print(f"Status: {status}")

# 3. Load model if needed
if status.get("status") != "loaded":
    print("\n⏳ Loading model (background)...")
    load_resp = requests.post(
        f"{API}/ai/models/load",
        headers=headers,
        json={"model_name": "DarkIdol-Lama3.1.gguf"}
    )
    print(f"Load started: {load_resp.json()}")
    
    # Wait for loading
    print("⏳ Waiting for model to load (checking every 5s)...")
    for i in range(30):  # Max 2.5 minutes
        time.sleep(5)
        status = requests.get(f"{API}/ai/models/current", headers=headers).json()
        print(f"  [{i*5}s] Status: {status.get('status')}")
        if status.get("status") == "loaded":
            print("✅ Model loaded!")
            break
    else:
        print("❌ Timeout waiting for model")
        exit(1)
else:
    print("✅ Model already loaded!")

# 4. Test chat
print("\n💬 Testing chat...")
chat_resp = requests.post(
    f"{API}/ai/chat",
    headers=headers,
    json={
        "message": "Say only 'Hello!' and nothing else.",
        "save_to_history": True
    },
    timeout=60
)

if chat_resp.status_code == 200:
    data = chat_resp.json()
    print(f"✅ Chat successful!")
    print(f"📝 Message: {data.get('message')}")
    print(f"🤖 Response: {data.get('response')}")
    print(f"💾 Saved: {data.get('saved')}")
else:
    print(f"❌ Chat failed: {chat_resp.status_code}")
    print(f"Error: {chat_resp.text}")

# 5. Check history
print("\n📚 Checking chat history...")
history = requests.get(f"{API}/user/chats", headers=headers).json()
print(f"Total chats: {len(history)}")
if history:
    print(f"Latest: {history[-1]}")
