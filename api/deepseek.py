from flask import Flask, request, jsonify, Response
import requests
import json
import os
import mimetypes

app = Flask(__name__)

TOKEN = "/Kb254CgtERhGauIVrFG3OZaukSW5DF7CvHhgtp1nyeGDjx+NXt6fB6Raf7g780v"
POW_API = "https://dark.ps/deepseek/pow"

def get_headers():
    return {
        'authorization': f'Bearer {TOKEN}',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        'origin': 'https://chat.deepseek.com',
        'referer': 'https://chat.deepseek.com/',
        'content-type': 'application/json',
    }

def solve_pow(target_path):
    headers = get_headers()
    r = requests.post('https://chat.deepseek.com/api/v0/chat/create_pow_challenge', headers=headers, json={'target_path': target_path}, timeout=30)
    challenge = r.json()['data']['biz_data']['challenge']
    r = requests.post(POW_API, json={'challenge': challenge}, timeout=120)
    return r.json()['x-ds-pow-response']

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/api/deepseek', methods=['POST', 'OPTIONS'])
def deepseek_chat():
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        thinking = data.get('thinking', False)
        search = data.get('search', False)
        files = data.get('files', [])
        
        headers = get_headers()
        
        # Session
        r = requests.post('https://chat.deepseek.com/api/v0/chat_session/create', headers=headers, json={}, timeout=30)
        session_id = r.json()['data']['biz_data']['id']
        
        # PoW للشات
        pow_resp = solve_pow('/api/v0/chat/completion')
        headers['x-ds-pow-response'] = pow_resp
        
        # إرسال
        payload = {
            'chat_session_id': session_id,
            'prompt': prompt,
            'ref_file_ids': files,
            'thinking_enabled': thinking,
            'search_enabled': search,
        }
        
        r = requests.post('https://chat.deepseek.com/api/v0/chat/completion', headers=headers, json=payload, timeout=120, stream=True)
        
        full_text = ""
        thinking_text = ""
        
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
                    if 'v' in obj and isinstance(obj['v'], str):
                        content = obj['v']
                        if 'p' in obj and obj['p'] == 'response/thinking_content':
                            thinking_text += content
                        else:
                            full_text += content
                except:
                    continue
        
        full_text = full_text.replace('FINISHED', '').strip()
        thinking_text = thinking_text.replace('FINISHED', '').strip()
        
        return jsonify({"reply": full_text, "thinking": thinking_text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/deepseek/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    if request.method == 'OPTIONS':
        return Response(status=204)
    
    try:
        file = request.files['file']
        filename = file.filename
        mime = mimetypes.guess_type(filename)[0] or 'image/jpeg'
        
        headers = get_headers()
        pow_resp = solve_pow('/api/v0/file/upload_file')
        headers['x-ds-pow-response'] = pow_resp
        
        r = requests.post(
            'https://chat.deepseek.com/api/v0/file/upload_file',
            headers=headers,
            files={'file': (filename, file.read(), mime)},
            timeout=120
        )
        
        data = r.json()
        file_id = data.get('data', {}).get('biz_data', {}).get('file_id', '')
        
        if file_id:
            return jsonify({"file_id": file_id})
        else:
            return jsonify({"error": str(data)[:200]}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
