from flask import Flask, request, jsonify
import requests
import random
import string
import base64
import json
import re

app = Flask(__name__)

SUPABASE_URL = 'https://qcpujeurnkbvwlvmylyx.supabase.co/functions/v1/chat'
IMAGE_EDIT_URL = 'https://shorts.multiplewords.in/mwvideos/api/edit_image_from_text'

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_options(path):
    return jsonify({}), 200

def generate_auth():
    auth_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    auth_string += ''.join(random.choice(string.digits) for _ in range(5))
    auth_string += ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
    return base64.b64encode(auth_string.encode()).decode()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'google/gemini-2.5-flash')
        
        payload = {"messages": messages, "model": model}
        response = requests.post(SUPABASE_URL, json=payload, timeout=60, stream=True)
        
        full = ""
        for line in response.iter_lines():
            if not line or not line.startswith(b'data: '):
                continue
            data_line = line[6:]
            if data_line == b'[DONE]':
                break
            try:
                obj = json.loads(data_line)
                delta = obj.get('choices', [{}])[0].get('delta', {})
                if delta.get('content'):
                    full += delta['content']
            except:
                continue
        
        return jsonify({"content": full or "مفيش رد"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/edit-image', methods=['POST'])
def edit_image():
    try:
        file = request.files['file']
        prompt = request.form.get('prompt', 'Make it more beautiful')
        
        authorization = generate_auth()
        headers = {
            'authorization': authorization,
            'x-forwarded-for': '.'.join(str(random.randint(1,254)) for _ in range(4)),
            'accept': 'application/json'
        }
        
        files = {'file': (file.filename, file.read(), 'image/jpeg')}
        data = {'prompt': prompt, 'user_id': '1'}
        
        response = requests.post(IMAGE_EDIT_URL, headers=headers, files=files, data=data, timeout=60)
        
        try:
            result = response.json()
            return jsonify(result)
        except:
            return jsonify({"error": response.text[:300]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
