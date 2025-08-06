#!/usr/bin/env python3
"""
Test script using the official Tripo3D Python SDK.
"""

import asyncio
import os
from tripo3d import TripoClient

API_KEY = ""

async def test_tripo_sdk():
    """Test the official Tripo3D SDK."""
    print("🔍 Testing Tripo3D SDK...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    
    try:
        async with TripoClient(api_key=API_KEY) as client:
            print("✅ Connected to Tripo3D API")
            
            # Test account info
            try:
                balance = await client.get_balance()
                print(f"💰 Account Balance: {balance}")
            except Exception as e:
                print(f"❌ Balance check failed: {e}")
            
            # Test text-to-model generation
            try:
                print("\n🚀 Testing text-to-model generation...")
                task_id = await client.text_to_model(prompt="A red sports car")
                print(f"✅ Task created: {task_id}")
                
                # Wait for completion
                print("⏳ Waiting for generation to complete...")
                task = await client.wait_for_task(task_id)
                print(f"✅ Generation completed: {task}")
                
                # Download the model
                output_path = f"./output/{task_id}"
                os.makedirs("./output", exist_ok=True)
                await client.download_task_models(task, output_path)
                print(f"✅ Model downloaded to: {output_path}")
                
            except Exception as e:
                print(f"❌ Text-to-model failed: {e}")
            
    except Exception as e:
        print(f"❌ SDK connection failed: {e}")

def main():
    """Run the SDK test."""
    asyncio.run(test_tripo_sdk())

if __name__ == "__main__":
    main() 