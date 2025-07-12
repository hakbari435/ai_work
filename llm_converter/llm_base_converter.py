#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base class for working with LLMs
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class LLMProvider(Enum):
    """
    List of LLM providers
    """
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"

class LLMBaseConverter(ABC):
    """
    Simple base class for working with LLMs
    """
    
    def __init__(self, api_key: str, model_name: str, prompt: str, provider: LLMProvider):
        """
        Initialize the converter
        
        Args:
            api_key: API key
            model_name: Model name
            prompt: Main prompt
            provider: LLM provider
        """
        self.api_key = api_key
        self.model_name = model_name
        self.prompt = prompt
        self.provider = provider
        self.model = None
    
    @abstractmethod
    def _initialize_model(self):
        """
        Initialize model based on provider
        """
        pass
    
    @abstractmethod
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """
        Call the model
        
        Args:
            full_prompt: Complete prompt
            
        Returns:
            Model response or None if error
        """
        pass
    
    @abstractmethod
    def get_available_models(self) -> list:
        """
        Get list of available models
        
        Returns:
            List of model names
        """
        pass
    
    def build_full_prompt(self, input_text: str) -> str:
        """
        Build complete prompt
        
        Args:
            input_text: Input text
            
        Returns:
            Complete prompt
        """
        return f"{self.prompt}\n\nInput: {input_text}\nOutput:"
    
    def convert(self, input_text: str) -> Optional[str]:
        """
        Process input text
        
        Args:
            input_text: Input text
            
        Returns:
            Model response or None if error
        """
        try:
            # Initialize model if needed
            if self.model is None:
                self._initialize_model()
            
            # Build complete prompt
            full_prompt = self.build_full_prompt(input_text)
            
            # Call model
            response = self._call_model(full_prompt)
            
            # Clean response
            if response:
                return response.strip()
            return None
            
        except Exception as e:
            print(f"Error in processing: {e}")
            return None
    
    def get_provider_info(self) -> dict:
        """
        Get provider information
        
        Returns:
            Provider information
        """
        return {
            "provider": self.provider.value,
            "model_name": self.model_name,
            "api_key_set": bool(self.api_key),
            "model_initialized": self.model is not None
        }

# Implementation classes for each LLM

class GeminiConverter(LLMBaseConverter):
    """
    Implementation for Google Gemini
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash", prompt: str = ""):
        super().__init__(api_key, model_name, prompt, LLMProvider.GEMINI)
    
    def _initialize_model(self):
        """Initialize Gemini model"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ Gemini model ({self.model_name}) initialized")
        except Exception as e:
            print(f"❌ Error initializing Gemini: {e}")
            raise
    
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """Call Gemini model"""
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error calling Gemini: {e}")
            return None
    
    def get_available_models(self) -> list:
        """Get available Gemini models"""
        return [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro",
            "gemini-pro-vision"
        ]

