#!/usr/bin/env python3
"""
Test script to check Tripo API key configuration
"""

import os
import sys
from dotenv import load_dotenv

def test_api_key():
    """Test if Tripo API key is configured"""
    
    print("Testing Tripo API Key Configuration...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("Please create a .env file with your Tripo API key")
        return False
    
    # Check API key
    api_key = os.getenv('TRIPO_API_KEY')
    if api_key and api_key != "your_tripo_api_key_here":
        print(f"✅ Tripo API key found: {api_key[:10]}...")
        return True
    else:
        print("❌ Tripo API key not configured")
        print("Please add your Tripo API key to the .env file:")
        print("TRIPO_API_KEY=your_actual_api_key_here")
        return False

def create_env_template():
    """Create a template .env file"""
    template = """# Tripo AI API Configuration
TRIPO_API_KEY=your_tripo_api_key_here
TRIPO_API_URL=https://api.tripo.ai

# Web Server Configuration
WEB_SERVER_HOST=localhost
WEB_SERVER_PORT=5000
DEBUG=True

# File Storage
MODEL_STORAGE_PATH=./data/generated_models
CACHE_PATH=./data/cache
LOG_PATH=./data/logs

# Security
SECRET_KEY=your_secret_key_here_change_this_in_production

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Model Generation Settings
DEFAULT_MODEL_QUALITY=high
DEFAULT_MODEL_FORMAT=glb
MAX_GENERATION_TIME=300
MAX_FILE_SIZE=100MB
"""
    
    with open('.env', 'w') as f:
        f.write(template)
    print("✅ Created .env template file")
    print("Please edit .env and add your actual Tripo API key")

if __name__ == "__main__":
    if not os.path.exists('.env'):
        print("Creating .env template...")
        create_env_template()
    else:
        test_api_key() 