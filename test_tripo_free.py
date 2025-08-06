#!/usr/bin/env python3
"""
Test script to check for free methods or trial options in Tripo3D.
"""

import asyncio
import os
from tripo3d import TripoClient

API_KEY = "tsk_1dZGrZJGhPjbZxU30svAeON8mPK41dkBo9I2DjKudx7"

async def test_free_methods():
    """Test if there are any free methods available."""
    print("🔍 Testing for free methods in Tripo3D...")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    
    try:
        async with TripoClient(api_key=API_KEY) as client:
            print("✅ Connected to Tripo3D API")
            
            # Check balance first
            try:
                balance = await client.get_balance()
                print(f"💰 Account Balance: {balance}")
            except Exception as e:
                print(f"❌ Balance check failed: {e}")
            
            # Test different methods that might be free
            methods_to_test = [
                {
                    "name": "text_to_model (standard)",
                    "method": lambda: client.text_to_model(prompt="A red sports car")
                },
                {
                    "name": "text_to_model (minimal)",
                    "method": lambda: client.text_to_model(
                        prompt="A red sports car",
                        texture=False,  # No texture
                        pbr=False,      # No PBR
                        smart_low_poly=True  # Low poly
                    )
                },
                {
                    "name": "image_to_model (if you have an image)",
                    "method": lambda: client.image_to_model(image_path="test_image.jpg")
                },
                {
                    "name": "multiview_to_model (if you have multiple images)",
                    "method": lambda: client.multiview_to_model(image_paths=["img1.jpg", "img2.jpg"])
                }
            ]
            
            for method_test in methods_to_test:
                print(f"\n🚀 Testing: {method_test['name']}")
                
                try:
                    if "image" in method_test['name']:
                        print("⏭️ Skipping image methods (no test images available)")
                        continue
                    
                    task_id = await method_test['method']()
                    print(f"✅ Task created: {task_id}")
                    
                    # Wait for completion
                    print("⏳ Waiting for generation to complete...")
                    task = await client.wait_for_task(task_id)
                    print(f"✅ Generation completed: {task}")
                    
                    # Download the model
                    output_path = f"./output/{task_id}_{method_test['name'].replace(' ', '_')}"
                    os.makedirs("./output", exist_ok=True)
                    await client.download_task_models(task, output_path)
                    print(f"✅ Model downloaded to: {output_path}")
                    
                    # If this works, we found a working method!
                    print(f"🎉 SUCCESS! Method '{method_test['name']}' works!")
                    return method_test
                    
                except Exception as e:
                    print(f"❌ Failed: {e}")
                    continue
            
            print("\n❌ All methods require credits")
            
    except Exception as e:
        print(f"❌ SDK connection failed: {e}")

def main():
    """Run the free methods test."""
    asyncio.run(test_free_methods())

if __name__ == "__main__":
    main() 