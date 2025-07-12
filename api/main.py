#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI for Compose to JSON conversion
"""

import os
import sys
sys.path.append('..')

from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from dotenv import load_dotenv
from llm_converter import ComposeToJsonConverter

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Compose to JSON API",
    description="Convert Jetpack Compose code to JSON using AI",
    version="1.0.0"
)

# Initialize converter
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

converter = ComposeToJsonConverter(API_KEY)

# Request model
class ComposeRequest(BaseModel):
    compose_code: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "compose_code": 'Text("Hello World")'
                }
            ]
        }
    }

# Response models
class SuccessResponse(BaseModel):
    success: bool = True
    input: str
    output: dict
    
class ErrorResponse(BaseModel):
    success: bool = False
    input: str
    error: str
    raw_response: str = ""

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Compose to JSON API",
        "version": "1.0.0",
        "endpoints": {
            "convert": "/convert",
            "health": "/health",
            "info": "/info"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "converter_ready": converter is not None,
        "training_examples": len(converter.training_examples) if converter else 0
    }

@app.get("/info")
async def get_info():
    """Get converter information"""
    if not converter:
        raise HTTPException(status_code=500, detail="Converter not initialized")
    
    info = converter.get_training_info()
    return {
        "model_info": info,
        "api_version": "1.0.0",
        "supported_features": [
            "Text conversion",
            "Button conversion", 
            "Layout conversion",
            "Persian text support",
            "Few-shot learning"
        ]
    }

@app.post("/convert")
async def convert_compose(request: ComposeRequest):
    """
    Convert Compose code to JSON
    
    Args:
        request: ComposeRequest with compose_code
        
    Returns:
        JSON conversion result
    """
    return await _convert_compose_code(request.compose_code)

@app.post("/convert/raw")
async def convert_compose_raw(compose_code: str = Form(...)):
    """
    Convert raw Compose code to JSON (accepts form data)
    
    Args:
        compose_code: Raw Compose code as form field
        
    Returns:
        JSON conversion result
    """
    return await _convert_compose_code(compose_code)

async def _convert_compose_code(compose_code: str):
    """
    Convert Compose code to JSON
    
    Args:
        compose_code: Compose code string
        
    Returns:
        JSON conversion result
    """
    try:
        # Validate input
        if not compose_code or not compose_code.strip():
            raise HTTPException(
                status_code=400, 
                detail="compose_code cannot be empty"
            )
        
        # Convert
        result = converter.convert_compose_to_json(compose_code.strip())
        
        # Return result
        if result['success']:
            return SuccessResponse(
                input=result['input'],
                output=result['output']
            )
        else:
            return ErrorResponse(
                input=result['input'],
                error=result['error'],
                raw_response=result.get('raw_response', '')
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Example usage endpoint
@app.get("/examples")
async def get_examples():
    """Get example requests"""
    return {
        "examples": [
            {
                "name": "Simple Text",
                "compose_code": 'Text("Hello World")',
                "expected_output": {"type": "Text", "text": "Hello World"}
            },
            {
                "name": "Button with Text",
                "compose_code": 'Button(onClick = { }) { Text("Click me") }',
                "expected_output": {
                    "type": "Button",
                    "onClick": "",
                    "children": [{"type": "Text", "text": "Click me"}]
                }
            },
            {
                "name": "Column Layout",
                "compose_code": 'Column { Text("Title") Text("Subtitle") }',
                "expected_output": {
                    "type": "Column",
                    "children": [
                        {"type": "Text", "text": "Title"},
                        {"type": "Text", "text": "Subtitle"}
                    ]
                }
            },
            {
                "name": "Persian Text",
                "compose_code": 'Text("سلام دنیا")',
                "expected_output": {"type": "Text", "text": "سلام دنیا"}
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)