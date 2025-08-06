#!/usr/bin/env python3
"""
Debug script to test the API and see what's happening
"""

import requests
import json
import os

def debug_api():
    """Debug the API to see what's happening"""
    
    print("Debugging API...")
    print("=" * 50)
    
    # Test the API
    try:
        response = requests.get("http://localhost:5000/api/models")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Total Models: {data.get('total')}")
            
            models = data.get('models', [])
            print(f"Models returned: {len(models)}")
            
            for i, model in enumerate(models):
                print(f"\nModel {i+1}:")
                print(f"  ID: {model.get('id')}")
                print(f"  Prompt: {model.get('prompt')}")
                print(f"  Created: {model.get('created_at')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error testing API: {e}")
    
    print("\n" + "=" * 50)
    print("Testing file path resolution...")
    
    # Test the file path resolution
    import sys
    sys.path.insert(0, '.')
    
    # Simulate the API's file path resolution
    api_file_path = os.path.join(os.path.dirname('src/web/routes/api.py'), '..', 'data', 'demo_models.json')
    print(f"API calculated path: {api_file_path}")
    
    # Test if this path exists
    if os.path.exists(api_file_path):
        print(f"✅ Path exists: {api_file_path}")
    else:
        print(f"❌ Path does not exist: {api_file_path}")
    
    # Test the actual path
    actual_path = "src/data/demo_models.json"
    print(f"Actual path: {actual_path}")
    if os.path.exists(actual_path):
        print(f"✅ Actual path exists: {actual_path}")
    else:
        print(f"❌ Actual path does not exist: {actual_path}")
    
    # Test absolute path
    abs_path = os.path.abspath(actual_path)
    print(f"Absolute path: {abs_path}")
    if os.path.exists(abs_path):
        print(f"✅ Absolute path exists: {abs_path}")
    else:
        print(f"❌ Absolute path does not exist: {abs_path}")

if __name__ == "__main__":
    debug_api() 