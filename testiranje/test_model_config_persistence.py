#!/usr/bin/env python3
"""
🧪 TEST MODEL CONFIG SAVE/LOAD PERSISTENCE
Tests that model configuration actually saves and loads correctly
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def login():
    """Get admin JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return None
    
    token = response.json().get("access_token")
    print(f"✅ Login successful - Token: {token[:20]}...")
    return token

def save_config(token):
    """Save model configuration"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test configuration with specific values
    config = {
        "capabilities": {
            "code_generation": {"enabled": True},
            "code_review": {"enabled": False},
            "documentation": {"enabled": True},
            "testing": {"enabled": True},
            "debugging": {"enabled": False}
        },
        "capability_settings": {
            "code_style": "google",
            "max_tokens": 2048,
            "temperature": 0.7
        },
        "agent_preferences": {
            "verbose": True,
            "auto_format": False
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/user/model-config", 
        json=config,
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Config save failed: {response.text}")
        return False
    
    print(f"✅ Config saved successfully")
    return True

def load_config(token):
    """Load model configuration"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(
        f"{BASE_URL}/user/model-config",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Config load failed: {response.text}")
        return None
    
    data = response.json()
    config = data.get("config", {})  # Extract config from wrapper
    print(f"✅ Config loaded successfully")
    return config

def verify_config(loaded_config):
    """Verify loaded config matches saved config"""
    print("\n📋 VERIFYING CONFIG DATA:")
    
    # Check capabilities
    caps = loaded_config.get("capabilities", {})
    print(f"  - code_generation: {caps.get('code_generation', {}).get('enabled')}")
    print(f"  - code_review: {caps.get('code_review', {}).get('enabled')}")
    print(f"  - documentation: {caps.get('documentation', {}).get('enabled')}")
    print(f"  - testing: {caps.get('testing', {}).get('enabled')}")
    print(f"  - debugging: {caps.get('debugging', {}).get('enabled')}")
    
    # Check settings
    settings = loaded_config.get("capability_settings", {})
    print(f"\n  - code_style: {settings.get('code_style')}")
    print(f"  - max_tokens: {settings.get('max_tokens')}")
    print(f"  - temperature: {settings.get('temperature')}")
    
    # Check preferences
    prefs = loaded_config.get("agent_preferences", {})
    print(f"\n  - verbose: {prefs.get('verbose')}")
    print(f"  - auto_format: {prefs.get('auto_format')}")
    
    # Validation
    expected_caps = {
        "code_generation": True,
        "code_review": False,
        "documentation": True,
        "testing": True,
        "debugging": False
    }
    
    all_correct = True
    for key, expected_value in expected_caps.items():
        actual_value = caps.get(key, {}).get('enabled')
        if actual_value != expected_value:
            print(f"\n❌ MISMATCH: {key} - Expected: {expected_value}, Got: {actual_value}")
            all_correct = False
    
    if settings.get('code_style') != 'google':
        print(f"\n❌ MISMATCH: code_style - Expected: google, Got: {settings.get('code_style')}")
        all_correct = False
    
    if settings.get('max_tokens') != 2048:
        print(f"\n❌ MISMATCH: max_tokens - Expected: 2048, Got: {settings.get('max_tokens')}")
        all_correct = False
    
    if settings.get('temperature') != 0.7:
        print(f"\n❌ MISMATCH: temperature - Expected: 0.7, Got: {settings.get('temperature')}")
        all_correct = False
    
    return all_correct

def main():
    print("=" * 60)
    print("🧪 MODEL CONFIG PERSISTENCE TEST")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1️⃣ STEP 1: Login...")
    token = login()
    if not token:
        return
    
    # Step 2: Save config
    print("\n2️⃣ STEP 2: Save model config...")
    if not save_config(token):
        return
    
    # Step 3: Wait a bit
    print("\n⏳ Waiting 2 seconds...")
    time.sleep(2)
    
    # Step 4: Load config
    print("\n3️⃣ STEP 3: Load model config...")
    loaded_config = load_config(token)
    if not loaded_config:
        return
    
    # Step 5: Verify
    print("\n4️⃣ STEP 4: Verify config matches...")
    if verify_config(loaded_config):
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Model config save/load works perfectly!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ FAILED! Model config data mismatch!")
        print("=" * 60)

if __name__ == "__main__":
    main()
