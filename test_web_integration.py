#!/usr/bin/env python3
"""
Test web server integration with API.
"""

import requests
import json
import time

def test_web_server_health():
    """Test web server health endpoint."""
    print("🔍 Testing Web Server Health...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Web server is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   Service: {data.get('service')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Web server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to web server: {e}")
        return False

def test_api_generation_endpoint():
    """Test the API generation endpoint."""
    print("\n🎨 Testing API Generation Endpoint...")
    
    try:
        # Test with a simple prompt
        test_data = {
            "prompt": "A simple red cube for testing"
        }
        
        response = requests.post(
            "http://localhost:5000/api/generate",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API generation endpoint working!")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            if data.get('job_id'):
                print(f"   Job ID: {data.get('job_id')}")
            return True
        else:
            print(f"❌ API generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ API generation test failed: {e}")
        return False

def test_models_listing():
    """Test the models listing endpoint."""
    print("\n📋 Testing Models Listing...")
    
    try:
        response = requests.get("http://localhost:5000/api/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Models listing working! Found {len(models)} models")
            return True
        else:
            print(f"❌ Models listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models listing test failed: {e}")
        return False

def test_credits_endpoint():
    """Test the credits endpoint."""
    print("\n💰 Testing Credits Endpoint...")
    
    try:
        response = requests.get("http://localhost:5000/api/credits", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Credits endpoint working!")
            print(f"   API Wallet: {data.get('api_wallet', 0)}")
            print(f"   Free Wallet: {data.get('free_wallet', 0)}")
            print(f"   Total Used: {data.get('total_used', 0)}")
            return True
        else:
            print(f"❌ Credits endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Credits test failed: {e}")
        return False

def main():
    """Run all web integration tests."""
    
    print("🌐 Web Server Integration Test")
    print("=" * 50)
    
    tests = [
        ("Web Server Health", test_web_server_health),
        ("API Generation", test_api_generation_endpoint),
        ("Models Listing", test_models_listing),
        ("Credits Endpoint", test_credits_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All web integration tests passed!")
        print("🚀 Your web server is fully functional and ready to use!")
        print("📱 You can now:")
        print("   - Visit http://localhost:5000 to use the web interface")
        print("   - Generate 3D models through the API")
        print("   - View models in the AR viewer")
    else:
        print("⚠️  Some web integration tests failed.")
        print("🔧 Make sure the web server is running on localhost:5000")

if __name__ == "__main__":
    main() 