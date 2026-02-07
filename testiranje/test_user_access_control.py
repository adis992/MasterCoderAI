#!/usr/bin/env python3
"""
🧪 TEST USER BLOCKING BEFORE ADMIN SETUP
Tests that regular users cannot login until admin completes setup
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_user_login_when_not_ready():
    """Test user login when system not initialized"""
    print("\n1️⃣ TESTING USER LOGIN WHEN SYSTEM NOT READY...")
    
    # First, reset server initialization state
    admin_token = admin_login()
    if not admin_token:
        print("❌ Cannot get admin token")
        return False
    
    # Reset initialization
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(
        f"{BASE_URL}/system/reset-initialization",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Server initialization reset")
    else:
        print(f"⚠️ Could not reset: {response.text}")
    
    # Disable user access
    response = requests.post(
        f"{BASE_URL}/system/update-component-status",
        json={
            "component": "user_access",
            "status": "blocked",
            "message": "Admin setup in progress"
        },
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ User access disabled")
    else:
        print(f"⚠️ Could not disable user access: {response.text}")
    
    # Now try user login
    print("\n2️⃣ ATTEMPTING USER LOGIN...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "user",
        "password": "user123"
    })
    
    if response.status_code == 503:
        print("✅ USER LOGIN BLOCKED AS EXPECTED (503 Service Unavailable)")
        data = response.json()
        print(f"   Message: {data.get('detail')}")
        return True
    elif response.status_code == 200:
        print("❌ USER LOGIN SUCCEEDED - THIS SHOULD NOT HAPPEN!")
        return False
    else:
        print(f"⚠️ Unexpected response: {response.status_code} - {response.text}")
        return False

def test_user_login_when_ready():
    """Test user login when system is initialized"""
    print("\n3️⃣ TESTING USER LOGIN WHEN SYSTEM READY...")
    
    # Re-enable user access
    admin_token = admin_login()
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    response = requests.post(
        f"{BASE_URL}/system/mark-initialized",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ System marked as initialized")
    else:
        print(f"⚠️ Could not mark initialized: {response.text}")
    
    # Now try user login
    print("\n4️⃣ ATTEMPTING USER LOGIN NOW...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "user",
        "password": "user123"
    })
    
    if response.status_code == 200:
        print("✅ USER LOGIN SUCCESSFUL AS EXPECTED")
        token = response.json().get("access_token")
        print(f"   Token: {token[:20]}...")
        return True
    else:
        print(f"❌ USER LOGIN FAILED: {response.text}")
        return False

def admin_login():
    """Helper to get admin token"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    
    if response.status_code != 200:
        return None
    
    return response.json().get("access_token")

def main():
    print("=" * 70)
    print("🧪 USER ACCESS CONTROL TEST")
    print("=" * 70)
    
    # Test 1: User blocked when not ready
    test1_passed = test_user_login_when_not_ready()
    
    # Test 2: User allowed when ready
    test2_passed = test_user_login_when_ready()
    
    print("\n" + "=" * 70)
    if test1_passed and test2_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Users are correctly blocked until admin completes setup")
    else:
        print("❌ TESTS FAILED!")
        print(f"   Test 1 (Block when not ready): {'✅ PASS' if test1_passed else '❌ FAIL'}")
        print(f"   Test 2 (Allow when ready): {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print("=" * 70)

if __name__ == "__main__":
    main()
