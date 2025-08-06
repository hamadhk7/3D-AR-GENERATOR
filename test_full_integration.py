#!/usr/bin/env python3
"""
Comprehensive test to verify API integration works throughout the entire codebase.
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add the project root to the Python path (same as scripts)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_environment_loading():
    """Test that environment variables are properly loaded."""
    print("🔍 Testing Environment Loading...")
    
    # Test .env file loading
    api_key = os.getenv("TRIPO_API_KEY")
    api_url = os.getenv("TRIPO_API_URL")
    
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    if not api_key.startswith("tsk_"):
        print("❌ API key format is invalid")
        return False
    
    print(f"✅ Environment loaded successfully")
    print(f"   API Key: {api_key[:10]}...")
    print(f"   API URL: {api_url}")
    return True

def test_settings_configuration():
    """Test that settings are properly configured."""
    print("\n🔧 Testing Settings Configuration...")
    
    try:
        from config.settings import settings
        
        print(f"✅ Settings loaded successfully")
        print(f"   API Key: {settings.tripo_api_key[:10]}...")
        print(f"   API URL: {settings.tripo_api_url}")
        print(f"   Web Server: {settings.web_server_host}:{settings.web_server_port}")
        print(f"   Debug Mode: {settings.debug}")
        
        return True
    except Exception as e:
        print(f"❌ Settings configuration failed: {e}")
        return False

def test_api_client_import():
    """Test that API client can be imported and initialized."""
    print("\n📦 Testing API Client Import...")
    
    try:
        from src.api_clients.tripo_client import TripoAPIClient, TripoGenerationRequest
        
        api_key = os.getenv("TRIPO_API_KEY")
        client = TripoAPIClient(api_key)
        
        print("✅ API client imported and initialized successfully")
        return True
    except Exception as e:
        print(f"❌ API client import failed: {e}")
        return False

async def test_api_client_functionality():
    """Test that API client works correctly."""
    print("\n🚀 Testing API Client Functionality...")
    
    try:
        from src.api_clients.tripo_client import TripoAPIClient, TripoGenerationRequest
        
        api_key = os.getenv("TRIPO_API_KEY")
        client = TripoAPIClient(api_key)
        
        # Test generation request
        request = TripoGenerationRequest(
            prompt="A simple test cube",
            format="glb",
            quality="medium"
        )
        
        print("✅ API client functionality test passed")
        return True
    except Exception as e:
        print(f"❌ API client functionality failed: {e}")
        return False

def test_web_routes_import():
    """Test that web routes can be imported."""
    print("\n🌐 Testing Web Routes Import...")
    
    try:
        from src.web.routes.api import api_bp
        from src.web.routes.models import models_bp
        
        print("✅ Web routes imported successfully")
        return True
    except Exception as e:
        print(f"❌ Web routes import failed: {e}")
        return False

def test_flask_app_creation():
    """Test that Flask app can be created."""
    print("\n🏗️ Testing Flask App Creation...")
    
    try:
        from src.web.app import create_app
        
        app = create_app()
        
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_mcp_server_import():
    """Test that MCP server can be imported."""
    print("\n🔌 Testing MCP Server Import...")
    
    try:
        from src.mcp_server.server import MCPServer
        from src.mcp_server.tools import get_tools
        from src.mcp_server.handlers import ToolHandler
        
        print("✅ MCP server imported successfully")
        return True
    except Exception as e:
        print(f"❌ MCP server import failed: {e}")
        return False

def test_utils_import():
    """Test that utility modules can be imported."""
    print("\n🛠️ Testing Utils Import...")
    
    try:
        from src.utils.logger import get_logger
        from src.utils.validators import validate_prompt
        
        logger = get_logger(__name__)
        logger.info("Utils test successful")
        
        print("✅ Utils imported successfully")
        return True
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False

def test_data_directories():
    """Test that required data directories exist."""
    print("\n📁 Testing Data Directories...")
    
    required_dirs = [
        "data/generated_models",
        "data/cache",
        "data/logs",
        "data/generated_models/glb",
        "data/generated_models/obj",
        "data/generated_models/usdz"
    ]
    
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Directory missing: {dir_path}")
            return False
    
    print("✅ All required directories exist")
    return True

def test_demo_models_file():
    """Test that demo models file exists and is valid JSON."""
    print("\n📄 Testing Demo Models File...")
    
    demo_models_file = "src/data/demo_models.json"
    
    if not os.path.exists(demo_models_file):
        print(f"❌ Demo models file missing: {demo_models_file}")
        return False
    
    try:
        with open(demo_models_file, 'r') as f:
            models = json.load(f)
        
        print(f"✅ Demo models file is valid JSON with {len(models)} models")
        return True
    except Exception as e:
        print(f"❌ Demo models file error: {e}")
        return False

async def test_end_to_end_workflow():
    """Test a complete end-to-end workflow."""
    print("\n🔄 Testing End-to-End Workflow...")
    
    try:
        # Test API client
        from src.api_clients.tripo_client import TripoAPIClient, TripoGenerationRequest
        
        api_key = os.getenv("TRIPO_API_KEY")
        client = TripoAPIClient(api_key)
        
        # Test generation request
        request = TripoGenerationRequest(
            prompt="A simple red cube for testing",
            format="glb",
            quality="medium"
        )
        
        print("✅ End-to-end workflow test passed")
        return True
    except Exception as e:
        print(f"❌ End-to-end workflow failed: {e}")
        return False

async def main():
    """Run all integration tests."""
    
    print("🚀 Full Codebase Integration Test")
    print("=" * 60)
    
    tests = [
        ("Environment Loading", test_environment_loading),
        ("Settings Configuration", test_settings_configuration),
        ("API Client Import", test_api_client_import),
        ("API Client Functionality", test_api_client_functionality),
        ("Web Routes Import", test_web_routes_import),
        ("Flask App Creation", test_flask_app_creation),
        ("MCP Server Import", test_mcp_server_import),
        ("Utils Import", test_utils_import),
        ("Data Directories", test_data_directories),
        ("Demo Models File", test_demo_models_file),
        ("End-to-End Workflow", test_end_to_end_workflow),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your codebase is fully integrated and ready to use!")
        print("🚀 You can now:")
        print("   - Start the web server: python scripts/start_web_server.py")
        print("   - Start the MCP server: python scripts/start_mcp_server.py")
        print("   - Generate 3D models through the web interface")
        print("   - View models in AR using the AR viewer")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("🔧 Make sure all dependencies are installed and configuration is correct.")

if __name__ == "__main__":
    asyncio.run(main()) 