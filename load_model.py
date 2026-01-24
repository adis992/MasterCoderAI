#!/usr/bin/env python3
import requests
import json
import time

API = 'http://127.0.0.1:8000'

# Login
print("=== Login ===")
login = requests.post(f'{API}/auth/login', json={'username':'admin','password':'admin'})
token = login.json()['access_token']
print(f"Token: {token[:50]}...")

headers = {'Authorization': f'Bearer {token}'}

# Load model
print("\n=== Loading Model to GPU ===")
print("This will take 1-2 minutes for 30GB model...")
start = time.time()

r = requests.post(f'{API}/ai/models/load', 
                  json={'model_name': 'DarkIdol-Lama3.1.gguf'},
                  headers=headers,
                  timeout=600)
                  
elapsed = time.time() - start
print(f"Status: {r.status_code}")
print(f"Time: {elapsed:.1f}s")
print(f"Response: {json.dumps(r.json(), indent=2)}")

# Check GPU after loading
print("\n=== GPU After Loading ===")
r = requests.get(f'{API}/ai/gpu')
print(json.dumps(r.json(), indent=2))
