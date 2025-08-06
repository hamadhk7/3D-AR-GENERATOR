#!/usr/bin/env python3
"""
Test script to verify capture functionality in AR viewer.
"""

import requests
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_capture_functionality():
    """Test the capture functionality in AR viewer."""
    
    base_url = "http://localhost:5000"
    
    print("📸 Testing Capture Functionality")
    print("=" * 50)
    
    # Test 1: Check if web server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running")
        else:
            print("❌ Web server health check failed")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to web server: {e}")
        return False
    
    # Test 2: Check if AR viewer page loads
    model_id = "tripo_3f1ab50b-835b-49ea-82bc-e858c2734a13"
    try:
        response = requests.get(f"{base_url}/models/{model_id}/ar")
        if response.status_code == 200:
            print("✅ AR viewer page loads")
            
            # Check if capture button exists
            if 'id="captureBtn"' in response.text:
                print("✅ Capture button found in HTML")
            else:
                print("❌ Capture button not found in HTML")
                return False
                
        else:
            print(f"❌ AR viewer page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading AR viewer page: {e}")
        return False
    
    print("\n🎯 **Capture Functionality Test Results:**")
    print("=" * 50)
    print("✅ Backend: Web server running")
    print("✅ Frontend: AR viewer page loads")
    print("✅ UI: Capture button present")
    
    print("\n📱 **How to Test Capture:**")
    print("=" * 50)
    print("1. Go to: http://localhost:5000/models/tripo_3f1ab50b-835b-49ea-82bc-e858c2734a13/ar")
    print("2. Click 'Start AR' to load the 3D model")
    print("3. Click 'Capture' button")
    print("4. Check your downloads folder for the screenshot")
    print("5. Look for toast notification confirming capture")
    
    print("\n🔧 **Expected Behavior:**")
    print("=" * 50)
    print("• Capture button shows 'Capturing...' with spinner")
    print("• Screenshot downloads automatically")
    print("• Toast notification shows 'Screenshot saved successfully!'")
    print("• File named: ar-screenshot-{model_id}-{timestamp}.png")
    
    print("\n🐛 **If Capture Doesn't Work:**")
    print("=" * 50)
    print("• Check browser console for JavaScript errors")
    print("• Ensure 3D model is loaded before capturing")
    print("• Try different browsers (Chrome recommended)")
    print("• Check browser download settings")
    
    return True

if __name__ == "__main__":
    test_capture_functionality() 