#!/usr/bin/env python3
"""
Script to help check web interface credits and understand the credit system.
"""

import requests
import json

def check_api_credits():
    """Check what the API reports for credits."""
    print("🔍 Checking API Credit Information...")
    
    # Test both API keys
    api_keys = [
        
        ""
    ]
    
    base_url = "https://api.tripo3d.ai/v2/openapi"
    
    for i, api_key in enumerate(api_keys, 1):
        print(f"\n🔑 Testing API Key {i}: {api_key[:10]}...")
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Check balance
        try:
            response = requests.get(f"{base_url}/user/balance", headers=headers, timeout=10)
            print(f"📊 Balance endpoint: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Balance: {data}")
            elif response.status_code == 401:
                print(f"❌ Authentication failed")
            else:
                print(f"❌ Error: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test task creation
        try:
            payload = {"type": "text_to_model", "prompt": "A red sports car"}
            response = requests.post(f"{base_url}/task", headers=headers, json=payload, timeout=10)
            print(f"📊 Task creation: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Task created successfully")
            elif response.status_code == 403:
                print(f"❌ No credits available")
            elif response.status_code == 401:
                print(f"❌ Authentication failed")
            else:
                print(f"❌ Error: {response.text[:100]}...")
        except Exception as e:
            print(f"❌ Exception: {e}")

def provide_web_check_instructions():
    """Provide detailed instructions for checking web interface."""
    print("\n🌐 WEB INTERFACE CREDIT CHECK INSTRUCTIONS:")
    print("=" * 50)
    print("1. Open your web browser")
    print("2. Go to: https://platform.tripo3d.ai")
    print("3. Log in to your account")
    print("4. Look for these sections:")
    print("   - Dashboard (main page)")
    print("   - Credits or Balance")
    print("   - Account Settings")
    print("   - Billing or Subscription")
    print("   - API Keys or Developer Settings")
    print("5. Check for different credit types:")
    print("   - API Credits")
    print("   - Web Interface Credits")
    print("   - Trial Credits")
    print("   - Free Credits")
    print("6. Look for API key management")
    print("7. Check if credits can be allocated to API keys")
    print("\n📝 Please tell me:")
    print("- How many credits you see")
    print("- Where exactly you see them")
    print("- If there are different types of credits")
    print("- If there's an API key management section")

def analyze_credit_discrepancy():
    """Analyze the credit discrepancy issue."""
    print("\n🔍 CREDIT DISCREPANCY ANALYSIS:")
    print("=" * 40)
    print("❌ PROBLEM: Web shows 270 credits, API shows 0 credits")
    print("\n🎯 POSSIBLE CAUSES:")
    print("1. Different credit pools (Web vs API)")
    print("2. Credits not allocated to API usage")
    print("3. API key linked to different account")
    print("4. Backend configuration issue")
    print("5. Credits only available for web interface")
    print("\n🚀 SOLUTIONS TO TRY:")
    print("1. Check web interface for API-specific settings")
    print("2. Look for credit allocation options")
    print("3. Generate new API key from different section")
    print("4. Contact Tripo3D support")
    print("5. Check if credits are trial/web-only")

def main():
    """Run the credit check analysis."""
    check_api_credits()
    provide_web_check_instructions()
    analyze_credit_discrepancy()

if __name__ == "__main__":
    main() 