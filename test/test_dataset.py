#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test on dataset samples
"""

import os
import json
import sys
sys.path.append('..')
from dotenv import load_dotenv
from llm_converter import ComposeToJsonConverter

def test_dataset():
    """Test on 5 samples from dataset"""
    
    print("🧪 Dataset Test - 5 Samples")
    print("=" * 40)
    
    # Load API key
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ API key not found")
        return
    
    try:
        # Create converter
        print("🔄 Creating converter...")
        converter = ComposeToJsonConverter(api_key)
        
        # Test on 5 examples
        print("🔄 Testing on 5 dataset samples...")
        results = converter.test_on_examples(count=5)
        
        if not results:
            print("❌ No results")
            return
        
        # Analyze results
        print("\n📊 Results Analysis:")
        print("=" * 40)
        
        successful = 0
        correct = 0
        
        for i, result in enumerate(results, 1):
            print(f"\n--- Sample {i} ---")
            print(f"📤 Input: {result['input']}")
            
            if result['success']:
                successful += 1
                print("✅ Conversion: SUCCESS")
                
                if result.get('is_correct', False):
                    correct += 1
                    print("✅ Accuracy: CORRECT")
                else:
                    print("❌ Accuracy: INCORRECT")
                    print(f"   Expected: {result.get('expected', 'N/A')}")
                    print(f"   Got: {result.get('output', 'N/A')}")
            else:
                print("❌ Conversion: FAILED")
                print(f"   Error: {result.get('error', 'Unknown')}")
        
        # Summary
        print(f"\n📈 Summary:")
        print("=" * 40)
        print(f"✅ Successful conversions: {successful}/5 ({successful*20}%)")
        print(f"✅ Correct results: {correct}/5 ({correct*20}%)")
        
        if successful == 5:
            print("🎉 All conversions successful!")
        if correct == 5:
            print("🎯 Perfect accuracy!")
        
        return {
            'total': 5,
            'successful': successful,
            'correct': correct,
            'success_rate': successful * 20,
            'accuracy_rate': correct * 20
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = test_dataset()
    
    if result:
        print(f"\n💡 Final Score:")
        print(f"   Success Rate: {result['success_rate']}%")
        print(f"   Accuracy Rate: {result['accuracy_rate']}%")
    else:
        print("\n🔧 Test failed - check setup") 