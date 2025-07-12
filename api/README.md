# Compose to JSON API

FastAPI service for converting Jetpack Compose code to JSON.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install fastapi uvicorn requests
```

### 2. Set Environment Variables
Make sure `.env` file exists with:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Run Server
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API
- **API URL**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### GET `/`
Root endpoint with API information

### GET `/health`
Health check endpoint

### GET `/info`
Get converter information and capabilities

### GET `/examples`
Get example requests and expected outputs

### POST `/convert`
Convert Compose code to JSON

**Request Body:**
```json
{
  "compose_code": "Text(\"Hello World\")"
}
```

**Response:**
```json
{
  "success": true,
  "input": "Text(\"Hello World\")",
  "output": {
    "type": "Text",
    "text": "Hello World"
  }
}
```

## 🧪 Testing

### Manual Testing
```bash
# Test with curl
curl -X POST "http://localhost:8000/convert" \
     -H "Content-Type: application/json" \
     -d '{"compose_code": "Text(\"Hello World\")"}'
```

### Automated Testing
```bash
cd api
python test_api.py
```

## 📝 Example Usage

### Python Client
```python
import requests

# Convert Compose code
data = {"compose_code": 'Text("Hello World")'}
response = requests.post("http://localhost:8000/convert", json=data)
result = response.json()

if result['success']:
    print(result['output'])
```

### JavaScript Client
```javascript
const response = await fetch('http://localhost:8000/convert', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    compose_code: 'Text("Hello World")'
  })
});

const result = await response.json();
console.log(result.output);
```

## 🔧 Configuration

- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 8000
- **Reload**: Enabled in development
- **API Key**: From environment variable `GEMINI_API_KEY`

## 🎯 Supported Features

- ✅ Text conversion
- ✅ Button conversion
- ✅ Layout conversion (Column, Row, Box)
- ✅ Persian text support
- ✅ Few-shot learning (22 training examples)
- ✅ Error handling
- ✅ Input validation

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "input": "original_compose_code",
  "output": {
    "type": "ComponentType",
    "properties": "..."
  }
}
```

### Error Response
```json
{
  "success": false,
  "input": "original_compose_code",
  "error": "error_message",
  "raw_response": "raw_ai_response"
}
``` 