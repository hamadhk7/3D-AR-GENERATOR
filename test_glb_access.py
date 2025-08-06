#!/usr/bin/env python3
"""
Test script to check GLB file accessibility
"""

import requests
import sys

def test_glb_access():
    """Test if the GLB file is accessible from our local endpoint."""
    
    model_id = "tripo_3f1ab50b-835b-49ea-82bc-e858c2734a13"
    url = f"http://localhost:5000/api/models/{model_id}/download"
    
    print(f"Testing GLB file access for model: {model_id}")
    print(f"URL: {url}")
    
    try:
        # Test HEAD request first
        print("\n1. Testing HEAD request...")
        response = requests.head(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'Not set')}")
        print(f"Content-Length: {response.headers.get('Content-Length', 'Not set')}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        
        # Test GET request
        print("\n2. Testing GET request...")
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ GLB file is accessible!")
            
            # Check if it's actually a GLB file
            if response.content.startswith(b'glTF'):
                print("✅ Content appears to be a valid GLB file (starts with 'glTF')")
            else:
                print("⚠️  Content doesn't start with 'glTF' - might not be a valid GLB file")
                print(f"First 20 bytes: {response.content[:20]}")
        else:
            print(f"❌ Failed to access GLB file: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing GLB access: {e}")

if __name__ == "__main__":
    test_glb_access() 