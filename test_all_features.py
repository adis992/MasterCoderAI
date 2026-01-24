#!/usr/bin/env python3
"""Comprehensive feature test for MasterCoderAI v2.0.0"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_feature(name, func):
    """Test wrapper"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"{'='*60}")
    try:
        result = func()
        print(f"✅ PASS: {name}")
        return True
    except Exception as e:
        print(f"❌ FAIL: {name}")
        print(f"   Error: {str(e)}")
        return False

def test_backend_health():
    """1. Backend Health Check"""
    r = requests.get(f"{BASE_URL}/system/health")
    assert r.status_code == 200
    data = r.json()
    print(f"   Status: {data['status']}")
    print(f"   Database: {data['database']}")
    return data

def test_authentication():
    """2. Authentication (admin login)"""
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "admin",
        "password": "admin123"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    print(f"   Token: {token[:50]}...")
    return token

def test_gpu_info(token):
    """3. GPU Information"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/system/gpu", headers=headers)
    assert r.status_code == 200
    data = r.json()
    if data["count"] > 0:
        for gpu in data["gpus"]:
            print(f"   GPU {gpu['id']}: {gpu['name']} ({gpu['memory_used']}/{gpu['memory_total']} MB)")
    return data

def test_model_status(token):
    """4. Model Status"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/ai/model/status", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print(f"   Loaded: {data['loaded']}")
    if data["loaded"]:
        print(f"   Model: {data['model_name']}")
    return data

def test_settings(token):
    """5. AI Settings"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/ai/settings", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print(f"   Temperature: {data.get('temperature', 'N/A')}")
    print(f"   Max Tokens: {data.get('max_tokens', 'N/A')}")
    print(f"   Web Search: {data.get('web_search_enabled', False)}")
    return data

def test_chat_simple(token):
    """6. Simple Chat (no web search)"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/ai/chat", headers=headers, json={
        "message": "Say only 'Hello World' and nothing else."
    })
    assert r.status_code == 200
    data = r.json()
    print(f"   Response: {data['response'][:100]}...")
    return data

def test_web_search(token):
    """7. Web Search"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/ai/web-search", headers=headers, json={
        "query": "Python programming",
        "max_results": 3
    })
    assert r.status_code == 200
    data = r.json()
    print(f"   Results: {len(data['results'])}")
    if data["results"]:
        print(f"   First: {data['results'][0]['title'][:50]}...")
    return data

def test_user_list(token):
    """8. User Management (admin only)"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print(f"   Users: {len(data['users'])}")
    for user in data["users"]:
        print(f"   - {user['username']} ({user['role']})")
    return data

def test_database_tables(token):
    """9. Database Tables"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/admin/database/tables", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print(f"   Tables: {', '.join(data['tables'])}")
    return data

def test_chat_history(token):
    """10. Chat History"""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/ai/chats", headers=headers)
    assert r.status_code == 200
    data = r.json()
    print(f"   Total Chats: {len(data['chats'])}")
    return data

# Run all tests
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 MasterCoderAI v2.0.0 - Complete Feature Test")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    token = None
    
    # Test 1: Health
    results.append(test_feature("Backend Health", test_backend_health))
    
    # Test 2: Auth
    try:
        token = test_feature("Authentication", test_authentication)
    except:
        print("\n❌ Authentication failed - cannot continue")
        exit(1)
    
    # Test 3-10 (require token)
    if token:
        results.append(test_feature("GPU Information", lambda: test_gpu_info(token)))
        results.append(test_feature("Model Status", lambda: test_model_status(token)))
        results.append(test_feature("AI Settings", lambda: test_settings(token)))
        results.append(test_feature("Simple Chat", lambda: test_chat_simple(token)))
        results.append(test_feature("Web Search", lambda: test_web_search(token)))
        results.append(test_feature("User Management", lambda: test_user_list(token)))
        results.append(test_feature("Database Tables", lambda: test_database_tables(token)))
        results.append(test_feature("Chat History", lambda: test_chat_history(token)))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is fully operational.")
    else:
        print(f"\n⚠️ Some tests failed. Check logs above.")
    
    print("="*60 + "\n")
