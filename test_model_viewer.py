#!/usr/bin/env python3
"""
Test script to verify the model viewer functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_model_viewer():
    print("🧪 Testing Model Viewer Functionality")
    print("=" * 50)
    
    # Test 1: Car model (should show car shape)
    print("\n1. Testing car model...")
    try:
        response = requests.get(f"{BASE_URL}/view/demo_model_1754428143")
        if response.status_code == 200:
            print("✅ Car model page loads successfully")
            print("   Expected: Blue car with wheels")
        else:
            print(f"❌ Car model page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Car model error: {e}")
    
    # Test 2: Robot model (should show robot shape)
    print("\n2. Testing robot model...")
    try:
        response = requests.get(f"{BASE_URL}/view/demo_model_1")
        if response.status_code == 200:
            print("✅ Robot model page loads successfully")
            print("   Expected: Metallic robot with head and arms")
        else:
            print(f"❌ Robot model page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Robot model error: {e}")
    
    # Test 3: Plant model (should show default cube)
    print("\n3. Testing plant model...")
    try:
        response = requests.get(f"{BASE_URL}/view/demo_model_1754428740")
        if response.status_code == 200:
            print("✅ Plant model page loads successfully")
            print("   Expected: Red cube (default shape)")
        else:
            print(f"❌ Plant model page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Plant model error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Model viewer test completed!")
    print("\n📝 Manual Testing Instructions:")
    print("1. Open http://localhost:5000/view/demo_model_1754428143")
    print("   - Should show a blue car with wheels")
    print("2. Open http://localhost:5000/view/demo_model_1")
    print("   - Should show a metallic robot")
    print("3. Open http://localhost:5000/view/demo_model_1754428740")
    print("   - Should show a red cube")
    print("\n🎮 Try the controls:")
    print("- Auto Rotate: Makes the model spin")
    print("- Wireframe: Shows model structure")
    print("- Toggle Lights: Changes lighting")
    print("- Reset Camera: Returns to original view")

if __name__ == "__main__":
    test_model_viewer() 