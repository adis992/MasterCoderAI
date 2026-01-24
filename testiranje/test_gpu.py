#!/usr/bin/env python3
import requests
import json

API = 'http://127.0.0.1:8000'

# Test GPU
print("=== GPU Info ===")
r = requests.get(f'{API}/ai/gpu')
print(json.dumps(r.json(), indent=2))

# Login
print("\n=== Login ===")
login = requests.post(f'{API}/auth/login', json={'username':'admin','password':'admin'})
token = login.json()['access_token']
print(f"Token: {token[:50]}...")

headers = {'Authorization': f'Bearer {token}'}

# Check current model
print("\n=== Current Model ===")
r = requests.get(f'{API}/ai/models/current', headers=headers)
print(json.dumps(r.json(), indent=2))

# Check models
print("\n=== Available Models ===")
r = requests.get(f'{API}/ai/models', headers=headers)
print(json.dumps(r.json(), indent=2))
