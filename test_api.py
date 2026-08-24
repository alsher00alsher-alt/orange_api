import requests
import json

print("="*50)
print("🧪 اختبار الـ API")
print("="*50)

SUPABASE_URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'

prompt = input("📝 اكتب سؤالك: ").strip()
model = input("🎯 النموذج (افتراضي openai/gpt-5-nano): ").strip() or "openai/gpt-5-nano"

payload = {
    "messages": [{"role": "user", "content": prompt}],
    "model": model
}

print(f"\n⏳ إرسال للموديل: {model}")
print("="*50)

try:
    response = requests.post(SUPABASE_URL, json=payload, timeout=60, stream=True)
    print(f"Status: {response.status_code}")
    print("="*50)
    
    full_text = ""
    
    for line in response.iter_lines():
        if not line:
            continue
        text = line.decode('utf-8', errors='ignore')
        
        if text.startswith('data:'):
            data = text[5:].strip()
            if data == '[DONE]':
                break
            try:
                obj = json.loads(data)
                delta = obj.get('choices', [{}])[0].get('delta', {})
                content = delta.get('content', '')
                if content:
                    full_text += content
                    print(content, end='', flush=True)
            except:
                continue
    
    print("\n" + "="*50)
    print(f"✅ النص الكامل ({len(full_text)} حرف):")
    print(full_text[:200])
    
except Exception as e:
    print(f"❌ خطأ: {e}")

print("\n✅ انتهى")
