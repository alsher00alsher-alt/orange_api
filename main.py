from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def sign_in(number, password):
    url = "https://services.orange.eg/SignIn.svc/SignInUser"
    payload = {
        "appVersion": "9.0.1",
        "channel": {"ChannelName": "MobinilAndMe", "Password": "ig3yh*mk5l42@oj7QAR8yF"},
        "dialNumber": number, "isAndroid": True, "lang": "ar", "password": password
    }
    headers = {'User-Agent': "okhttp/4.10.0", 'Content-Type': "application/json; charset=UTF-8"}
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    if data.get('SignInUserResult', {}).get('ErrorCode') != 0:
        return None, data.get('SignInUserResult', {}).get('ErrorDescription', 'بيانات دخول خاطئة')
    return data['SignInUserResult']['AccessToken'], None

def generate_token(number, password, access_token):
    url = "https://services.orange.eg/APIs/Profile/api/BasicAuthentication/Generate"
    payload = {"ChannelName": "MobinilAndMe", "ChannelPassword": "ig3yh*mk5l42@oj7QAR8yF",
               "Dial": number, "Language": "ar", "Module": "0", "Password": password}
    headers = {'User-Agent': "okhttp/4.10.0", 'Content-Type': "application/json; charset=UTF-8",
               'AppVersion': "9.0.1", 'OsVersion': "13", 'IsAndroid': "true",
               'IsEasyLogin': "false", 'Token': access_token}
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    if data.get('ErrorCode') != 0:
        return None, data.get('ErrorDescription', 'فشل توليد التوكن')
    return data['Token'], None

def execute_ramadan(number, token):
    url = "https://services.orange.eg/APIs/Ramadan2024/api/RamadanOffers/Fawazeer/Questions"
    payload = {"Dial": number, "Language": "ar", "Token": token}
    headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
               'Content-Type': "application/json", 'Origin': "https://services.orange.eg",
               'X-Requested-With': "com.orange.mobinilandmf"}
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    if data.get('ErrorCode') == 1:
        return False, "دخلت الفوازير اليوم، جرب غداً"
    if not data.get('Questions'):
        return False, "لا توجد أسئلة"
    answers = []
    for q in data['Questions']:
        for a in q['Answers']:
            if a.get('IsCorrect'):
                answers.append({"QuestionId": a["QuestionId"], "AnswerId": a["Id"]})
                break
    submit_url = "https://services.orange.eg/APIs/Ramadan2024/api/RamadanOffers/Fawazeer/Submit"
    submit_payload = {"Dial": number, "Language": "ar", "Token": token, "Answers": answers}
    r = requests.post(submit_url, json=submit_payload, headers=headers)
    result = r.json()
    if result.get('ErrorDescription') == "FawazeerSuccess":
        return True, "✅ تم بنجاح! أرسلت 250 ميجا"
    return False, result.get('ErrorDescription', 'فشل')

def execute_fiveg(number, token):
    url = "https://services.orange.eg/APIs/Promotions/api/Postpaid5G/Redeem"
    payload = {"Dial": number, "Language": "ar", "Token": token}
    headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
               'Content-Type': "application/json", 'Accept': "application/json, text/plain, */*",
               'Origin': "https://services.orange.eg", 'X-Requested-With': "com.orange.mobinilandme"}
    r = requests.post(url, json=payload, headers=headers)
    data = r.json()
    if data.get('ErrorCode') == 0:
        return True, "✅ تم تفعيل عرض 5G بنجاح (500 ميجا)"
    return False, data.get('ErrorDescription', 'فشل العرض')

@app.route('/api', methods=['POST'])
def api_handler():
    data = request.get_json()
    if not data: return jsonify({"error": "بيانات غير صالحة"}), 400
    action = data.get('action')
    number = data.get('number')
    password = data.get('password')
    if not number or not password: return jsonify({"error": "أدخل الرقم وكلمة المرور"}), 400
    if action not in ['ramadan', 'fiveg']: return jsonify({"error": "إجراء غير صحيح"}), 400
    acc_token, err = sign_in(number, password)
    if err: return jsonify({"error": err}), 401
    main_token, err = generate_token(number, password, acc_token)
    if err: return jsonify({"error": err}), 401
    if action == 'ramadan':
        success, msg = execute_ramadan(number, main_token)
    else:
        success, msg = execute_fiveg(number, main_token)
    if success: return jsonify({"success": msg})
    return jsonify({"error": msg}), 400

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Orange API active"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
