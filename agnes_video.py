import requests
import time

print("🎬 Agnes Video Generator")
print("="*50)

AGNES_KEY = 'sk-eV8aSN0NWxNYGnTdvws5nIGAcMWvUk0G2i0u5MdGIdyl2H1Q'

prompt = input("📝 اكتب وصف الفيديو: ").strip()

print("\n⏳ جاري إنشاء الفيديو...")

try:
    # طلب توليد فيديو
    resp = requests.post(
        'https://apihub.agnes-ai.com/v1/videos',
        headers={'Authorization': 'Bearer ' + AGNES_KEY, 'Content-Type': 'application/json'},
        json={'model': 'agnes-video-v2.0', 'prompt': prompt, 'num_frames': 81, 'frame_rate': 24},
        timeout=60
    )
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:500]}")
    
    if resp.status_code == 200:
        data = resp.json()
        video_id = data.get('video_id') or data.get('id', '')
        
        if video_id:
            print(f"\n✅ Video ID: {video_id}")
            print("⏳ جاري التحقق من الحالة...")
            
            # نستنى ونشوف الحالة
            for i in range(10):
                time.sleep(10)
                status_resp = requests.get(
                    f'https://apihub.agnes-ai.com/agnesapi?video_id={video_id}',
                    headers={'Authorization': 'Bearer ' + AGNES_KEY},
                    timeout=30
                )
                status_data = status_resp.json()
                status = status_data.get('status', 'unknown')
                print(f"— {status}")
                
                if status == 'completed':
                    url = status_data.get('metadata', {}).get('url') or status_data.get('url', '')
                    print(f"\n✅ الفيديو جاهز: {url}")
                    break
                elif status == 'failed':
                    print("❌ فشل")
                    break
        else:
            print("❌ مفيش video_id")
    else:
        print("❌ فشل الطلب")
        
except Exception as e:
    print(f"❌ خطأ: {e}")
