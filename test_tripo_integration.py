#!/usr/bin/env python3
"""
Test script to verify Tripo API integration
"""

import requests
import json
import os
import sys

def test_tripo_integration():
    """Test the Tripo API integration"""
    
    print("Testing Tripo API Integration...")
    print("=" * 50)
    
    # Test 1: Check if API is accessible
    print("1. Testing API health...")
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API is not responding")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # Test 2: Check credits
    print("\n2. Testing credits system...")
    try:
        response = requests.get("http://localhost:5000/api/credits")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Credits available: {data.get('free_wallet', 0)}")
        else:
            print("❌ Credits check failed")
    except Exception as e:
        print(f"❌ Credits check error: {e}")
    
    # Test 3: Test model generation with Tripo API
    print("\n3. Testing Tripo API model generation...")
    try:
        generation_data = {
            "prompt": "A metallic coffee cup",
            "format": "glb",
            "quality": "high"
        }
        
        print("Sending generation request...")
        response = requests.post(
            "http://localhost:5000/api/generate",
            json=generation_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Model generation successful!")
                print(f"Model ID: {data.get('model', {}).get('id', 'N/A')}")
                print(f"Message: {data.get('message', 'N/A')}")
                
                # Test 4: Check if model appears in list
                print("\n4. Testing model listing...")
                list_response = requests.get("http://localhost:5000/api/models")
                if list_response.status_code == 200:
                    list_data = list_response.json()
                    models = list_data.get('models', [])
                    print(f"✅ Found {len(models)} models in list")
                    
                    # Look for our generated model
                    for model in models:
                        if model.get('id', '').startswith('tripo_'):
                            print(f"✅ Found Tripo model: {model.get('id')}")
                            print(f"   Prompt: {model.get('prompt')}")
                            print(f"   Status: {model.get('status')}")
                            break
                else:
                    print("❌ Model listing failed")
                    
            else:
                print("❌ Model generation failed")
                print(f"Error: {data.get('error', 'Unknown error')}")
        else:
            print("❌ Generation request failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Generation test error: {e}")
    
    print("\n" + "=" * 50)
    print("Integration test completed!")

if __name__ == "__main__":
    test_tripo_integration() 