#!/usr/bin/env python3
"""
Test script to directly call Tripo API endpoints
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_tripo_direct():
    """Test direct Tripo API calls"""
    
    print("Testing Direct Tripo API Calls...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('TRIPO_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"Using API key: {api_key[:10]}...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    base_url = "https://api.tripo3d.ai/v2/openapi"
    
    # Test different endpoints
    endpoints = [
        "/task/health",
        "/credits",
        "/billing", 
        "/account",
        "/user",
        "/balance",
        "/wallet"
    ]
    
    for endpoint in endpoints:
        try:
            print(f"\nTesting endpoint: {endpoint}")
            response = requests.get(
                f"{base_url}{endpoint}",
                headers=headers,
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Success: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"✅ Success: {response.text[:200]}...")
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_tripo_direct() 