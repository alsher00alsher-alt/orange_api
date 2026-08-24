import requests
import time
import json

print("="*60)
print("🎬 اختبار جميع نماذج الفيديو")
print("="*60)

prompt = input("📝 اكتب الوصف: ").strip()
if not prompt:
    prompt = "cat and dog playing"

By = "dark.ps"

# جميع النماذج
video_models = [
    {"name": "veo3.1-pro", "duration": 4, "aspect": "16:9", "quality": "1080p"},
    {"name": "veo3.1-fast", "duration": 4, "aspect": "16:9", "quality": "1080p"},
    {"name": "sora-2", "duration": 4, "aspect": "16:9", "quality": "1080p"},
    {"name": "sora-2-pro", "duration": 4, "aspect": "16:9", "quality": "1080p"},
    {"name": "gemini-omni-flash", "duration": 5, "aspect": "16:9", "quality": "1080p"},
    {"name": "flux-3-video", "duration": 4, "aspect": "16:9", "quality": "1080p"},
]

image_models = [
    {"name": "flux-2", "aspect": "1:1"},
    {"name": "nano-banana-pro", "aspect": "1:1", "quality": "2K"},
    {"name": "gpt-image-2", "aspect": "1:1"},
]

def test_video_model(model_info):
    name = model_info["name"]
    duration = model_info["duration"]
    aspect = model_info["aspect"]
    quality = model_info["quality"]
    
    print(f"\n{'='*50}")
    print(f"🎯 تجربة: {name}")
    print(f"{'='*50}")
    
    url = f"https://{By}/synthesia"
    
    payload = {
        "model": name,
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": aspect,
        "resolution": quality
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        print(f"❌ فشل الاتصال: {e}")
        return None
    
    if response.status_code != 202:
        try:
            error = response.json()
            print(f"❌ فشل: {error.get('error', response.text[:200])}")
        except:
            print(f"❌ فشل: {response.text[:200]}")
        return None
    
    task_id = response.json().get("task_id")
    print(f"✅ Task ID: {task_id}")
    print("⏳ جاري المعالجة...")
    
    # نستنى شوية ونشوف النتيجة
    for i in range(5):
        time.sleep(15)
        try:
            check = requests.get(f"https://{By}/task/{task_id}", timeout=30)
            result = check.json()
            status = result.get("status", "unknown")
            print(f"— {status}")
            
            if status == "completed":
                print(f"✅ النتيجة: {result.get('media')}")
                return result.get('media')
            elif status == "failed":
                print(f"❌ فشل: {result.get('error')}")
                return None
        except:
            continue
    
    return None

def test_image_model(model_info):
    name = model_info["name"]
    aspect = model_info.get("aspect", "1:1")
    quality = model_info.get("quality", "2K")
    
    print(f"\n{'='*50}")
    print(f"🎨 تجربة صورة: {name}")
    print(f"{'='*50}")
    
    url = f"https://{By}/synthesia"
    
    payload = {
        "model": name,
        "prompt": prompt,
        "aspect_ratio": aspect,
        "quality": quality
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        print(f"❌ فشل الاتصال: {e}")
        return None
    
    if response.status_code != 202:
        try:
            error = response.json()
            print(f"❌ فشل: {error.get('error', response.text[:200])}")
        except:
            print(f"❌ فشل: {response.text[:200]}")
        return None
    
    task_id = response.json().get("task_id")
    print(f"✅ Task ID: {task_id}")
    print("⏳ جاري المعالجة...")
    
    for i in range(5):
        time.sleep(15)
        try:
            check = requests.get(f"https://{By}/task/{task_id}", timeout=30)
            result = check.json()
            status = result.get("status", "unknown")
            print(f"— {status}")
            
            if status == "completed":
                print(f"✅ النتيجة: {result.get('media')}")
                return result.get('media')
            elif status == "failed":
                print(f"❌ فشل: {result.get('error')}")
                return None
        except:
            continue
    
    return None

# تشغيل الاختبارات
results = {}

print("\n" + "="*60)
print("🎬 اختبار نماذج الفيديو...")
print("="*60)

for model in video_models:
    result = test_video_model(model)
    results[f"video: {model['name']}"] = result

print("\n" + "="*60)
print("🎨 اختبار نماذج الصور...")
print("="*60)

for model in image_models:
    result = test_image_model(model)
    results[f"image: {model['name']}"] = result

# عرض النتائج النهائية
print("\n" + "="*60)
print("📊 النتائج النهائية:")
print("="*60)

working = []
failed = []

for key, value in results.items():
    if value:
        working.append(key)
        print(f"✅ {key}: {value}")
    else:
        failed.append(key)
        print(f"❌ {key}: فشل")

print(f"\n📈 الشغال: {len(working)}")
print(f"📉 الفاشل: {len(failed)}")

if working:
    print(f"\n✅ النماذج الشغالة:")
    for w in working:
        print(f"  - {w}")

if failed:
    print(f"\n❌ النماذج الفاشلة:")
    for f in failed:
        print(f"  - {f}")
