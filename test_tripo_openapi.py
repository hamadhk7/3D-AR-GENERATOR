#!/usr/bin/env python3
"""
Test script to directly test Tripo3D OpenAPI endpoints.
"""

import requests
import json

API_KEY = ""
BASE_URL = "https://api.tripo3d.ai/v2/openapi"

def test_openapi_endpoints():
    """Test various OpenAPI endpoints."""
    print("🔍 Testing Tripo3D OpenAPI endpoints...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🌐 Base URL: {BASE_URL}")
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/task/health", headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Health check successful: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Account info (if available)
    print("\n2️⃣ Testing account info...")
    try:
        response = requests.get(f"{BASE_URL}/account", headers=headers, timeout=10)
        print(f"📊 Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Account info: {response.json()}")
        else:
            print(f"❌ Account info failed: {response.text}")
    except Exception as e:
        print(f"❌ Account info error: {e}")
    
    # Test 3: Create a task
    print("\n3️⃣ Testing task creation...")
    try:
        payload = {
            "type": "text_to_model",
            "prompt": "A red sports car",
            "model_version": "v2.5-20250123"
        }
        
        response = requests.post(f"{BASE_URL}/task", headers=headers, json=payload, timeout=30)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("code") == 0:
                task_id = response_data["data"]["task_id"]
                print(f"✅ Task created successfully: {task_id}")
                
                # Test 4: Get task status
                print(f"\n4️⃣ Testing task status for: {task_id}")
                status_response = requests.get(f"{BASE_URL}/task/{task_id}", headers=headers, timeout=10)
                print(f"📊 Status: {status_response.status_code}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"✅ Task status: {status_data}")
                else:
                    print(f"❌ Task status failed: {status_response.text}")
            else:
                print(f"❌ Task creation failed: {response_data}")
        else:
            print(f"❌ Task creation failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Task creation error: {e}")
    
    # Test 5: Check for any available endpoints
    print("\n5️⃣ Testing other endpoints...")
    endpoints_to_test = [
        "/user",
        "/balance", 
        "/credits",
        "/usage",
        "/models",
        "/tasks"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            print(f"📊 {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.json()}")
            elif response.status_code == 404:
                print(f"❌ {endpoint}: Not found")
            else:
                print(f"❌ {endpoint}: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

def main():
    """Run the OpenAPI test."""
    test_openapi_endpoints()

if __name__ == "__main__":
    main() 