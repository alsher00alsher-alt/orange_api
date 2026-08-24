import requests
import base64
import random
import string
import os

print("="*50)
print("🎨 اختبار تعديل الصور")
print("="*50)

# المسارات
image_path = input("📁 مسار الصورة (اتركه فاضي لاستخدام cat.jpg): ").strip()
if not image_path:
    image_path = "/storage/emulated/0/Download/cat.jpg"

if not os.path.exists(image_path):
    print(f"❌ الصورة غير موجودة: {image_path}")
    exit()

prompt = input("📝 وصف التعديل (اتركه فاضي لـ Make it more beautiful): ").strip()
if not prompt:
    prompt = "Make it more beautiful"

def generate_auth():
    s = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    s += ''.join(random.choice(string.digits) for _ in range(5))
    s += ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return base64.b64encode(s.encode()).decode()

url = 'https://shorts.multiplewords.in/mwvideos/api/edit_image_from_text'

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'authorization': generate_auth(),
    'origin': 'https://saifs.ai',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'x-forwarded-for': '.'.join(str(random.randint(1,254)) for _ in range(4))
}

print(f"\n📁 الصورة: {image_path}")
print(f"📝 التعديل: {prompt}")
print("⏳ جاري الرفع...")

try:
    with open(image_path, 'rb') as f:
        response = requests.post(
            url,
            headers=headers,
            files={'file': (image_path, f, 'image/jpeg')},
            data={'prompt': prompt, 'user_id': '1'},
            timeout=60
        )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if 'edited_image_url' in data:
            print(f"\n✅ تم التعديل!")
            print(f"🔗 الرابط: {data['edited_image_url']}")
            
            # تحميل الصورة
            print("⏳ تحميل الصورة...")
            img_response = requests.get(data['edited_image_url'])
            output_path = "/storage/emulated/0/Download/edited_test.jpg"
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            print(f"✅ تم الحفظ في: {output_path}")
        else:
            print(f"❌ مفيش edited_image_url")
            print(str(data)[:500])
    else:
        print(f"❌ فشل: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ خطأ: {e}")

print("\n✅ انتهى")
