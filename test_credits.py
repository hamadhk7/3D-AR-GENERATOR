#!/usr/bin/env python3
"""
Test script to check the credits endpoint
"""

import requests
import json

def test_credits():
    """Test the credits endpoint"""
    
    print("Testing Credits Endpoint...")
    print("=" * 50)
    
    try:
        # Test the credits endpoint
        response = requests.get("http://localhost:5000/api/credits")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Credits endpoint working")
            print(f"Source: {data.get('source', 'unknown')}")
            print(f"API Wallet: {data.get('api_wallet', 0)}")
            print(f"Free Wallet: {data.get('free_wallet', 0)}")
            print(f"Frozen: {data.get('frozen', 0)}")
            print(f"Note: {data.get('note', 'No note')}")
            
            if data.get('source') in ['real_tripo_api', 'user_account']:
                print("✅ Real Tripo account credits detected!")
            else:
                print("⚠️ Using demo credits")
                
        else:
            print("❌ Credits endpoint failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing credits: {e}")

if __name__ == "__main__":
    test_credits() 