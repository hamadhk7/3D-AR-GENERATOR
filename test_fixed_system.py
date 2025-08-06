#!/usr/bin/env python3
"""
Test script to verify the fixed 3D AR demo system
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_system():
    print("🧪 Testing Fixed 3D AR Demo System")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Generate a new model
    print("\n2. Testing model generation...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json={"prompt": "red sports car"}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Model generation successful")
                print(f"   Model ID: {data.get('model_id')}")
                print(f"   Message: {data.get('message')}")
            else:
                print("❌ Model generation failed")
        else:
            print(f"❌ Model generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model generation error: {e}")
    
    # Test 3: Get models list
    print("\n3. Testing models list...")
    try:
        response = requests.get(f"{BASE_URL}/api/models")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                models = data.get('models', [])
                print(f"✅ Found {len(models)} models")
                for model in models:
                    print(f"   - {model['prompt']} (ID: {model['id']})")
            else:
                print("❌ Failed to get models list")
        else:
            print(f"❌ Models list failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Models list error: {e}")
    
    # Test 4: Get specific model
    print("\n4. Testing specific model retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/api/models/demo_model_1754427911")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                model = data.get('model')
                print(f"✅ Retrieved model: {model['prompt']}")
                print(f"   Format: {model['format']}")
                print(f"   Quality: {model['quality']}")
            else:
                print("❌ Failed to get specific model")
        else:
            print(f"❌ Specific model failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Specific model error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 System test completed!")
    print("\n📝 Next steps:")
    print("1. Open http://localhost:5000/ in your browser")
    print("2. Go to 'All Models' to see your generated models")
    print("3. Click 'View' on any model to see the details")
    print("4. Try generating more models!")

if __name__ == "__main__":
    test_system() 