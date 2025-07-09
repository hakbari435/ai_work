import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# بارگذاری تنظیمات از فایل .env
load_dotenv()

class ComposeToJsonAI:
    def __init__(self):
        # تنظیم API key
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyC510zTsiMR5emEDt0cZSmyvtDC5tMQcZ4')
        genai.configure(api_key=api_key)
        
        # تنظیم مدل
        self.model = genai.GenerativeModel('gemini-pro')
        
        # بارگذاری نمونه‌های آموزشی
        self.load_training_examples()
        
        # ساخت پرامت اولیه
        self.create_prompt_template()
    
    def load_training_examples(self):
        """بارگذاری نمونه‌های آموزشی از فایل JSON"""
        try:
            with open('compose_sdui_dataset.json', 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
        except FileNotFoundError:
            print("فایل dataset پیدا نشد!")
            self.training_data = []
    
    def create_prompt_template(self):
        """ساخت پرامت Few-shot با استفاده از نمونه‌های آموزشی"""
        
        # انتخاب چند نمونه برای few-shot
        examples = self.training_data[:5]  # ۵ نمونه اول
        
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
        
        prompt_parts.extend([
            "",
            "حالا کد زیر را تبدیل کنید:",
            "ورودی: {input_code}",
            "خروجی:"
        ])
        
        self.prompt_template = "\n".join(prompt_parts)
    
    def convert_compose_to_json(self, compose_code):
        """تبدیل کد Compose به JSON"""
        try:
            # ساخت پرامت نهایی
            prompt = self.prompt_template.format(input_code=compose_code)
            
            # ارسال درخواست به Gemini
            response = self.model.generate_content(prompt)
            
            # پردازش پاسخ
            result_text = response.text.strip()
            
            # تلاش برای parse کردن JSON
            try:
                result_json = json.loads(result_text)
                return {
                    'success': True,
                    'input': compose_code,
                    'output': result_json,
                    'raw_response': result_text
                }
            except json.JSONDecodeError:
                # اگر پاسخ JSON معتبر نبود، سعی کنیم آن را اصلاح کنیم
                cleaned_text = self.clean_json_response(result_text)
                try:
                    result_json = json.loads(cleaned_text)
                    return {
                        'success': True,
                        'input': compose_code,
                        'output': result_json,
                        'raw_response': result_text,
                        'cleaned': True
                    }
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'input': compose_code,
                        'error': 'پاسخ JSON معتبر نیست',
                        'raw_response': result_text
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'input': compose_code,
                'error': str(e)
            }
    
    def clean_json_response(self, text):
        """تمیز کردن پاسخ برای تبدیل به JSON معتبر"""
        # حذف متن اضافی قبل و بعد از JSON
        lines = text.split('\n')
        json_lines = []
        json_started = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('{') or stripped.startswith('['):
                json_started = True
            
            if json_started:
                json_lines.append(line)
                
            if json_started and (stripped.endswith('}') or stripped.endswith(']')):
                break
        
        return '\n'.join(json_lines)
    
    def test_on_dataset(self, limit=5):
        """تست مدل روی چند نمونه از dataset"""
        results = []
        
        test_samples = self.training_data[5:5+limit]  # نمونه‌های تست (غیر از آموزشی)
        
        for sample in test_samples:
            result = self.convert_compose_to_json(sample['input'])
            
            # مقایسه با نتیجه مورد انتظار
            if result['success']:
                expected = sample['output']
                actual = result['output']
                is_correct = expected == actual
                
                result['expected'] = expected
                result['is_correct'] = is_correct
            
            results.append(result)
            
        return results
    
    def evaluate_results(self, results):
        """ارزیابی نتایج تست"""
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        correct = sum(1 for r in results if r.get('is_correct', False))
        
        print(f"نتایج ارزیابی:")
        print(f"تعداد کل نمونه‌ها: {total}")
        print(f"تعداد پاسخ‌های موفق: {successful}")
        print(f"تعداد پاسخ‌های صحیح: {correct}")
        print(f"درصد موفقیت: {(successful/total)*100:.1f}%")
        print(f"درصد صحت: {(correct/total)*100:.1f}%")
        
        return {
            'total': total,
            'successful': successful,
            'correct': correct,
            'success_rate': (successful/total)*100,
            'accuracy_rate': (correct/total)*100
        }

def main():
    """تابع اصلی برای تست"""
    print("راه‌اندازی مدل تبدیل Compose به JSON...")
    
    # ایجاد نمونه از کلاس
    converter = ComposeToJsonAI()
    
    # تست یک نمونه ساده
    test_input = 'Text("سلام دنیا")'
    print(f"\nتست نمونه: {test_input}")
    
    result = converter.convert_compose_to_json(test_input)
    
    if result['success']:
        print("✅ موفق:")
        print(json.dumps(result['output'], ensure_ascii=False, indent=2))
    else:
        print("❌ خطا:")
        print(result['error'])
        print("پاسخ خام:", result.get('raw_response', 'ندارد'))

if __name__ == "__main__":
    main() 