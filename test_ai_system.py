import json

class MockComposeToJsonAI:
    """نسخه شبیه‌سازی‌شده برای تست بدون API"""
    
    def __init__(self):
        self.load_training_examples()
        self.create_prompt_template()
    
    def load_training_examples(self):
        """بارگذاری نمونه‌های آموزشی از فایل JSON"""
        try:
            with open('compose_sdui_dataset.json', 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            print(f"✅ {len(self.training_data)} نمونه آموزشی بارگذاری شد")
        except FileNotFoundError:
            print("❌ فایل dataset پیدا نشد!")
            self.training_data = []
    
    def create_prompt_template(self):
        """ساخت پرامت Few-shot"""
        examples = self.training_data[:5]
        
        prompt_parts = [
            "شما یک متخصص تبدیل کد Jetpack Compose به JSON هستید.",
            "وظیفه شما تبدیل کد Compose به ساختار JSON مشخص‌شده است.",
            "",
            "قوانین تبدیل:",
            "1. هر component یک type دارد",
            "2. محتوای متنی در فیلد text قرار می‌گیرد", 
            "3. onClick functions در فیلد onClick قرار می‌گیرند",
            "4. modifier ها به صورت modifier.نام تبدیل می‌شوند",
            "5. children components در آرایه children قرار می‌گیرند",
            "",
            "نمونه‌های تبدیل:"
        ]
        
        for i, example in enumerate(examples, 1):
            prompt_parts.extend([
                f"",
                f"نمونه {i}:",
                f"ورودی: {example['input']}",
                f"خروجی: {json.dumps(example['output'], ensure_ascii=False)}"
            ])
        
        prompt_parts.extend([
            "",
            "حالا کد زیر را تبدیل کنید:",
            "ورودی: {input_code}",
            "خروجی:"
        ])
        
        self.prompt_template = "\n".join(prompt_parts)
        print("✅ پرامت Few-shot آماده شد")
    
    def show_prompt_example(self, compose_code):
        """نمایش پرامت نهایی برای یک ورودی"""
        prompt = self.prompt_template.format(input_code=compose_code)
        print("\n" + "="*50)
        print("پرامت نهایی که به AI ارسال می‌شود:")
        print("="*50)
        print(prompt)
        print("="*50)
    
    def mock_convert(self, compose_code):
        """شبیه‌سازی تبدیل (برای تست ساختار)"""
        # در اینجا معمولاً درخواست به AI ارسال می‌شود
        # فعلاً فقط نشان می‌دهیم که چه پرامتی ارسال می‌شود
        
        self.show_prompt_example(compose_code)
        
        # سعی کنیم پاسخ را از dataset پیدا کنیم
        for item in self.training_data:
            if item['input'] == compose_code:
                return {
                    'success': True,
                    'input': compose_code,
                    'output': item['output'],
                    'source': 'dataset'
                }
        
        return {
            'success': False,
            'input': compose_code,
            'error': 'این نمونه در dataset موجود نیست'
        }
    
    def test_examples(self):
        """تست چند نمونه از dataset"""
        print("\n🧪 شروع تست نمونه‌ها:")
        
        if not self.training_data:
            print("❌ هیچ داده‌ای برای تست موجود نیست")
            return
            
        test_samples = self.training_data[:3]  # ۳ نمونه اول
        
        for i, sample in enumerate(test_samples, 1):
            print(f"\n--- تست {i} ---")
            print(f"ورودی: {sample['input']}")
            
            # فقط پرامت را نشان بده، تبدیل انجام نده
            print("✅ نتیجه مورد انتظار:")
            print(json.dumps(sample['output'], ensure_ascii=False, indent=2))

def show_system_architecture():
    """نمایش معماری سیستم"""
    print("🏗️ معماری سیستم AI:")
    print("""
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   کد Compose    │───▶│   پرامت AI     │───▶│   JSON خروجی   │
    │  Text("سلام")   │    │  Few-shot       │    │ {"type":"Text"} │
    └─────────────────┘    │  + Examples     │    └─────────────────┘
                           │  + Rules        │
                           └─────────────────┘
    
    مراحل:
    1️⃣ بارگذاری dataset آموزشی
    2️⃣ ساخت پرامت Few-shot با نمونه‌ها
    3️⃣ ارسال ورودی + پرامت به AI (Gemini)
    4️⃣ پردازش و تمیز کردن پاسخ
    5️⃣ برگرداندن JSON نهایی
    """)

def main():
    """تابع اصلی"""
    print("🚀 سیستم تبدیل Compose به JSON")
    print("================================")
    
    # نمایش معماری
    show_system_architecture()
    
    # ایجاد نمونه تست
    ai_system = MockComposeToJsonAI()
    
    # تست چند نمونه
    ai_system.test_examples()
    
    print("\n📝 مرحله بعدی:")
    print("1. دریافت API key از Gemini")
    print("2. جایگزینی MockComposeToJsonAI با ComposeToJsonAI واقعی")
    print("3. تست روی نمونه‌های جدید")
    print("4. بهبود prompt و افزایش دقت")

if __name__ == "__main__":
    main() 