#!/usr/bin/env python3
"""Test JWT token creation and parsing"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Simulate token creation (same as login)
user_data = {
    "sub": "admin",
    "id": 1,
    "is_admin": True
}

to_encode = user_data.copy()
expire = datetime.utcnow() + timedelta(minutes=60*24)
to_encode.update({"exp": expire})
token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

print("=" * 60)
print("🔑 CREATED TOKEN:")
print(token)
print()

# Parse token (same as verify_token)
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print("📦 DECODED PAYLOAD:")
print(f"  Full payload: {payload}")
print(f"  sub: {payload.get('sub')}")
print(f"  id: {payload.get('id')}")
print(f"  is_admin: {payload.get('is_admin')}")
print()

# Build user object (same as verify_token)
username = payload.get("sub")
user_id = payload.get("id")
is_admin = payload.get("is_admin", False)
current_user = {"username": username, "id": user_id, "is_admin": is_admin}

print("👤 CURRENT_USER OBJECT:")
print(f"  Full object: {current_user}")
print(f"  current_user['id']: {current_user['id']}")
print(f"  Type of id: {type(current_user['id'])}")
print("=" * 60)
