import json

def clean_value(value):
    """Clean values to ensure consistent JSON output"""
    if value is None:
        return ""
    if isinstance(value, bool):
        return value
    return value

def clean_dict(data):
    """Recursively clean dictionary values"""
    if isinstance(data, dict):
        return {key: clean_dict(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_dict(item) for item in data]
    else:
        return clean_value(data)

data = [
    {
        "input": 'Text("سلام دنیا")',
        "output": {"type": "Text", "text": "سلام دنیا"}
    },
    {
        "input": 'Button(onClick = { doSomething() }) { Text("ورود") }',
        "output": {
            "type": "Button",
            "onClick": "doSomething",
            "children": [{"type": "Text", "text": "ورود"}]
        }
    },
    {
        "input": 'Column { Text("عنوان") }',
        "output": {
            "type": "Column",
            "children": [{"type": "Text", "text": "عنوان"}]
        }
    },
    {
        "input": 'Row { Button(onClick = { }) { Text("تایید") } }',
        "output": {
            "type": "Row",
            "children": [
                {
                    "type": "Button",
                    "onClick": "",
                    "children": [{"type": "Text", "text": "تایید"}]
                }
            ]
        }
    },
    {
        "input": 'Box { Text("داخل باکس") }',
        "output": {
            "type": "Box",
            "children": [{"type": "Text", "text": "داخل باکس"}]
        }
    },
    {
        "input": 'Image(painter = painterResource(id = R.drawable.ic_logo), contentDescription = "لوگو")',
        "output": {
            "type": "Image",
            "src": "R.drawable.ic_logo",
            "contentDescription": "لوگو"
        }
    },
    {
        "input": 'Column(modifier = Modifier.fillMaxWidth()) { Text("تست") }',
        "output": {
            "type": "Column",
            "modifier.fillMaxWidth": True,
            "children": [{"type": "Text", "text": "تست"}]
        }
    },
    {
        "input": 'Row(modifier = Modifier.padding(8.dp)) { Text("مقدار") }',
        "output": {
            "type": "Row",
            "modifier.padding": 8,
            "children": [{"type": "Text", "text": "مقدار"}]
        }
    },
    {
        "input": 'Column { Text("متن بالا") Text("متن پایین") }',
        "output": {
            "type": "Column",
            "children": [
                {"type": "Text", "text": "متن بالا"},
                {"type": "Text", "text": "متن پایین"}
            ]
        }
    },
    {
        "input": 'Box(modifier = Modifier.size(100.dp)) { Text("100 در 100") }',
        "output": {
            "type": "Box",
            "modifier.size": 100,
            "children": [{"type": "Text", "text": "100 در 100"}]
        }
    },
    {
        "input": 'Button(onClick = { submitForm() }) { Text("ارسال") }',
        "output": {
            "type": "Button",
            "onClick": "submitForm",
            "children": [{"type": "Text", "text": "ارسال"}]
        }
    },
    {
        "input": 'Text("عدد 123")',
        "output": {"type": "Text", "text": "عدد 123"}
    },
    {
        "input": 'Row { Text("A") Text("B") }',
        "output": {
            "type": "Row",
            "children": [
                {"type": "Text", "text": "A"},
                {"type": "Text", "text": "B"}
            ]
        }
    },
    {
        "input": 'Column { Button(onClick = {}) { Text("کلیک") } }',
        "output": {
            "type": "Column",
            "children": [
                {
                    "type": "Button",
                    "onClick": "",
                    "children": [{"type": "Text", "text": "کلیک"}]
                }
            ]
        }
    },
    {
        "input": 'Text(text = "نمایش متن", color = Color.Red)',
        "output": {
            "type": "Text",
            "text": "نمایش متن",
            "color": "Red"
        }
    },
    {
        "input": 'Image(painter = rememberAsyncImagePainter("url"), contentDescription = null)',
        "output": {
            "type": "Image",
            "src": "url",
            "contentDescription": ""
        }
    },
    {
        "input": 'ConstraintLayout { val text = createRef(); Text("ساده", Modifier.constrainAs(text) {}) }',
        "output": {
            "type": "ConstraintLayout",
            "children": [
                {
                    "type": "Text",
                    "text": "ساده",
                    "modifier.constrainAs": "text"
                }
            ]
        }
    },
    {
        "input": 'Box(modifier = Modifier.padding(16.dp)) { Image(...) }',
        "output": {
            "type": "Box",
            "modifier.padding": 16,
            "children": [{"type": "Image"}]
        }
    },
    {
        "input": 'Text("یک متن دیگر")',
        "output": {"type": "Text", "text": "یک متن دیگر"}
    },
    {
        "input": 'Column(modifier = Modifier.fillMaxSize()) { Text("بالا") Text("پایین") }',
        "output": {
            "type": "Column",
            "modifier.fillMaxSize": True,
            "children": [
                {"type": "Text", "text": "بالا"},
                {"type": "Text", "text": "پایین"}
            ]
        }
    },
    {
        "input": 'Button(onClick = { println("کلیک شد") }) { Text("کلیک") }',
        "output": {
            "type": "Button",
            "onClick": 'println("کلیک شد")',
            "children": [{"type": "Text", "text": "کلیک"}]
        }
    },
    {
        "input": 'Row(modifier = Modifier.fillMaxWidth()) { Button(onClick = {}) { Text("تایید") } }',
        "output": {
            "type": "Row",
            "modifier.fillMaxWidth": True,
            "children": [
                {
                    "type": "Button",
                    "onClick": "",
                    "children": [{"type": "Text", "text": "تایید"}]
                }
            ]
        }
    }
]

# Clean the data and write to file as JSON array
with open("compose_sdui_dataset.json", "w", encoding="utf-8") as f:
    cleaned_data = [clean_dict(item) for item in data]
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
