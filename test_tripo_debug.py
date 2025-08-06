#!/usr/bin/env python3
"""
Debug script to test different Tripo3D API configurations.
"""

import requests
import json

API_KEY = ""

def test_different_endpoints():
    """Test various API endpoints and configurations."""
    print("🔍 Debugging Tripo3D API configuration...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    
    # Test different base URLs
    base_urls = [
        "https://api.tripo3d.ai/v2/openapi",
        "https://api.tripo3d.ai/v2",
        "https://api.tripo3d.ai/v1",
        "https://platform.tripo3d.ai/api/v2",
        "https://platform.tripo3d.ai/api/v1"
    ]
    
    # Test different authentication headers
    auth_methods = [
        {'Authorization': f'Bearer {API_KEY}'},
        {'Authorization': f'Token {API_KEY}'},
        {'X-API-Key': API_KEY},
        {'api-key': API_KEY}
    ]
    
    for base_url in base_urls:
        print(f"\n🌐 Testing base URL: {base_url}")
        
        for i, headers in enumerate(auth_methods):
            headers['Content-Type'] = 'application/json'
            print(f"  🔐 Auth method {i+1}: {list(headers.keys())[0]}")
            
            # Test 1: Simple GET request
            try:
                response = requests.get(f"{base_url}/health", headers=headers, timeout=5)
                print(f"    📊 /health: {response.status_code}")
                if response.status_code == 200:
                    print(f"    ✅ Success: {response.text[:100]}...")
                elif response.status_code == 401:
                    print(f"    ❌ Auth failed")
                elif response.status_code == 404:
                    print(f"    ❌ Not found")
                else:
                    print(f"    ❌ Error: {response.text[:100]}...")
            except Exception as e:
                print(f"    ❌ Exception: {e}")
            
            # Test 2: Task creation
            try:
                payload = {
                    "type": "text_to_model",
                    "prompt": "A red sports car"
                }
                response = requests.post(f"{base_url}/task", headers=headers, json=payload, timeout=10)
                print(f"    📊 POST /task: {response.status_code}")
                if response.status_code == 200:
                    print(f"    ✅ Success: {response.text[:100]}...")
                elif response.status_code == 403:
                    print(f"    ❌ No credits: {response.text[:100]}...")
                elif response.status_code == 401:
                    print(f"    ❌ Auth failed")
                else:
                    print(f"    ❌ Error: {response.text[:100]}...")
            except Exception as e:
                print(f"    ❌ Exception: {e}")

def test_credit_endpoints():
    """Test specific credit-related endpoints."""
    print("\n💰 Testing credit-related endpoints...")
    
    base_url = "https://api.tripo3d.ai/v2/openapi"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test different credit endpoints
    credit_endpoints = [
        "/balance",
        "/credits", 
        "/usage",
        "/account",
        "/user",
        "/billing",
        "/subscription"
    ]
    
    for endpoint in credit_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=5)
            print(f"📊 {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.text[:200]}...")
            elif response.status_code == 404:
                print(f"❌ {endpoint}: Not found")
            else:
                print(f"❌ {endpoint}: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

def test_different_payloads():
    """Test different request payloads."""
    print("\n📦 Testing different request payloads...")
    
    base_url = "https://api.tripo3d.ai/v2/openapi"
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test different payload formats
    payloads = [
        {"type": "text_to_model", "prompt": "A red sports car"},
        {"request_type": "text_to_model", "prompt": "A red sports car"},
        {"prompt": "A red sports car", "type": "text_to_model"},
        {"text": "A red sports car", "type": "text_to_model"},
        {"input": "A red sports car", "type": "text_to_model"}
    ]
    
    for i, payload in enumerate(payloads):
        try:
            response = requests.post(f"{base_url}/task", headers=headers, json=payload, timeout=10)
            print(f"📊 Payload {i+1}: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Success: {response.text[:100]}...")
            elif response.status_code == 403:
                print(f"❌ No credits: {response.text[:100]}...")
            else:
                print(f"❌ Error: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Exception: {e}")

def main():
    """Run all debug tests."""
    test_different_endpoints()
    test_credit_endpoints()
    test_different_payloads()

if __name__ == "__main__":
    main() 