#!/usr/bin/env python3
"""
Debug script to test model generation and identify async issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from src.api_clients.tripo_client import TripoAPIClient, TripoGenerationRequest
from config.settings import get_settings

async def test_generation():
    """Test the generation process step by step"""
    
    print("🔍 Testing Tripo API Generation Process...")
    print("=" * 50)
    
    # Get settings
    settings = get_settings()
    print(f"API Key: {settings.tripo_api_key[:10]}...")
    
    # Create client
    client = TripoAPIClient(settings.tripo_api_key)
    
    # Create request
    request = TripoGenerationRequest(
        prompt="A silver motorcycle with leather seats",
        format="glb",
        quality="high"
    )
    
    try:
        print("1. Starting generation...")
        response = await client.generate_model(request)
        
        if response.success:
            task_id = response.data['id']
            print(f"✅ Generation started. Task ID: {task_id}")
            
            print("2. Waiting for completion...")
            wait_response = await client.wait_for_generation(task_id, timeout=300)
            
            if wait_response.success:
                print("✅ Generation completed")
                
                print("3. Getting final status...")
                status_response = await client.get_generation_status(task_id)
                
                if status_response.success:
                    print(f"✅ Status: {status_response.data.get('status')}")
                    print(f"Data: {status_response.data}")
                else:
                    print(f"❌ Status check failed: {status_response.error}")
            else:
                print(f"❌ Wait failed: {wait_response.error}")
        else:
            print(f"❌ Generation failed: {response.error}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    asyncio.run(test_generation()) 