class OpenAIConverter(LLMBaseConverter):
    """
    Implementation for OpenAI GPT
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo", prompt: str = ""):
        super().__init__(api_key, model_name, prompt, LLMProvider.OPENAI)
    
    def _initialize_model(self):
        """Initialize OpenAI model"""
        try:
            import openai
            openai.api_key = self.api_key
            self.model = openai
            print(f"✅ OpenAI model ({self.model_name}) initialized")
        except Exception as e:
            print(f"❌ Error initializing OpenAI: {e}")
            raise
    
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """Call OpenAI model"""
        try:
            response = self.model.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=1000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error calling OpenAI: {e}")
            return None
    
    def get_available_models(self) -> list:
        """Get available OpenAI models"""
        return [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]

class ClaudeConverter(LLMBaseConverter):
    """
    Implementation for Anthropic Claude
    """
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229", prompt: str = ""):
        super().__init__(api_key, model_name, prompt, LLMProvider.CLAUDE)
    
    def _initialize_model(self):
        """Initialize Claude model"""
        try:
            import anthropic
            self.model = anthropic.Anthropic(api_key=self.api_key)
            print(f"✅ Claude model ({self.model_name}) initialized")
        except Exception as e:
            print(f"❌ Error initializing Claude: {e}")
            raise
    
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """Call Claude model"""
        try:
            response = self.model.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=0.1,
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error calling Claude: {e}")
            return None
    
    def get_available_models(self) -> list:
        """Get available Claude models"""
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1"
        ]

class OllamaConverter(LLMBaseConverter):
    """
    Implementation for Ollama (local models)
    """
    
    def __init__(self, api_key: str = "", model_name: str = "llama2", prompt: str = ""):
        super().__init__(api_key, model_name, prompt, LLMProvider.OLLAMA)
    
    def _initialize_model(self):
        """Initialize Ollama model"""
        try:
            import requests
            self.model = requests
            print(f"✅ Ollama model ({self.model_name}) initialized")
        except Exception as e:
            print(f"❌ Error initializing Ollama: {e}")
            raise
    
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """Call Ollama model"""
        try:
            response = self.model.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.model_name,
                    'prompt': full_prompt,
                    'stream': False
                }
            )
            return response.json()['response']
        except Exception as e:
            print(f"❌ Error calling Ollama: {e}")
            return None
    
    def get_available_models(self) -> list:
        """Get available Ollama models"""
        return [
            "llama2",
            "llama2:13b",
            "codellama",
            "mistral",
            "neural-chat"
        ]

class HuggingFaceConverter(LLMBaseConverter):
    """
    Implementation for Hugging Face
    """
    
    def __init__(self, api_key: str, model_name: str = "microsoft/DialoGPT-medium", prompt: str = ""):
        super().__init__(api_key, model_name, prompt, LLMProvider.HUGGINGFACE)
    
    def _initialize_model(self):
        """Initialize Hugging Face model"""
        try:
            from transformers import pipeline
            self.model = pipeline("text-generation", model=self.model_name, token=self.api_key)
            print(f"✅ Hugging Face model ({self.model_name}) initialized")
        except Exception as e:
            print(f"❌ Error initializing Hugging Face: {e}")
            raise
    
    def _call_model(self, full_prompt: str) -> Optional[str]:
        """Call Hugging Face model"""
        try:
            response = self.model(full_prompt, max_length=200, num_return_sequences=1)
            return response[0]['generated_text'].replace(full_prompt, "").strip()
        except Exception as e:
            print(f"❌ Error calling Hugging Face: {e}")
            return None
    
    def get_available_models(self) -> list:
        """Get available Hugging Face models"""
        return [
            "microsoft/DialoGPT-medium",
            "microsoft/DialoGPT-large",
            "facebook/blenderbot-400M-distill",
            "google/flan-t5-base",
            "bigscience/bloom-560m"
        ]

# Helper function to create converter
def create_converter(provider: LLMProvider, api_key: str, model_name: str = "", prompt: str = "") -> LLMBaseConverter:
    """
    Create converter based on provider
    
    Args:
        provider: LLM provider
        api_key: API key
        model_name: Model name (optional)
        prompt: Main prompt
        
    Returns:
        Converter instance
    """
    if provider == LLMProvider.GEMINI:
        return GeminiConverter(api_key, model_name or "gemini-1.5-flash", prompt)
    elif provider == LLMProvider.OPENAI:
        return OpenAIConverter(api_key, model_name or "gpt-3.5-turbo", prompt)
    elif provider == LLMProvider.CLAUDE:
        return ClaudeConverter(api_key, model_name or "claude-3-sonnet-20240229", prompt)
    elif provider == LLMProvider.OLLAMA:
        return OllamaConverter(api_key, model_name or "llama2", prompt)
    elif provider == LLMProvider.HUGGINGFACE:
        return HuggingFaceConverter(api_key, model_name or "microsoft/DialoGPT-medium", prompt)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# Example usage
if __name__ == "__main__":
    print("🚀 LLMBaseConverter is ready!")
    print("\n📋 Supported providers:")
    for provider in LLMProvider:
        print(f"   - {provider.value}")
    
    print("\n💡 Example usage:")
    print("converter = create_converter(LLMProvider.GEMINI, 'your-api-key', prompt='Your prompt')")
    print("result = converter.convert('Input text')")
    print("print(result)") 