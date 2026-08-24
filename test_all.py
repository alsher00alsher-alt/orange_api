import requests
import json
import time

print("="*60)
print("🧪 اختبار شامل لكل خدمات AI FOR YOU")
print("="*60)

# ============ 1. اختبار الشات ============
print("\n1️⃣ اختبار الشات:")
SUPABASE_URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'

models = [
    "google/gemini-2.5-flash",
    "google/gemini-2.5-pro",
    "openai/gpt-5-nano",
    "openai/gpt-5",
    "anthropic/claude-sonnet-5",
]

for model in models:
    try:
        payload = {"messages":[{"role":"user","content":"اهلا"}],"model":model}
        r = requests.post(SUPABASE_URL, json=payload, timeout=30)
        if r.status_code == 200:
            print(f"  ✅ {model} → شغال")
        else:
            print(f"  ❌ {model} → {r.status_code}")
    except Exception as e:
        print(f"  ❌ {model} → {e}")

# ============ 2. اختبار تعديل الصور ============
print("\n2️⃣ اختبار تعديل الصور:")
IMAGE_EDIT_URL = 'https://shorts.multiplewords.in/mwvideos/api/edit_image_from_text'

import random, string, base64

def generate_auth():
    s = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    s += ''.join(random.choice(string.digits) for _ in range(5))
    s += ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return base64.b64encode(s.encode()).decode()

# صورة اختبار صغيرة
test_image = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
)

files = {'file': ('test.jpg', test_image, 'image/jpeg')}
data = {'prompt': 'Make it more beautiful', 'user_id': '1'}
headers = {
    'authorization': generate_auth(),
    'x-forwarded-for': f'{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}'
}

try:
    r = requests.post(IMAGE_EDIT_URL, headers=headers, files=files, data=data, timeout=30)
    result = r.json()
    if result.get('edited_image_url'):
        print(f"  ✅ تعديل الصور شغال")
        print(f"  🔗 {result['edited_image_url'][:80]}...")
    else:
        print(f"  ❌ فشل: {str(result)[:200]}")
except Exception as e:
    print(f"  ❌ {e}")

# ============ 3. اختبار توليد الصور ============
print("\n3️⃣ اختبار توليد الصور:")

# Agnes
AGNES_KEY = 'sk-eV8aSN0NWxNYGnTdvws5nIGAcMWvUk0G2i0u5MdGIdyl2H1Q'
try:
    r = requests.post(
        'https://apihub.agnes-ai.com/v1/images/generations',
        headers={'Authorization': 'Bearer ' + AGNES_KEY, 'Content-Type': 'application/json'},
        json={'model':'agnes-image-2.1-flash','prompt':'cat','size':'1K','ratio':'1:1','extra_body':{'response_format':'url'}},
        timeout=30
    )
    data = r.json()
    if data.get('data'):
        print(f"  ✅ Agnes صور شغال")
    else:
        print(f"  ❌ Agnes صور فشل: {str(data)[:100]}")
except Exception as e:
    print(f"  ❌ Agnes: {e}")

# ============ 4. اختبار توليد الفيديو ============
print("\n4️⃣ اختبار توليد الفيديو:")
try:
    r = requests.post(
        'https://apihub.agnes-ai.com/v1/videos',
        headers={'Authorization': 'Bearer ' + AGNES_KEY, 'Content-Type': 'application/json'},
        json={'model':'agnes-video-v2.0','prompt':'cat running','num_frames':81,'frame_rate':24},
        timeout=30
    )
    data = r.json()
    if data.get('video_id'):
        print(f"  ✅ Agnes فيديو شغال")
        print(f"  🎬 Video ID: {data['video_id']}")
    else:
        print(f"  ❌ Agnes فيديو فشل: {str(data)[:100]}")
except Exception as e:
    print(f"  ❌ Agnes فيديو: {e}")

# ============ 5. اختبار Nexus ============
print("\n5️⃣ اختبار Nexus:")
NEXII_KEY = 'sk-e0683fb0c7af3fc6-dcdb07-72c65552'
try:
    r = requests.post(
        'https://ai.nexii.cloud/v1/chat/completions',
        headers={'Authorization': 'Bearer ' + NEXII_KEY, 'Content-Type': 'application/json'},
        json={'model':'auto/best-chat','messages':[{'role':'user','content':'اهلا'}],'max_tokens':100},
        timeout=30
    )
    if r.status_code == 200:
        print(f"  ✅ Nexus شغال")
    else:
        print(f"  ❌ Nexus فشل: {r.status_code}")
except Exception as e:
    print(f"  ❌ Nexus: {e}")

print("\n" + "="*60)
print("✅ الاختبار خلص")
print("="*60)
