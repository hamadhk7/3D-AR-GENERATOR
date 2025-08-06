#!/usr/bin/env python3
"""
Test script for 3D AR Demo application
"""

import requests
import json
import time
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_models():
    """Test getting models list"""
    print("\n🔍 Testing get models...")
    try:
        response = requests.get(f"{BASE_URL}/api/models")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get models passed: Found {len(data)} models")
            return True
        else:
            print(f"❌ Get models failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get models error: {e}")
        return False

def test_generate_model():
    """Test model generation"""
    print("\n🔍 Testing model generation...")
    try:
        payload = {"prompt": "test car model"}
        response = requests.post(
            f"{BASE_URL}/api/generate",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model generation passed: {data}")
            return True
        else:
            print(f"❌ Model generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model generation error: {e}")
        return False

def test_get_specific_model():
    """Test getting a specific model"""
    print("\n🔍 Testing get specific model...")
    try:
        response = requests.get(f"{BASE_URL}/api/models/demo_model_1")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get specific model passed: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ Get specific model failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get specific model error: {e}")
        return False

def test_static_files():
    """Test static file serving"""
    print("\n🔍 Testing static files...")
    static_files = [
        "/static/css/main.css",
        "/static/js/main.js"
    ]
    
    all_passed = True
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            if response.status_code == 200:
                print(f"✅ Static file {file_path} loaded successfully")
            else:
                print(f"❌ Static file {file_path} failed: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ Static file {file_path} error: {e}")
            all_passed = False
    
    return all_passed

def test_web_pages():
    """Test web page loading"""
    print("\n🔍 Testing web pages...")
    pages = [
        "/",
        "/models/",
        "/view/demo_model_1",
        "/models/demo_model_1/ar"
    ]
    
    all_passed = True
    for page in pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✅ Page {page} loaded successfully")
            else:
                print(f"❌ Page {page} failed: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ Page {page} error: {e}")
            all_passed = False
    
    return all_passed

def test_cors():
    """Test CORS headers"""
    print("\n🔍 Testing CORS...")
    try:
        response = requests.get(f"{BASE_URL}/api/models")
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print(f"✅ CORS header found: {cors_header}")
            return True
        else:
            print("❌ CORS header not found")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting 3D AR Demo Application Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Get Models", test_get_models),
        ("Generate Model", test_generate_model),
        ("Get Specific Model", test_get_specific_model),
        ("Static Files", test_static_files),
        ("Web Pages", test_web_pages),
        ("CORS", test_cors)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1) 