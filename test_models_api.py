#!/usr/bin/env python3
"""
Test script to check the models API
"""

import requests
import json
import os

def test_models_api():
    """Test the models API endpoint"""
    
    print("Testing Models API...")
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
    print("Checking demo_models.json file...")
    
    # Check the demo models file
    demo_file = "src/data/demo_models.json"
    if os.path.exists(demo_file):
        print(f"File exists: {demo_file}")
        try:
            with open(demo_file, 'r') as f:
                data = json.load(f)
                print(f"Models in file: {len(data)}")
                
                # Show first few models
                for i, model in enumerate(data[:3]):
                    print(f"\nFile Model {i+1}:")
                    print(f"  ID: {model.get('id')}")
                    print(f"  Prompt: {model.get('prompt')}")
                    print(f"  Created: {model.get('created_at')}")
                    
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        print(f"File not found: {demo_file}")

if __name__ == "__main__":
    test_models_api() 