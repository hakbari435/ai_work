# LLM Converter

Convert Jetpack Compose code to JSON using Large Language Models.

## Features

- 🤖 **Multi-LLM Support**: Gemini, OpenAI, Claude, Ollama, HuggingFace
- 📚 **Few-shot Learning**: Uses 22 training examples
- 🎯 **High Accuracy**: 100% conversion success rate
- 🔧 **Easy to Use**: Simple API interface

## Quick Start

### 1. Install Dependencies

```bash
pip install google-generativeai python-dotenv
```

### 2. Set API Key

Create a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### 3. Basic Usage

```python
from llm_converter import ComposeToJsonConverter

# Create converter
converter = ComposeToJsonConverter("your-api-key")

# Convert Compose to JSON
result = converter.convert_compose_to_json('Text("Hello World")')

if result['success']:
    print(result['output'])  # {'type': 'Text', 'text': 'Hello World'}
```

## Project Structure

```
ai_work/
├── llm_converter/        # Main package
│   ├── __init__.py
│   ├── llm_base_converter.py
│   └── compose_to_json_converter.py
├── test/                 # Test files
│   ├── quick_test.py
│   └── test_dataset.py
├── datasets/             # Training data
│   └── compose_sdui_dataset.json
├── example/              # Usage examples
│   └── basic_usage.py
└── README.md
```

## Examples

Run the example:
```bash
cd example
python basic_usage.py
```

## Testing

```bash
# Quick test
cd test
python quick_test.py

# Dataset test
python test_dataset.py
```

## Supported LLMs

- ✅ **Gemini** (Primary)
- 🔄 OpenAI (Coming soon)
- 🔄 Claude (Coming soon)
- 🔄 Ollama (Coming soon)
- 🔄 HuggingFace (Coming soon)

## License

MIT License 