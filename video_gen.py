import requests
import time
import json

print("="*50)
print("🎬 AI Video Generator")
print("="*50)

# الإعدادات
prompt = input("📝 اكتب وصف الفيديو: ").strip()
if not prompt:
    prompt = "cat and dog"

print("\n📋 النماذج المتاحة:")
print("1. veo3.1-pro (4-8 ثواني)")
print("2. veo3.1-fast (4-8 ثواني)")
print("3. sora-2 (4-8 ثواني)")
print("4. sora-2-pro (4-8 ثواني)")
print("5. gemini-omni-flash (3-10 ثواني)")
print("6. flux-3-video (4-20 ثانية)")

model_choice = input("\n🎯 اختار الموديل (1-6): ").strip()

models = {
    "1": "veo3.1-pro",
    "2": "veo3.1-fast",
    "3": "sora-2",
    "4": "sora-2-pro",
    "5": "gemini-omni-flash",
    "6": "flux-3-video"
}

model = models.get(model_choice, "gemini-omni-flash")

duration = input("⏱️ المدة بالثواني (3-20): ").strip() or "10"
aspect_ratio = input("📐 الأبعاد (16:9 أو 9:16): ").strip() or "16:9"
resolution = input("🎯 الجودة (720p/1080p): ").strip() or "1080p"

By = "dark.ps"

def generate_video():
    г = f"https://{By}/synthesia"
    о = f"https://{By}/task"
    
    п = {
        "model": model,
        "prompt": prompt,
        "duration": int(duration),
        "aspect_ratio": aspect_ratio,
        "resolution": resolution
    }
    
    print(f"\n⏳ جاري توليد الفيديو...")
    print(f"📝 الوصف: {prompt}")
    print(f"🎯 الموديل: {model}")
    print(f"⏱️ المدة: {duration} ثانية")
    print(f"📐 الأبعاد: {aspect_ratio}")
    print(f"🎯 الجودة: {resolution}")
    
    try:
        р = requests.post(г, json=п, timeout=60)
    except requests.RequestException:
        print("❌ فشل الاتصال")
        return
    
    if р.status_code != 202:
        try:
            е = р.json()
            print(е["error"] if "error" in е else р.text)
        except:
            print(р.text)
        return
    
    т = р.json()["task_id"]
    print(f"\n✅ Task ID: {т}")
    print("⏳ جاري المعالجة...")
    
    while True:
        try:
            с = requests.get(f"{о}/{т}", timeout=30)
            д = с.json()
        except (requests.RequestException, ValueError):
            time.sleep(10)
            continue
        
        if д["status"] == "completed":
            print(f"\n✅ تم التوليد!")
            print(f"🔗 رابط الفيديو: {д['media']}")
            break
        
        if д["status"] == "failed":
            print(f"❌ فشل: {д.get('error', 'Unknown error')}")
            break
        
        print(f"— {д['status']}")
        time.sleep(20)

generate_video()
