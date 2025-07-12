#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8001"

def test_api():
    """Test all API endpoints"""
    
    print("🧪 Testing Compose to JSON API")
    print("=" * 40)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test 1: Root endpoint
        print("\n📝 Test 1: Root endpoint")
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 2: Health check
        print("\n📝 Test 2: Health check")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 3: Info endpoint
        print("\n📝 Test 3: Info endpoint")
        response = requests.get(f"{BASE_URL}/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test 4: Examples endpoint
        print("\n📝 Test 4: Examples endpoint")
        response = requests.get(f"{BASE_URL}/examples")
        print(f"Status: {response.status_code}")
        examples = response.json()
        print(f"Found {len(examples['examples'])} examples")
        
        # Test 5: Convert endpoint - Simple Text
        print("\n📝 Test 5: Convert Simple Text")
        data = {"compose_code": 'Text("Hello World")'}
        response = requests.post(f"{BASE_URL}/convert", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Output: {result.get('output')}")
        
        # Test 6: Convert endpoint - Button
        print("\n📝 Test 6: Convert Button")
        data = {"compose_code": 'Button(onClick = { }) { Text("Click me") }'}
        response = requests.post(f"{BASE_URL}/convert", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Output: {result.get('output')}")
        
        # Test 7: Convert endpoint - Persian Text
        print("\n📝 Test 7: Convert Persian Text")
        data = {"compose_code": 'Text("سلام دنیا")'}
        response = requests.post(f"{BASE_URL}/convert", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"Output: {result.get('output')}")
        
        # Test 8: Error handling - Empty input
        print("\n📝 Test 8: Error handling - Empty input")
        data = {"compose_code": ""}
        response = requests.post(f"{BASE_URL}/convert", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Error: {result.get('detail')}")
        
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api() 