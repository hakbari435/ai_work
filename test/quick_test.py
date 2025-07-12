#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick test for API key
"""

import os
import sys
sys.path.append('..')
from dotenv import load_dotenv
from llm_converter import ComposeToJsonConverter

def quick_test():
    """Simple test to check if API key works"""
    
    print("🧪 Quick Test - API Key Check")
    print("=" * 30)
    
    # Load .env file
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ API key not found in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Create converter
        print("🔄 Creating converter...")
        converter = ComposeToJsonConverter(api_key)
        
        # Simple test code
        test_code = 'Text("Hello World")'
        
        print(f"🔄 Testing with: {test_code}")
        
        # Convert
        result = converter.convert_compose_to_json(test_code)
        
        # Show result
        if result['success']:
            print("✅ SUCCESS!")
            print(f"📤 Input: {result['input']}")
            print(f"📥 Output: {result['output']}")
            return True
        else:
            print("❌ FAILED!")
            print(f"Error: {result['error']}")
            
            # Show raw response if available
            if 'raw_response' in result:
                print(f"📄 Raw response:")
                print("=" * 40)
                print(result['raw_response'])
                print("=" * 40)
            
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    
    if success:
        print("\n🎉 API key works! Ready for main project.")
    else:
        print("\n🔧 Need to fix issues before using main project.") 