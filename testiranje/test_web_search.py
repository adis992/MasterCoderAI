#!/usr/bin/env python3
"""
Test Web Search funkcionalnosti
"""
import requests
import json

# API endpoint
API_URL = "http://172.16.20.104:8000"

# Login credentials (admin)
USERNAME = "admin"
PASSWORD = "admin123"

def test_web_search():
    """Test Web Search endpoint"""
    print("🧪 Testing Web Search...")
    
    # 1. Login
    print("\n1️⃣ Logging in...")
    login_data = {"username": USERNAME, "password": PASSWORD}
    login_res = requests.post(f"{API_URL}/auth/login", json=login_data)
    
    if login_res.status_code != 200:
        print(f"❌ Login failed: {login_res.text}")
        return
    
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ Logged in! Token: {token[:20]}...")
    
    # 2. Test Web Search
    print("\n2️⃣ Testing Web Search...")
    search_query = "Python programming tutorial"
    search_data = {"query": search_query}
    
    search_res = requests.post(
        f"{API_URL}/ai/web-search", 
        json=search_data, 
        headers=headers
    )
    
    if search_res.status_code != 200:
        print(f"❌ Web Search failed: {search_res.text}")
        return
    
    results = search_res.json()
    print(f"✅ Web Search successful!")
    print(f"\n📊 Search Results for: '{results['query']}'")
    print(f"⏱️ Timestamp: {results['timestamp']}")
    print(f"📝 Results count: {len(results['results'])}\n")
    
    # 3. Display results
    for idx, result in enumerate(results["results"], 1):
        print(f"{idx}. {result['title']}")
        print(f"   📝 {result['snippet'][:100]}...")
        print(f"   🔗 {result['link']}\n")
    
    print("\n✅ ALL TESTS PASSED!")

if __name__ == "__main__":
    test_web_search()
