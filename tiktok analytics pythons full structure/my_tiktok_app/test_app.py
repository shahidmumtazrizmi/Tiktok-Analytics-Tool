#!/usr/bin/env python3
"""
Test script for TikTok Analytics + RAG Chatbot
"""

import requests
import time
import sys

def test_app():
    """Test the application endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing TikTok Analytics + RAG Chatbot...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check: FAILED (Connection error: {e})")
        return False
    
    # Test home page
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Home page: PASSED")
        else:
            print(f"❌ Home page: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Home page: FAILED (Connection error: {e})")
    
    # Test chatbot page
    try:
        response = requests.get(f"{base_url}/chatbot", timeout=5)
        if response.status_code == 200:
            print("✅ Chatbot page: PASSED")
        else:
            print(f"❌ Chatbot page: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Chatbot page: FAILED (Connection error: {e})")
    
    # Test analytics API
    try:
        response = requests.get(f"{base_url}/api/analytics/trending-products", timeout=5)
        if response.status_code == 200:
            print("✅ Analytics API: PASSED")
            data = response.json()
            print(f"   Found {len(data.get('data', []))} products")
        else:
            print(f"❌ Analytics API: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Analytics API: FAILED (Connection error: {e})")
    
    # Test chat API
    try:
        chat_data = {
            "message": "How do I set up my TikTok Shop?",
            "session_id": "test-session"
        }
        response = requests.post(f"{base_url}/api/chat/send", json=chat_data, timeout=10)
        if response.status_code == 200:
            print("✅ Chat API: PASSED")
            data = response.json()
            print(f"   Response: {data.get('response', '')[:100]}...")
        else:
            print(f"❌ Chat API: FAILED (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat API: FAILED (Connection error: {e})")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print(f"📊 Dashboard: {base_url}")
    print(f"🤖 Chatbot: {base_url}/chatbot")
    print(f"📚 API Docs: {base_url}/docs")
    
    return True

if __name__ == "__main__":
    # Wait a bit for the app to start
    print("⏳ Waiting for app to start...")
    time.sleep(3)
    
    success = test_app()
    sys.exit(0 if success else 1) 