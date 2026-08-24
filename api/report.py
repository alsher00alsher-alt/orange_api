from flask import Flask, request, jsonify, Response
import requests
import time
import random

app = Flask(__name__)

COOKIES = "m_pixel_ratio=3; wd=408x907; c_user=61573411021653; locale=ar_AR; wl_cbv=v2%3Bclient_version%3A3258%3Btimestamp%3A1787574018; fbl_st=101032757%3BT%3A29792900; vpd=v1%3B756x408x3"

cookies = {}
for item in COOKIES.split('; '):
    if '=' in item:
        key, value = item.split('=', 1)
        cookies[key] = value

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/report', methods=['GET', 'OPTIONS'])
def report():
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    post_id = request.args.get('post_id', '')
    reason = request.args.get('reason', 'privacy')
    
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update({'user-agent': 'Mozilla/5.0 (Linux; Android 14)'})
    
    try:
        url = "https://m.facebook.com/a/report.php"
        resp = session.get(url, params={'content_id': post_id, 'report_type': reason}, timeout=5)
        
        # فحص لو المنشور اتحظر
        check = session.get(f"https://m.facebook.com/story.php?story_fbid={post_id}", timeout=5)
        banned = "هذا المحتوى غير متاح" in check.text or "This content isn't available" in check.text
        
        return jsonify({"success": resp.status_code == 200, "banned": banned})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
