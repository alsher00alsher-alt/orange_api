import requests
import json
import os

print("="*50)
print("🎙️ اختبار المكالمة الصوتية")
print("="*50)

SUPABASE_URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'

# 1. اختبار الشات (نص → رد)
print("\n1️⃣ اختبار الشات:")
prompt = input("📝 اكتب سؤالك: ").strip()

payload = {
    "messages": [{"role": "user", "content": prompt}],
    "model": "openai/gpt-5-nano"
}

print("⏳ جاري...")
response = requests.post(SUPABASE_URL, json=payload, timeout=60, stream=True)

full_text = ""
for line in response.iter_lines():
    if not line or not line.startswith(b'data: '):
        continue
    data = line[6:]
    if data == b'[DONE]':
        break
    try:
        obj = json.loads(data)
        delta = obj.get('choices', [{}])[0].get('delta', {})
        content = delta.get('content', '')
        if content:
            print(content, end='', flush=True)
            full_text += content
    except:
        continue

print("\n\n✅ انتهى الشات")

# 2. تحويل النص لصوت (TTS)
print("\n2️⃣ تحويل النص لصوت:")
print("⏳ جاري توليد الصوت...")

# نستخدم Voice.ai API
VOICE_API = 'https://tts-backend.voice.ai'
AGENT_ID = '142bb0d2-7f84-4b39-9c7e-69972d86c1e6'

headers = {
    'accept': '*/*',
    'origin': 'https://voice.ai',
    'referer': 'https://voice.ai/',
    'user-agent': 'Mozilla/5.0',
}

try:
    resp = requests.get(f"{VOICE_API}/api/v1/voice-agent/{AGENT_ID}/connection", headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ فيه token: {'participant_token' in data}")
    else:
        print(f"❌ {resp.text[:200]}")
except Exception as e:
    print(f"❌ {e}")

print("\n✅ انتهى الاختبار")
