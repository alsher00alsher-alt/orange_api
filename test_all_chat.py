import requests
import json
import base64
import time

print("="*60)
print("🤖 اختبار جميع النماذج - رسالة: مرحبا")
print("="*60)

URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'

models = [
    {"name": "Gemini Flash Image", "id": "google/gemini-2.5-flash-image"},
    {"name": "Gemini Flash", "id": "google/gemini-2.5-flash"},
    {"name": "Gemini Flash Lite", "id": "google/gemini-2.5-flash-lite"},
    {"name": "Gemini Pro", "id": "google/gemini-2.5-pro"},
    {"name": "GPT-5 Nano", "id": "openai/gpt-5-nano"},
    {"name": "GPT-5 Mini", "id": "openai/gpt-5-mini"},
    {"name": "GPT-5", "id": "openai/gpt-5"},
    {"name": "Claude Haiku", "id": "anthropic/claude-3-5-haiku-20241022"},
    {"name": "Claude Sonnet 4.5", "id": "anthropic/claude-sonnet-4-5"},
    {"name": "Claude Opus 4.1", "id": "anthropic/claude-opus-4-1-20250805"},
    {"name": "Claude Sonnet 5", "id": "anthropic/claude-sonnet-5"},
    {"name": "Claude Fable 5", "id": "anthropic/claude-fable-5"},
]

def test_model(model_info, prompt="مرحبا"):
    name = model_info["name"]
    model_id = model_info["id"]
    
    print(f"\n{'='*50}")
    print(f"🎯 {name}")
    print(f"📝 الموديل: {model_id}")
    print(f"{'='*50}")
    
    payload = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "model": model_id
    }
    
    try:
        response = requests.post(URL, json=payload, timeout=30, stream=True)
        
        if response.status_code >= 400:
            print(f"❌ فشل: {response.status_code}")
            try:
                print(f"   {response.text[:200]}")
            except:
                pass
            return False
        
        print("✅ الرد: ", end='', flush=True)
        
        for line in response.iter_lines():
            if not line or not line.startswith(b'data: '):
                continue
            
            data = line[6:]
            if data == b'[DONE]':
                break
            
            try:
                obj = json.loads(data)
                choices = obj.get('choices', [])
                
                if choices:
                    delta = choices[0].get('delta', {})
                    content = delta.get('content')
                    
                    if content:
                        print(content, end='', flush=True)
                        
            except json.JSONDecodeError:
                continue
        
        print()
        return True
        
    except requests.RequestException as e:
        print(f"❌ خطأ: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

# تشغيل الاختبارات
results = []
working = 0
failed = 0

for model in models:
    success = test_model(model)
    results.append({"name": model["name"], "success": success})
    
    if success:
        working += 1
    else:
        failed += 1
    
    time.sleep(2)

# عرض النتائج النهائية
print("\n" + "="*60)
print("📊 النتائج النهائية:")
print("="*60)

print(f"\n✅ الشغال: {working}")
print(f"❌ الفاشل: {failed}")

print("\n✅ النماذج الشغالة:")
for result in results:
    if result["success"]:
        print(f"  ✅ {result['name']}")

print("\n❌ النماذج الفاشلة:")
for result in results:
    if not result["success"]:
        print(f"  ❌ {result['name']}")

print("\n✅ انتهى")
