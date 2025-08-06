#!/usr/bin/env python3
"""
Test script to try different Tripo3D configurations for lower credit usage.
"""

import asyncio
import os
from tripo3d import TripoClient

API_KEY = "tsk_1dZGrZJGhPjbZxU30svAeON8mPK41dkBo9I2DjKudx7"

async def test_tripo_configurations():
    """Test different Tripo3D configurations."""
    print("🔍 Testing different Tripo3D configurations...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    
    configurations = [
        {
            "name": "Standard (current)",
            "params": {}
        },
        {
            "name": "Lite - Low texture quality",
            "params": {"texture_quality": "low"}
        },
        {
            "name": "Lite - Smart low poly",
            "params": {"smart_low_poly": True}
        },
        {
            "name": "Lite - Compressed",
            "params": {"compress": True}
        },
        {
            "name": "Lite - Low texture + Smart low poly",
            "params": {"texture_quality": "low", "smart_low_poly": True}
        },
        {
            "name": "Lite - All optimizations",
            "params": {"texture_quality": "low", "smart_low_poly": True, "compress": True}
        }
    ]
    
    try:
        async with TripoClient(api_key=API_KEY) as client:
            print("✅ Connected to Tripo3D API")
            
            # Check balance first
            try:
                balance = await client.get_balance()
                print(f"💰 Account Balance: {balance}")
            except Exception as e:
                print(f"❌ Balance check failed: {e}")
            
            # Test each configuration
            for config in configurations:
                print(f"\n🚀 Testing: {config['name']}")
                print(f"📋 Parameters: {config['params']}")
                
                try:
                    task_id = await client.text_to_model(
                        prompt="A red sports car",
                        **config['params']
                    )
                    print(f"✅ Task created: {task_id}")
                    
                    # Wait for completion
                    print("⏳ Waiting for generation to complete...")
                    task = await client.wait_for_task(task_id)
                    print(f"✅ Generation completed: {task}")
                    
                    # Download the model
                    output_path = f"./output/{task_id}_{config['name'].replace(' ', '_')}"
                    os.makedirs("./output", exist_ok=True)
                    await client.download_task_models(task, output_path)
                    print(f"✅ Model downloaded to: {output_path}")
                    
                    # If this works, we found a working configuration!
                    print(f"🎉 SUCCESS! Configuration '{config['name']}' works!")
                    return config
                    
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    continue
            
            print("\n❌ All configurations failed")
            
    except Exception as e:
        print(f"❌ SDK connection failed: {e}")

def main():
    """Run the configuration test."""
    asyncio.run(test_tripo_configurations())

if __name__ == "__main__":
    main() 