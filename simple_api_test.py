#!/usr/bin/env python3
"""
Simple API test script to verify Tripo AI API connection.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

async def test_api_connection():
    """Test the API connection with the configured API key."""
    
    print("🔍 Testing Tripo AI API Connection...")
    
    # Get API key from environment
    api_key = os.getenv("TRIPO_API_KEY")
    api_url = os.getenv("TRIPO_API_URL", "https://api.tripo3d.ai/v2/openapi")
    
    if not api_key:
        print("❌ No API key found in environment variables")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...")
    print(f"🌐 API URL: {api_url}")
    print("-" * 50)
    
    try:
        import aiohttp
        
        # Test basic connection
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Test with a simple task creation instead of health check
            print("📡 Testing API with simple task creation...")
            try:
                # Create a simple test payload
                test_payload = {
                    "type": "text_to_model",
                    "prompt": "A simple red cube",
                    "model_version": "v2.5-20250123"
                }
                
                async with session.post(f"{api_url}/task", headers=headers, json=test_payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ API connection successful!")
                        print(f"Response: {data}")
                        
                        if data.get("code") == 0 and data.get("data", {}).get("task_id"):
                            print(f"✅ Task created successfully! Task ID: {data['data']['task_id']}")
                            return True
                        else:
                            print(f"⚠️  API responded but task creation failed: {data}")
                            return False
                    else:
                        error_text = await response.text()
                        print(f"❌ API request failed with status {response.status}")
                        print(f"Error: {error_text}")
                        return False
            except Exception as e:
                print(f"❌ Connection error: {e}")
                return False
                
    except ImportError:
        print("❌ aiohttp not installed. Please install it with: pip install aiohttp")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_credits():
    """Test credit balance endpoint."""
    
    print("\n💰 Testing credit balance...")
    
    api_key = os.getenv("TRIPO_API_KEY")
    api_url = os.getenv("TRIPO_API_URL", "https://api.tripo3d.ai/v2/openapi")
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Try to get user info or credits
            try:
                async with session.get(f"{api_url}/user", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ User info retrieved successfully!")
                        print(f"User data: {data}")
                        return True
                    else:
                        print(f"⚠️  Could not get user info (status {response.status})")
                        return False
            except Exception as e:
                print(f"⚠️  Could not check user info: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error checking credits: {e}")
        return False

async def main():
    """Main test function."""
    
    print("🚀 Tripo AI API Connection Test")
    print("=" * 50)
    
    # Test basic connection
    connection_ok = await test_api_connection()
    
    if connection_ok:
        # Test credits
        await test_credits()
        
        print("\n🎉 API connection test completed successfully!")
        print("🚀 Your API key is valid and ready to use!")
    else:
        print("\n❌ API connection failed. Please check:")
        print("   - Your API key is correct")
        print("   - You have internet connection")
        print("   - The API service is available")

if __name__ == "__main__":
    asyncio.run(main()) 