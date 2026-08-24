import requests
import json

print("="*50)
print("🧪 اختبار DeepSeek")
print("="*50)

TOKEN = "/Kb254CgtERhGauIVrFG3OZaukSW5DF7CvHhgtp1nyeGDjx+NXt6fB6Raf7g780v"
POW_API = "https://dark.ps/deepseek/pow"

prompt = input("📝 اكتب سؤالك: ").strip()

headers = {
    'authorization': f'Bearer {TOKEN}',
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
    'origin': 'https://chat.deepseek.com',
    'referer': 'https://chat.deepseek.com/',
    'content-type': 'application/json',
}

# Session
r = requests.post('https://chat.deepseek.com/api/v0/chat_session/create', headers=headers, json={}, timeout=30)
session_id = r.json()['data']['biz_data']['id']
print(f"✅ Session: {session_id[:10]}...")

# PoW
r = requests.post('https://chat.deepseek.com/api/v0/chat/create_pow_challenge', headers=headers, json={'target_path': '/api/v0/chat/completion'}, timeout=30)
challenge = r.json()['data']['biz_data']['challenge']
r = requests.post(POW_API, json={'challenge': challenge}, timeout=120)
pow_resp = r.json()['x-ds-pow-response']
headers['x-ds-pow-response'] = pow_resp
print(f"✅ PoW: {pow_resp[:20]}...")

# إرسال
payload = {
    'chat_session_id': session_id,
    'prompt': prompt,
    'ref_file_ids': [],
    'thinking_enabled': False,
    'search_enabled': False,
}

print("⏳ إرسال...")
r = requests.post('https://chat.deepseek.com/api/v0/chat/completion', headers=headers, json=payload, timeout=60, stream=True)
print(f"Status: {r.status_code}")
print("="*50)

full_text = ""

for line in r.iter_lines():
    if not line:
        continue
    text = line.decode('utf-8', errors='ignore')
    
    if text.startswith('data:'):
        data_str = text[5:].strip()
        if not data_str or data_str == '[DONE]':
            continue
        try:
            obj = json.loads(data_str)
            
            # استخراج النص
            if 'v' in obj and isinstance(obj['v'], str):
                content = obj['v']
                
                # لو مش تفكير
                if 'p' in obj and obj['p'] == 'response/thinking_content':
                    print(f"\033[90m{content}\033[0m", end='', flush=True)
                else:
                    full_text += content
                    print(content, end='', flush=True)
                    
        except:
            continue

print("\n" + "="*50)
print(f"✅ الرد ({len(full_text)} حرف)")
print("✅ انتهى")
