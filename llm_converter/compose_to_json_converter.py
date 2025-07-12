#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compose to JSON converter for SDUI
"""

import json
from .llm_base_converter import GeminiConverter

class ComposeToJsonConverter(GeminiConverter):
    """
    Compose to JSON converter that inherits from GeminiConverter
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the converter
        
        Args:
            api_key: Gemini API key
            model_name: Gemini model name
        """
        # Base prompt
        base_prompt = "You are an expert in converting Jetpack Compose code to JSON."
        
        # Call parent class
        super().__init__(api_key, model_name, base_prompt)
        
        # Training examples list
        self.training_examples = []
        
        # Number of examples for few-shot
        self.few_shot_count = 5
        
        # Auto-load examples
        self.load_training_examples()
    
    def load_training_examples(self, dataset_file: str = "../datasets/compose_sdui_dataset.json"):
        """
        Load training examples from file
        
        Args:
            dataset_file: Dataset file path
        """
        try:
            with open(dataset_file, 'r', encoding='utf-8') as f:
                self.training_examples = json.load(f)
            
            print(f"✅ {len(self.training_examples)} training examples loaded")
            
        except FileNotFoundError:
            print(f"❌ File {dataset_file} not found")
            self.training_examples = []
        except json.JSONDecodeError:
            print(f"❌ Error reading JSON file")
            self.training_examples = []
        except Exception as e:
            print(f"❌ Error loading examples: {e}")
            self.training_examples = []
    
    def create_few_shot_prompt(self, input_code: str) -> str:
        """
        Create prompt with few-shot examples
        
        Args:
            input_code: Input code
            
        Returns:
            Complete prompt with examples
        """
        # Start prompt
        prompt_parts = [
            "You are an expert in converting Jetpack Compose code to JSON.",
            "Convert Compose code to JSON format exactly.",
            "",
            "Rules:",
            "- Generate only valid JSON",
            "- Use English keys", 
            "- Preserve UI structure",
            "- No additional explanations",
            ""
        ]
        
        # Add few-shot examples
        if self.training_examples:
            prompt_parts.append("Examples:")
            prompt_parts.append("")
            
            # Select examples
            examples_to_use = self.training_examples[:self.few_shot_count]
            
            for i, example in enumerate(examples_to_use, 1):
                prompt_parts.extend([
                    f"Example {i}:",
                    f"Input: {example['input']}",
                    f"Output: {json.dumps(example['output'], ensure_ascii=False)}",
                    ""
                ])
        
        # Add input code
        prompt_parts.extend([
            "Now convert this code:",
            f"Input: {input_code}",
            "Output:"
        ])
        
        return "\n".join(prompt_parts)
    
    def convert_compose_to_json(self, compose_code: str) -> dict:
        """
        Convert Compose code to JSON
        
        Args:
            compose_code: Jetpack Compose code
            
        Returns:
            Result dictionary
        """
        print(f"🔄 Converting Compose code: {compose_code}")
        
        try:
            # Create prompt with examples
            full_prompt = self.create_few_shot_prompt(compose_code)
            
            # Use _call_model from parent class
            if self.model is None:
                self._initialize_model()
            
            result = self._call_model(full_prompt)
            
            if result:
                # Clean response
                cleaned_result = result.strip()
                
                # Remove markdown code blocks if present
                if cleaned_result.startswith('```json'):
                    cleaned_result = cleaned_result[7:]  # Remove ```json
                if cleaned_result.startswith('```'):
                    cleaned_result = cleaned_result[3:]   # Remove ```
                if cleaned_result.endswith('```'):
                    cleaned_result = cleaned_result[:-3]  # Remove ending ```
                
                # Final cleanup
                cleaned_result = cleaned_result.strip()
                
                # Try to parse JSON
                try:
                    result_json = json.loads(cleaned_result)
                    print(f"✅ Conversion successful!")
                    return {
                        'success': True,
                        'input': compose_code,
                        'output': result_json,
                        'raw_response': cleaned_result
                    }
                except json.JSONDecodeError:
                    # If JSON is invalid
                    print(f"❌ Invalid JSON")
                    return {
                        'success': False,
                        'input': compose_code,
                        'error': 'Response is not valid JSON',
                        'raw_response': cleaned_result
                    }
            else:
                print(f"❌ Conversion error")
                return {
                    'success': False,
                    'input': compose_code,
                    'error': 'Error calling model'
                }
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {
                'success': False,
                'input': compose_code,
                'error': str(e)
            }
    
    def test_on_examples(self, count: int = 3):
        """
        Test on examples from dataset
        
        Args:
            count: Number of test examples
            
        Returns:
            List of results
        """
        if not self.training_examples:
            print("❌ Training examples not loaded")
            return []
        
        # Select test examples (from end of dataset)
        test_examples = self.training_examples[-count:]
        results = []
        
        print(f"🧪 Testing on {len(test_examples)} examples...")
        
        for i, example in enumerate(test_examples, 1):
            print(f"\n--- Test {i} ---")
            result = self.convert_compose_to_json(example['input'])
            
            if result['success']:
                # Compare with expected result
                expected = example['output']
                actual = result['output']
                is_correct = expected == actual
                
                result['expected'] = expected
                result['is_correct'] = is_correct
                
                if is_correct:
                    print(f"✅ Result correct")
                else:
                    print(f"❌ Result incorrect")
                    print(f"   Expected: {expected}")
                    print(f"   Got: {actual}")
            
            results.append(result)
        
        return results
    
    def get_training_info(self) -> dict:
        """
        Get training information
        
        Returns:
            Training information
        """
        base_info = self.get_provider_info()
        
        return {
            **base_info,
            "training_examples_count": len(self.training_examples),
            "few_shot_count": self.few_shot_count,
            "training_loaded": len(self.training_examples) > 0,
            "class_name": "ComposeToJsonConverter"
        }
    
    def set_few_shot_count(self, count: int):
        """
        Set number of few-shot examples
        
        Args:
            count: Number of examples
        """
        if self.training_examples:
            self.few_shot_count = max(1, min(count, len(self.training_examples)))
        else:
            self.few_shot_count = count
        print(f"✅ Few-shot examples count: {self.few_shot_count}")

# Example usage
if __name__ == "__main__":
    print("🚀 Compose to JSON Converter (with training)")
    print("=" * 50)
    
    try:
        # Create converter
        converter = ComposeToJsonConverter("fake-api-key")
        
        # Set example count
        converter.set_few_shot_count(3)
        
        # Show information
        info = converter.get_training_info()
        print(f"\n📋 Information:")
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Test conversion
        print(f"\n🧪 Test conversion:")
        test_codes = [
            'Text("Hello World")',
            'Button(onClick = { }) { Text("Click me") }'
        ]
        
        for code in test_codes:
            result = converter.convert_compose_to_json(code)
            print(f"\n   Input: {code}")
            if result['success']:
                print(f"   Output: {json.dumps(result['output'], ensure_ascii=False)}")
            else:
                print(f"   Error: {result['error']}")
        
        # Test on dataset examples
        print(f"\n📊 Test on dataset examples:")
        results = converter.test_on_examples(2)
        
        # Summary
        if results:
            successful = sum(1 for r in results if r['success'])
            correct = sum(1 for r in results if r.get('is_correct', False))
            print(f"\n📈 Summary:")
            print(f"   Successful: {successful}/{len(results)}")
            print(f"   Correct: {correct}/{len(results)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n💡 For real usage:")
    print(f"converter = ComposeToJsonConverter('your-real-api-key')")
    print(f"result = converter.convert_compose_to_json('Text(\"Hello\")')")
    print(f"print(result)") 