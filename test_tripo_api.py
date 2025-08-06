#!/usr/bin/env python3
"""
Test script to find the correct Tripo3D API endpoints.
"""

import requests
import json

API_KEY = "tcli_b676fa73dcff44d1ad55de03bd2a9c2e"
BASE_URL = "https://api.tripo3d.ai/v2"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            print(f"❌ Unknown method: {method}")
            return
            
        print(f"\n🔍 Testing: {method} {endpoint}")
        print(f"📊 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                content = response.json()
                print(f"✅ JSON Response: {json.dumps(content, indent=2)}")
            except:
                print(f"📄 Text Response: {response.text[:500]}...")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Test various API endpoints."""
    print("🔍 Testing Tripo3D API endpoints...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Test correct Tripo API endpoints
    endpoints = [
        # Task endpoints (correct Tripo API)
        ("/task", "POST", {"request_type": "text_to_model", "prompt": "red sports car"}),
        ("/task/123", "GET"),  # Test task status
        
        # Alternative endpoint patterns
        ("/tasks", "POST", {"request_type": "text_to_model", "prompt": "red sports car"}),
        ("/tasks/123", "GET"),
        ("/jobs", "POST", {"request_type": "text_to_model", "prompt": "red sports car"}),
        ("/jobs/123", "GET"),
        ("/generate", "POST", {"request_type": "text_to_model", "prompt": "red sports car"}),
        
        # Health/status endpoints
        ("/health", "GET"),
        ("/status", "GET"),
        ("/ping", "GET"),
        
        # Account endpoints
        ("/account", "GET"),
        ("/user", "GET"),
        ("/me", "GET"),
    ]
    
    for endpoint, method, *args in endpoints:
        data = args[0] if args else None
        test_endpoint(endpoint, method, data)
        
    print("\n🎯 Next steps:")
    print("1. Check the responses above for working endpoints")
    print("2. Look for API documentation on the Tripo3D platform")
    print("3. Check for SDK or code examples")
    print("4. Contact Tripo3D support for API documentation")

if __name__ == "__main__":
    main() 