import json

def show_final_prompt():
    """نمایش پرامت نهایی که به AI ارسال می‌شود"""
    
    # بارگذاری dataset
    with open('compose_sdui_dataset.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ {len(data)} نمونه از dataset بارگذاری شد")
    
    # انتخاب ۵ نمونه اول برای few-shot
    examples = data[:5]
    
    # ساخت پرامت
    prompt_parts = [
        "شما یک متخصص تبدیل کد Jetpack Compose به JSON هستید.",
        "وظیفه شما تبدیل کد Compose به ساختار JSON مشخص‌شده است.",
        "",
        "قوانین تبدیل:",
        "1. هر component یک type دارد (مثل Text, Button, Column, Row, Box, Image)",
        "2. محتوای متنی در فیلد text قرار می‌گیرد", 
        "3. onClick functions در فیلد onClick قرار می‌گیرند",
        "4. modifier ها به صورت modifier.نام تبدیل می‌شوند",
        "5. children components در آرایه children قرار می‌گیرند",
        "",
        "نمونه‌های تبدیل:"
    ]
    
    # اضافه کردن نمونه‌ها
    for i, example in enumerate(examples, 1):
        prompt_parts.extend([
            f"",
            f"نمونه {i}:",
            f"ورودی: {example['input']}",
            f"خروجی: {json.dumps(example['output'], ensure_ascii=False)}"
        ])
    
    # کد نمونه برای تست
    test_input = 'Column { Text("عنوان") Button(onClick = {submit()}) { Text("ارسال") } }'
    
    prompt_parts.extend([
        "",
        "حالا کد زیر را تبدیل کنید:",
        f"ورودی: {test_input}",
        "خروجی:"
    ])
    
    final_prompt = "\n".join(prompt_parts)
    
    print("\n" + "="*60)
    print("🤖 پرامت نهایی که به Gemini ارسال می‌شود:")
    print("="*60)
    print(final_prompt)
    print("="*60)
    
    print(f"\n📊 آمار پرامت:")
    print(f"- تعداد خطوط: {len(prompt_parts)}")
    print(f"- تعداد کاراکتر: {len(final_prompt)}")
    print(f"- تعداد نمونه‌های آموزشی: {len(examples)}")
    
    print(f"\n🎯 نتیجه مورد انتظار برای '{test_input}':")
    expected = {
        "type": "Column",
        "children": [
            {"type": "Text", "text": "عنوان"},
            {
                "type": "Button", 
                "onClick": "submit",
                "children": [{"type": "Text", "text": "ارسال"}]
            }
        ]
    }
    print(json.dumps(expected, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    show_final_prompt() 