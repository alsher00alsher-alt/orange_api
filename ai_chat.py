import requests
import json
import base64

print("="*50)
print("🤖 AI Chat + Image Generator")
print("="*50)

URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'

models = {
    "1": "google/gemini-2.5-flash-image",
    "2": "google/gemini-2.5-flash",
    "3": "google/gemini-2.5-pro",
    "4": "openai/gpt-5-mini",
    "5": "openai/gpt-5",
    "6": "anthropic/claude-sonnet-4-5",
    "7": "anthropic/claude-opus-4-1",
}

print("\n📋 النماذج:")
print("1. Gemini Flash Image (صور + شات)")
print("2. Gemini Flash (شات سريع)")
print("3. Gemini Pro (شات قوي)")
print("4. GPT-5 Mini")
print("5. GPT-5")
print("6. Claude Sonnet 4.5")
print("7. Claude Opus 4.1")

choice = input("\n🎯 اختار الموديل (1-7): ").strip()
model = models.get(choice, "google/gemini-2.5-flash")

prompt = input("📝 اكتب سؤالك أو وصف الصورة: ").strip()

payload = {
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "model": model
}

print(f"\n⏳ جاري الإرسال...")
print(f"🎯 الموديل: {model}")

try:
    response = requests.post(URL, json=payload, timeout=60, stream=True)
    
    if response.status_code >= 400:
        print(f"❌ فشل: {response.text[:500]}")
        exit()
    
    print("\n✅ الرد:\n")
    
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
                images = delta.get('images', [])
                
                if images:
                    url = images[0].get('image_url', {}).get('url', '')
                    
                    if url.startswith('data:image/'):
                        header, base64_data = url.split(',', 1)
                        ext = header.split('/')[1].split(';')[0]
                        filename = f"generated.{ext}"
                        
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(base64_data))
                        
                        print(f"\n🖼️ تم حفظ الصورة: {filename}")
                else:
                    content = delta.get('content')
                    if content:
                        print(content, end='', flush=True)
                        
        except json.JSONDecodeError:
            continue
    
    print("\n\n✅ انتهى")
    
except Exception as e:
    print(f"❌ خطأ: {e}")
