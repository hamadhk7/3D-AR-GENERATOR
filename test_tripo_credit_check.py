#!/usr/bin/env python3
"""
Script to check Tripo3D credit information and try different approaches.
"""

import requests
import json

API_KEY = "tsk_1dZGrZJGhPjbZxU30svAeON8mPK41dkBo9I2DjKudx7"
BASE_URL = "https://api.tripo3d.ai/v2/openapi"

def check_credit_info():
    """Try to get credit information from various endpoints."""
    print("💰 Checking credit information...")
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Try different credit-related endpoints
    endpoints = [
        "/user/balance",
        "/user/credits", 
        "/user/usage",
        "/user/account",
        "/api/user/balance",
        "/api/user/credits",
        "/api/balance",
        "/api/credits",
        "/v2/user/balance",
        "/v2/user/credits",
        "/v2/balance",
        "/v2/credits"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=5)
            print(f"📊 {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.text[:200]}...")
            elif response.status_code == 404:
                print(f"❌ {endpoint}: Not found")
            else:
                print(f"❌ {endpoint}: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")

def test_free_generation():
    """Test if there are any free generation options."""
    print("\n🎁 Testing free generation options...")
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test different generation types that might be free
    generation_types = [
        {"type": "text_to_model", "prompt": "A red sports car", "free": True},
        {"type": "text_to_model", "prompt": "A red sports car", "trial": True},
        {"type": "text_to_model", "prompt": "A red sports car", "demo": True},
        {"type": "text_to_model", "prompt": "A red sports car", "quality": "low"},
        {"type": "text_to_model", "prompt": "A red sports car", "quality": "basic"},
        {"type": "text_to_model", "prompt": "A red sports car", "texture": False},
        {"type": "text_to_model", "prompt": "A red sports car", "pbr": False}
    ]
    
    for i, payload in enumerate(generation_types):
        try:
            response = requests.post(f"{BASE_URL}/task", headers=headers, json=payload, timeout=10)
            print(f"📊 Free option {i+1}: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Success: {response.text[:100]}...")
            elif response.status_code == 403:
                print(f"❌ Still no credits: {response.text[:100]}...")
            else:
                print(f"❌ Error: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Exception: {e}")

def test_different_api_versions():
    """Test different API versions to see if they have different credit systems."""
    print("\n🔄 Testing different API versions...")
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Test different API versions
    api_versions = [
        "https://api.tripo3d.ai/v1",
        "https://api.tripo3d.ai/v2", 
        "https://api.tripo3d.ai/v3",
        "https://platform.tripo3d.ai/api/v1",
        "https://platform.tripo3d.ai/api/v2"
    ]
    
    for version in api_versions:
        print(f"\n🌐 Testing {version}")
        
        # Test health endpoint
        try:
            response = requests.get(f"{version}/health", headers=headers, timeout=5)
            print(f"  📊 /health: {response.status_code}")
        except Exception as e:
            print(f"  ❌ /health: Error - {e}")
        
        # Test task creation
        try:
            payload = {"type": "text_to_model", "prompt": "A red sports car"}
            response = requests.post(f"{version}/task", headers=headers, json=payload, timeout=10)
            print(f"  📊 POST /task: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ Success: {response.text[:100]}...")
            elif response.status_code == 403:
                print(f"  ❌ No credits: {response.text[:100]}...")
            else:
                print(f"  ❌ Error: {response.text[:100]}...")
        except Exception as e:
            print(f"  ❌ POST /task: Error - {e}")

def check_web_interface_credits():
    """Provide instructions for checking web interface credits."""
    print("\n🌐 Web Interface Credit Check:")
    print("1. Go to https://platform.tripo3d.ai")
    print("2. Log in to your account")
    print("3. Look for 'Credits', 'Balance', or 'Billing' section")
    print("4. Check if there are different types of credits:")
    print("   - API Credits")
    print("   - Web Interface Credits") 
    print("   - Trial Credits")
    print("   - Free Credits")
    print("5. Look for API key management section")
    print("6. Check if credits are allocated to specific API keys")

def main():
    """Run all credit-related tests."""
    check_credit_info()
    test_free_generation()
    test_different_api_versions()
    check_web_interface_credits()

if __name__ == "__main__":
    main() 