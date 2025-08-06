#!/usr/bin/env python3
"""
Test script to check if .env file is being read correctly.
"""

import os
from pathlib import Path

def test_env_loading():
    """Test if environment variables are loaded correctly."""
    
    print("🔍 Testing Environment Variables...")
    print("-" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Read the file content
        with open(env_file, 'r') as f:
            content = f.read()
            print(f"📄 File content (first 100 chars): {content[:100]}...")
            
            # Check if API key is in the file
            if "" in content:
                print("✅ API key found in .env file")
            else:
                print("❌ API key not found in .env file")
    else:
        print("❌ .env file not found")
    
    # Check environment variable
    api_key = os.getenv("TRIPO_API_KEY")
    print(f"\n🔑 Environment variable TRIPO_API_KEY: {api_key}")
    
    if api_key and api_key.startswith("tsk_"):
        print("✅ API key is properly set in environment")
        print(f"   Key: {api_key[:10]}...")
    else:
        print("❌ API key not found in environment or invalid format")
    
    # Try to load with python-dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key_after_load = os.getenv("TRIPO_API_KEY")
        print(f"\n🔄 After dotenv load: {api_key_after_load}")
        
        if api_key_after_load and api_key_after_load.startswith("tsk_"):
            print("✅ API key loaded successfully with dotenv")
        else:
            print("❌ API key still not loaded properly")
            
    except ImportError:
        print("⚠️  python-dotenv not installed")
    except Exception as e:
        print(f"❌ Error loading .env: {e}")

if __name__ == "__main__":
    test_env_loading() 