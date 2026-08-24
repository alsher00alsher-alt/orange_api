import requests
import time

AGNES_KEY = 'sk-eV8aSN0NWxNYGnTdvws5nIGAcMWvUk0G2i0u5MdGIdyl2H1Q'
VIDEO_ID = 'task_mIdmBMKsAebGCn0tOpUpwY3dEfIGGi0n'

print("⏳ فحص حالة الفيديو...")
print("="*50)

while True:
    try:
        resp = requests.get(
            f'https://apihub.agnes-ai.com/agnesapi?video_id={VIDEO_ID}',
            headers={'Authorization': 'Bearer ' + AGNES_KEY},
            timeout=30
        )
        data = resp.json()
        status = data.get('status', 'unknown')
        progress = data.get('progress', 0)
        
        print(f"📊 الحالة: {status} | التقدم: {progress}%")
        
        if status == 'completed':
            url = data.get('metadata', {}).get('url') or data.get('url', '')
            print(f"\n✅ الفيديو جاهز!")
            print(f"🔗 الرابط: {url}")
            break
        elif status == 'failed':
            print(f"\n❌ فشل: {data.get('error', '')}")
            break
        
        time.sleep(15)
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        time.sleep(15)
