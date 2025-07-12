#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic Usage Example - LLM Converter
"""

import os
import sys
sys.path.append('..')
from dotenv import load_dotenv
from llm_converter import ComposeToJsonConverter

def main():
    """Main example function"""
    
    print("🚀 LLM Converter - Basic Usage Example")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Please set GEMINI_API_KEY in .env file")
        return
    
    # Create converter
    print("🔄 Creating converter...")
    converter = ComposeToJsonConverter(api_key)
    
    # Show info
    info = converter.get_training_info()
    print(f"✅ Loaded {info['training_examples_count']} training examples")
    print(f"✅ Using {info['few_shot_count']} few-shot examples")
    
    # Example 1: Simple Text
    print("\n" + "="*30)
    print("📝 Example 1: Simple Text")
    print("="*30)
    
    compose_code = 'Text("Hello World")'
    result = converter.convert_compose_to_json(compose_code)
    
    if result['success']:
        print(f"✅ Input: {result['input']}")
        print(f"✅ Output: {result['output']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 2: Button with Text
    print("\n" + "="*30)
    print("📝 Example 2: Button with Text")
    print("="*30)
    
    compose_code = 'Button(onClick = { }) { Text("Click me") }'
    result = converter.convert_compose_to_json(compose_code)
    
    if result['success']:
        print(f"✅ Input: {result['input']}")
        print(f"✅ Output: {result['output']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 3: Column with multiple children
    print("\n" + "="*30)
    print("📝 Example 3: Column Layout")
    print("="*30)
    
    compose_code = '''Column {
        Text("Title")
        Text("Subtitle")
        Button(onClick = { }) { Text("Action") }
    }'''
    
    result = converter.convert_compose_to_json(compose_code)
    
    if result['success']:
        print(f"✅ Input: {result['input']}")
        print(f"✅ Output: {result['output']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 4: Persian text
    print("\n" + "="*30)
    print("📝 Example 4: Persian Text")
    print("="*30)
    
    compose_code = 'Text("سلام دنیا")'
    result = converter.convert_compose_to_json(compose_code)
    
    if result['success']:
        print(f"✅ Input: {result['input']}")
        print(f"✅ Output: {result['output']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*50)
    print("🎉 Examples completed!")
    print("💡 You can now use ComposeToJsonConverter in your projects")

if __name__ == "__main__":
    main() 