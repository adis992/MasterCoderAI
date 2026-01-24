#!/usr/bin/env python3
"""Direct chat test - bypass frontend"""
import requests
import json
import time

API = 'http://127.0.0.1:8000'

print("=" * 60)
print("🧪 DIRECT CHAT TEST (NO FRONTEND)")
print("=" * 60)

# 1. Login
print("\n[1/4] Login...")
r = requests.post(f'{API}/auth/login', json={'username': 'admin', 'password': 'admin'})
if r.status_code != 200:
    print(f"❌ Login failed: {r.text}")
    exit(1)
token = r.json()['access_token']
print(f"✅ Token: {token[:30]}...")

headers = {'Authorization': f'Bearer {token}'}

# 2. Check model
print("\n[2/4] Check current model...")
r = requests.get(f'{API}/ai/models/current', headers=headers)
print(f"Model: {r.json()}")
if not r.json().get('model_name'):
    print("❌ No model loaded! Load it first.")
    exit(1)

# 3. Send chat message
print("\n[3/4] Sending chat message...")
print("Message: 'Hello, who are you?'")
start = time.time()

try:
    r = requests.post(
        f'{API}/ai/chat',
        json={'message': 'Hello, who are you?', 'save_to_history': True},
        headers=headers,
        timeout=120  # 2 min timeout
    )
    elapsed = time.time() - start
    
    print(f"\n⏱️  Response time: {elapsed:.1f}s")
    print(f"📊 Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"\n✅ SUCCESS!")
        print(f"📝 AI Response:\n{data['response']}")
        print(f"🤖 Model: {data['model_name']}")
    else:
        print(f"❌ Error: {r.text}")
        
except requests.Timeout:
    print(f"❌ TIMEOUT after {time.time() - start:.1f}s")
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "=" * 60)
