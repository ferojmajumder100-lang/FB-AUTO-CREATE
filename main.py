#!/usr/bin/env python3

import requests
import time
import sys
import os
import asyncio
import re
import random
import threading
import json
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# ==================== টেলিগ্রাম টোকেন ====================
TOKEN = "8816064734:AAGoIdwfZLYyku8VfyxLqmMaCtVnv3ShBws"
ADMIN_ID = 7787612625
LOG_GROUP_ID = "-1003538330629"
OTP_GROUP_URL = "https://t.me/power_otp_botx"

# ==================== X-MNIT কনফিগারেশন ====================
XMNIT_BASE_URL = "https://x.mnitnetwork.com"
LOGIN_EMAIL = "minhajurrahmanrabbi20@gmail.com"
LOGIN_PASSWORD = "minhajur_rahman_rabbi_"
AUTH_TOKEN = None

# ==================== ডাটাবেস ====================
ACTIVE_NUMBERS_DB = "xmnit_active_numbers.json"
USERS_DB = "users.json"

# ==================== User Storage ====================
user_language = {}
user_create_mode = {}
user_auto_mode = {}

# শুধু 1 টি ইউজার এজেন্ট (itel)
DEFAULT_USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 12; itel S665L Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
]

# ==================== সম্পূর্ণ ল্যাঙ্গুয়েজ লিস্ট ====================
LANGUAGES = [
    {"code": "bn-BD", "country": "Bangladesh"}, {"code": "en-US", "country": "United States"},
    {"code": "hi-IN", "country": "India"}, {"code": "ur-PK", "country": "Pakistan"},
    {"code": "ar-SA", "country": "Saudi Arabia"}, {"code": "fr-FR", "country": "France"},
    {"code": "de-DE", "country": "Germany"}, {"code": "es-ES", "country": "Spain"},
    {"code": "it-IT", "country": "Italy"}, {"code": "ru-RU", "country": "Russia"},
    {"code": "zh-CN", "country": "China"}, {"code": "ja-JP", "country": "Japan"},
    {"code": "ko-KR", "country": "South Korea"}, {"code": "tr-TR", "country": "Turkey"},
    {"code": "id-ID", "country": "Indonesia"}, {"code": "ms-MY", "country": "Malaysia"},
    {"code": "th-TH", "country": "Thailand"}, {"code": "vi-VN", "country": "Vietnam"},
    {"code": "nl-NL", "country": "Netherlands"}, {"code": "pt-PT", "country": "Portugal"},
]

# ==================== র‍্যান্ডম নাম ====================
RANDOM_FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra", "Mark", "Ashley",
    "Paul", "Kimberly", "Steven", "Emily", "Andrew", "Donna", "Kenneth", "Michelle"
]

RANDOM_LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
]

# ==================== ফেসবুক রেজিস্ট্রেশন হেডার ====================
base_headers = {
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua': '"Chromium";v="148", "Android WebView";v="148", "Not/A)Brand";v="99"',
    'x-response-format': 'JSONStream',
    'sec-ch-ua-mobile': '?1',
    'x-asbd-id': '359341',
    'x-fb-lsd': 'AdRg5ufqsQVcQXAYMc0sAcuMAYE',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://limited.facebook.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://limited.facebook.com/reg/?is_two_steps_login=0&cid=103&refsrc=deprecated&soft=hjk',
    'priority': 'u=1, i'
}

static_data_template = {
    'ccp': '2',
    'reg_instance': '9XYnakzu3MZlEdcKm5l6S7Xh',
    'submission_request': 'true',
    'helper': '',
    'reg_impression_id': '16b59158-6fd5-4197-a940-9a9a29ce1e50',
    'ns': '3',
    'zero_header_af_client': '',
    'app_id': '103',
    'logger_id': '2dd9b1d6-cbeb-4244-ac05-5f7d8c12f13d',
    'field_names[0]': 'firstname',
    'field_names[1]': 'birthday_wrapper',
    'birthday_day': '8',
    'birthday_month': '6',
    'birthday_year': '1993',
    'age_step_input': '',
    'did_use_age': '',
    'field_names[2]': 'reg_email__',
    'field_names[3]': 'sex',
    'sex': '2',
    'preferred_pronoun': '',
    'custom_gender': '',
    'field_names[4]': 'reg_passwd__',
    'name_suggest_elig': 'false',
    'was_shown_name_suggestions': 'false',
    'did_use_suggested_name': 'false',
    'use_custom_gender': 'false',
    'guid': '',
    'pre_form_step': '',
    'encpass': '#PWD_BROWSER:5:1780971336:AWpQAHRsP2zkO3/VeBaZHD0D1UfjIAKyX/a9B/S+iN7x9UUA7AZ1+iRkLq9/wo+6nR6pBkU9AcC0SBxwuoThC3UQlN/Yrgq9KUZ/VE3HAcYhXaKa3e3iRRZLairgU9n0M2cyTtrOPuihyKyE',
    'submit': 'Sign up',
    'fb_dtsg': 'NAfx3wG1Lv9JqEl5Xo_k4IgVl9NOIczPI42MHjtMHwUlwIJPkjDwRQw:0:0',
    'jazoest': '24981',
    'lsd': 'AdRg5ufqsQVcQXAYMc0sAcuMAYE',
    '__dyn': '1Z3pawlEnwm8_Bg9ppoW5UdE4a2i5U4e0C86u7E39x60zU3ex608ewk9E4W0pKq0FE6S0x81vohw73wGwcq1GwqU2YwbK0oi0zE1jU1soG0hi0Lo6-0Co1kU1UU3jwea',
    '__csr': '',
    '__hsdp': '',
    '__hblp': '',
    '__sjsp': '',
    '__req': '9',
    '__fmt': '1',
    '__a': 'AYziFkahooYGibmFOiEjTgieqVVZfkpaag_fk7JZ7MuPjmhxkA1_y8Va3uw3j-5R57TlEkPviSDWHWtTFhXBDy8M4ZSYCckmIVU',
    '__user': '0'
}

url = 'https://limited.facebook.com/reg/submit/?app_id=103&multi_step_form=1&skip_suma=0&shouldForceMTouch=1'

# ==================== কান্ট্রি ফ্ল্যাগ ====================
COUNTRY_FLAGS = {
    "BD": "🇧🇩", "US": "🇺🇸", "IN": "🇮🇳", "PK": "🇵🇰", "SA": "🇸🇦",
    "AE": "🇦🇪", "GB": "🇬🇧", "CA": "🇨🇦", "AU": "🇦🇺", "DE": "🇩🇪",
    "FR": "🇫🇷", "IT": "🇮🇹", "ES": "🇪🇸", "NL": "🇳🇱", "RU": "🇷🇺",
    "CN": "🇨🇳", "JP": "🇯🇵", "KR": "🇰🇷", "TR": "🇹🇷", "ID": "🇮🇩",
    "MY": "🇲🇾", "TH": "🇹🇭", "VN": "🇻🇳", "PH": "🇵🇭", "EG": "🇪🇬",
}

PREFIX_TO_COUNTRY = {
    "1": "US", "44": "GB", "91": "IN", "92": "PK", "966": "SA", "971": "AE",
    "49": "DE", "33": "FR", "39": "IT", "34": "ES", "31": "NL", "7": "RU",
    "86": "CN", "81": "JP", "82": "KR", "90": "TR", "62": "ID", "60": "MY",
    "66": "TH", "84": "VN", "63": "PH", "20": "EG", "880": "BD", "55": "BR",
    "52": "MX", "61": "AU", "1": "CA", "27": "ZA", "234": "NG",
}

def get_country_flag_from_prefix(phone):
    phone_str = str(phone).replace("+", "").strip()
    for length in range(4, 0, -1):
        prefix = phone_str[:length]
        if prefix in PREFIX_TO_COUNTRY:
            country_code = PREFIX_TO_COUNTRY[prefix]
            return COUNTRY_FLAGS.get(country_code, "🌍"), country_code
    return "🌍", "XX"

def mask_number_for_group(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:4] + "*******" + phone_str[-4:]
    return phone_str[:4] + "*******"

# ==================== ইউজার ডাটাবেস ফাংশন ====================
def init_user_db():
    if not os.path.exists(USERS_DB):
        with open(USERS_DB, "w") as f:
            json.dump([], f)

init_user_db()

def get_all_users():
    try:
        with open(USERS_DB, "r") as f:
            return json.load(f)
    except:
        return []

def add_user(user_id):
    users = get_all_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_DB, "w") as f:
            json.dump(users, f)

def broadcast_to_all(message_text):
    users = get_all_users()
    success = 0
    fail = 0
    for user_id in users:
        try:
            import telebot
            tb = telebot.TeleBot(TOKEN)
            tb.send_message(user_id, message_text, parse_mode="Markdown")
            success += 1
        except:
            fail += 1
    return success, fail

# ==================== X-MNIT ফাংশন ====================
def xmnit_login():
    global AUTH_TOKEN
    login_url = f"{XMNIT_BASE_URL}/mapi/v1/mauth/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": XMNIT_BASE_URL,
        "Referer": f"{XMNIT_BASE_URL}/mauth/login",
        "x-requested-with": "mark.via.gp"
    }
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data.get("data", {}).get("token")
            if AUTH_TOKEN:
                print("✅ XMNIT Login Success!")
                return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
    return False

def xmnit_get_live_ranges(service):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xmnit_login()
    
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            logs = data.get("data", {}).get("logs", [])
            ranges = []
            for log in logs:
                app_name = log.get("app_name", "").lower()
                if service.lower() in app_name:
                    rng = log.get("range")
                    if rng:
                        range_str = str(rng).upper().strip()
                        if not range_str.endswith('X'):
                            digits_only = re.sub(r'[^0-9]', '', range_str)
                            if digits_only:
                                if len(digits_only) >= 10:
                                    prefix = digits_only[:5] if len(digits_only) >= 11 else digits_only[:4]
                                    range_str = prefix + "XXXXXX"
                                else:
                                    range_str = digits_only + "XXXXX"
                        ranges.append(range_str)
            ranges = list(dict.fromkeys(ranges))
            return ranges
    except Exception as e:
        print(f"Ranges error: {e}")
    return []

def get_combined_fb_ig_ranges():
    fb_data = xmnit_get_live_ranges("facebook")
    ig_data = xmnit_get_live_ranges("instagram")
    all_ranges = list(set(fb_data + ig_data))
    return all_ranges

def xmnit_fetch_number(range_code):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xmnit_login()
    
    url = f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/number"
    headers = {
        "mauthtoken": AUTH_TOKEN,
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": XMNIT_BASE_URL,
        "x-requested-with": "mark.via.gp"
    }
    payload = {"range": range_code, "is_national": False, "remove_plus": False}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            number_data = data.get("data", {})
            number = number_data.get("full_number") or number_data.get("number")
            
            if number:
                return str(number).replace("+", "").strip()
    except Exception as e:
        print(f"Fetch error: {e}")
    return None

def xmnit_check_otp():
    global AUTH_TOKEN
    results = []
    if not AUTH_TOKEN:
        xmnit_login()
    
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xmnit_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XMNIT_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            numbers_list = data.get("data", {}).get("numbers", [])
            active = get_active_numbers()
            
            for item in numbers_list:
                number = item.get("number", "")
                message = item.get("message", "")
                
                if str(number) in active:
                    otp = extract_otp_from_text(message)
                    if otp != "N/A":
                        results.append({
                            "phone": number,
                            "message": message,
                            "otp": otp,
                            "range": active[str(number)].get("range", "")
                        })
    except Exception as e:
        print(f"OTP error: {e}")
    return results

def extract_otp_from_text(text):
    text = str(text)
    clean_text = re.sub(r'[-\s\.]', '', text)
    
    patterns = [
        r'FB[-]?(\d{5,6})', r'code[:\s]*(\d{4,8})', r'otp[:\s]*(\d{4,8})',
        r'(\d{8})', r'(\d{7})', r'(\d{6})', r'(\d{5})', r'(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            otp = match.group(1)
            if len(otp) >= 4:
                return otp
    
    digits = re.findall(r'\d+', clean_text)
    for digit in digits:
        if len(digit) >= 4:
            return digit
    return "N/A"

def mask_number(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:7] + "XXX" + phone_str[-2:]
    return phone_str

# ==================== ডাটাবেস ফাংশন ====================
def init_databases():
    if not os.path.exists(ACTIVE_NUMBERS_DB):
        with open(ACTIVE_NUMBERS_DB, "w") as f:
            json.dump({}, f)

init_databases()

def get_active_numbers():
    with open(ACTIVE_NUMBERS_DB, "r") as f:
        return json.load(f)

def save_active_numbers(numbers):
    with open(ACTIVE_NUMBERS_DB, "w") as f:
        json.dump(numbers, f)

def add_active_number(phone, chat_id, range_code):
    flag, country_code = get_country_flag_from_prefix(phone)
    
    data = get_active_numbers()
    data[str(phone)] = {
        "chat_id": chat_id,
        "range": range_code,
        "country_flag": flag,
        "country_code": country_code,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_active_numbers(data)
    print(f"✅ Saved: {phone} - {flag}")

def remove_active_number(phone):
    data = get_active_numbers()
    if str(phone) in data:
        del data[str(phone)]
        save_active_numbers(data)

def add_user_number(chat_id, phone_number):
    if not hasattr(add_user_number, 'user_numbers'):
        add_user_number.user_numbers = {}
    
    if chat_id not in add_user_number.user_numbers:
        add_user_number.user_numbers[chat_id] = []
    
    if phone_number not in add_user_number.user_numbers[chat_id]:
        add_user_number.user_numbers[chat_id].append(phone_number)
        return True
    return False

def get_user_numbers(chat_id):
    if not hasattr(add_user_number, 'user_numbers'):
        add_user_number.user_numbers = {}
    return add_user_number.user_numbers.get(chat_id, [])

def remove_user_number(chat_id, phone_number):
    if hasattr(add_user_number, 'user_numbers'):
        if chat_id in add_user_number.user_numbers:
            if phone_number in add_user_number.user_numbers[chat_id]:
                add_user_number.user_numbers[chat_id].remove(phone_number)

# ==================== ইউজার এজেন্ট ফাংশন (শুধু 1 টি) ====================
def get_user_useragent(user_id):
    return DEFAULT_USER_AGENTS[0]

# ==================== ফেসবুক রেজিস্ট্রেশন ====================
def format_phone(phone):
    phone = phone.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone

def generate_random_name():
    first_name = random.choice(RANDOM_FIRST_NAMES)
    last_name = random.choice(RANDOM_LAST_NAMES)
    return first_name, last_name

def send_facebook_request(phone_number, lang_code, user_agent):
    first_name, last_name = generate_random_name()
    
    data = static_data_template.copy()
    data['firstname'] = first_name
    data['lastname'] = last_name
    data['reg_email__'] = phone_number
    
    headers = base_headers.copy()
    headers['accept-language'] = lang_code
    headers['User-Agent'] = user_agent
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=30)
        status_code = response.status_code
        
        return {
            'phone': phone_number,
            'status_code': status_code,
            'success': status_code == 200,
            'firstname': first_name,
            'lastname': last_name,
            'language': lang_code
        }
    except Exception as e:
        return {'phone': phone_number, 'success': False, 'error': str(e)[:50]}

def send_otp_notification(chat_id, phone, otp, message, flag, country_code):
    masked_phone = mask_number_for_group(phone)
    
    dm_msg = f"""✅ OTP RECEIVED!
━━━━━━━━━━━━━━━━━━━━
📱 Number: `{phone}`
🎯 Service: Facebook/Instagram
🌍 Country: {flag}
━━━━━━━━━━━━━━━━━━━━
🔐 OTP Code: `{otp}`
━━━━━━━━━━━━━━━━━━━━
📩 Full SMS:
`{message[:200]}`
━━━━━━━━━━━━━━━━━━━━"""
    
    # গ্রুপ মেসেজে OTP দেখানো হচ্ছে
    group_msg = f"{flag} {country_code} FB {masked_phone}\n🔐 OTP: `{otp}`"
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🔐 COPY {otp}", callback_data=f"copy_otp_{otp}")]
    ])
    
    try:
        import telebot
        tb = telebot.TeleBot(TOKEN)
        tb.send_message(chat_id, dm_msg, parse_mode="Markdown")
        tb.send_message(LOG_GROUP_ID, group_msg, parse_mode="Markdown", reply_markup=markup)
        print(f"📱 OTP Sent: {phone} -> {otp}")
    except Exception as e:
        print(f"Send error: {e}")

def send_account_created_to_group(phone, name, lang_code, flag):
    masked_phone = mask_number_for_group(phone)
    group_msg = f"""✅ ACCOUNT CREATED!

📞 PHONE: {flag} `{masked_phone}`
👤 NAME: {name}
🔑 PASSWORD: `arafat55`
🌐 LANGUAGE: `{lang_code}`"""
    
    try:
        import telebot
        tb = telebot.TeleBot(TOKEN)
        tb.send_message(LOG_GROUP_ID, group_msg, parse_mode="Markdown")
    except Exception as e:
        print(f"Group send error: {e}")

# ==================== এডমিন কীবোর্ড ====================
def get_admin_keyboard():
    keyboard = [
        [KeyboardButton("📢 BROADCAST")],
        [KeyboardButton("📊 STATS")],
        [KeyboardButton("🔙 BACK TO USER")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ==================== টেলিগ্রাম হ্যান্ডলার ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    add_user(user_id)
    
    if user_id == ADMIN_ID:
        keyboard = [
            [KeyboardButton("🎲 GET NUMBER")],
            [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
            [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
            [KeyboardButton("❓ HELP"), KeyboardButton("🛠 ADMIN")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"👋 WELCOME ADMIN!\n\n"
            f"🤖 X-MNIT + FB Creator Bot\n\n"
            f"📌 All features available!\n"
            f"🔑 Password: `arafat55`",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    keyboard = [
        [KeyboardButton("🎲 GET NUMBER")],
        [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
        [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    current_lang = user_language.get(user_id, "bn-BD")
    user_create_mode[user_id] = False
    user_auto_mode[user_id] = False
    
    await update.message.reply_text(
        f"🤖 X-MNIT + FB Creator Bot\n\n"
        f"🌐 Language: `{current_lang}`\n"
        f"🔄 UserAgent: 1 agent (itel)\n\n"
        "📌 HOW TO USE:\n"
        "1️⃣ Press '🎲 GET NUMBER' to get numbers\n"
        "2️⃣ Press '🚀 NOW CREATE' to create accounts\n"
        "3️⃣ Press '⚡ FULL AUTO CREATE' for auto creation\n"
        "4️⃣ Send numbers (only your numbers!)\n\n"
        "🔑 Password: `arafat55`\n"
        "✨ Random names for each account",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def get_number_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Fetching live ranges from X-MNIT...")
    
    ranges_data = get_combined_fb_ig_ranges()
    
    if not ranges_data:
        await update.message.reply_text("❌ No live ranges available right now!\nPlease try again later.")
        return
    
    keyboard = []
    for range_code in ranges_data[:15]:
        flag, _ = get_country_flag_from_prefix(range_code)
        keyboard.append([InlineKeyboardButton(f"{flag} {range_code}", callback_data=f"range_{range_code}")])
    
    keyboard.append([InlineKeyboardButton("🔄 REFRESH", callback_data="refresh_ranges")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📞 SELECT A RANGE:\n\n"
        f"Total {len(ranges_data)} live ranges available.",
        reply_markup=reply_markup
    )

async def set_language_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for i, lang in enumerate(LANGUAGES):
        row.append(InlineKeyboardButton(lang['country'], callback_data=f"lang_{lang['code']}"))
        if len(row) == 2 or i == len(LANGUAGES) - 1:
            keyboard.append(row)
            row = []
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌐 SELECT LANGUAGE:\n\n"
        f"Total {len(LANGUAGES)} languages available.",
        reply_markup=reply_markup
    )

async def now_create_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_phones = get_user_numbers(user_id)
    
    if not user_phones:
        await update.message.reply_text(
            "❌ YOU HAVE NO NUMBERS!\n\n"
            "First press '🎲 GET NUMBER' to get phone numbers."
        )
        return
    
    user_create_mode[user_id] = True
    user_auto_mode[user_id] = False
    
    keyboard = [
        [KeyboardButton("🎲 GET NUMBER")],
        [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
        [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([KeyboardButton("🛠 ADMIN")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    current_lang = user_language.get(user_id, "bn-BD")
    numbers_list = "\n".join([f"{get_country_flag_from_prefix(n)[0]} `{n}`" for n in user_phones[:5]])
    
    await update.message.reply_text(
        f"✅ READY TO CREATE ACCOUNTS!\n\n"
        f"🌐 Language: `{current_lang}`\n"
        f"📞 Your numbers:\n{numbers_list}\n\n"
        "⚠️ You can ONLY send numbers from your list above!\n\n"
        "📞 SEND NUMBERS (one per line):",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def full_auto_create_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    user_auto_mode[user_id] = True
    user_create_mode[user_id] = False
    
    await update.message.reply_text(
        "⚡ FULL AUTO CREATE MODE\n\n"
        "Send a number (like: 5, 10, 20)\n"
        "How many accounts do you want to create?\n\n"
        "Example: `5`\n\n"
        "⚠️ Bot will automatically:\n"
        "1. Get numbers from live ranges\n"
        "2. Create accounts\n"
        "3. Show results",
        parse_mode='Markdown'
    )

async def my_numbers_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_phones = get_user_numbers(user_id)
    
    if not user_phones:
        await update.message.reply_text("📭 You have no numbers yet!\n\nPress '🎲 GET NUMBER' to get numbers.")
        return
    
    numbers_text = "📞 YOUR NUMBERS:\n\n"
    for i, n in enumerate(user_phones, 1):
        flag, _ = get_country_flag_from_prefix(n)
        numbers_text += f"{i}. {flag} `{n}`\n"
    
    numbers_text += f"\nTotal: {len(user_phones)} numbers"
    
    keyboard = [[KeyboardButton("🔙 BACK")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(numbers_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = [
        [KeyboardButton("🎲 GET NUMBER")],
        [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
        [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([KeyboardButton("🛠 ADMIN")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📖 HELP GUIDE\n\n"
        "1️⃣ GET NUMBER - Get live numbers from X-MNIT\n"
        "2️⃣ NOW CREATE - Create Facebook accounts manually\n"
        "3️⃣ SET LANGUAGE - Change account language\n"
        "4️⃣ MY NUMBERS - View your numbers\n"
        "5️⃣ FULL AUTO CREATE - Auto create accounts\n\n"
        "⚠️ You can ONLY create accounts with numbers you received!\n\n"
        "🔑 Password: arafat55\n"
        "✨ Random names for each account",
        reply_markup=reply_markup
    )

async def admin_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized to use admin panel!")
        return
    
    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        "📢 BROADCAST - Send message to all users\n"
        "📊 STATS - View bot statistics\n"
        "🔙 BACK TO USER - Return to user menu",
        reply_markup=get_admin_keyboard()
    )

async def broadcast_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    await update.message.reply_text(
        "📢 BROADCAST MODE\n\n"
        "Send your broadcast message.\n"
        "It will be sent to ALL users.\n\n"
        "To cancel, send /cancel"
    )
    context.user_data['waiting_for_broadcast'] = True

async def stats_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized!")
        return
    
    total_users = len(get_all_users())
    active_numbers = len(get_active_numbers())
    
    await update.message.reply_text(
        f"📊 BOT STATISTICS\n\n"
        f"👥 Total Users: {total_users}\n"
        f"📱 Active Numbers: {active_numbers}\n"
        f"🌐 Languages: {len(LANGUAGES)}\n"
        f"🔄 UserAgent: itel (1 agent)\n"
        f"👤 Admin ID: {ADMIN_ID}"
    )

async def back_to_user_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = [
        [KeyboardButton("🎲 GET NUMBER")],
        [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
        [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([KeyboardButton("🛠 ADMIN")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    current_lang = user_language.get(user_id, "bn-BD")
    
    await update.message.reply_text(
        f"🔙 Back to User Menu\n\n"
        f"🌐 Language: `{current_lang}`",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_broadcast_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_input = update.message.text
    
    if not context.user_data.get('waiting_for_broadcast', False):
        return
    
    if user_input == "/cancel":
        context.user_data['waiting_for_broadcast'] = False
        await update.message.reply_text("❌ Broadcast cancelled!")
        return
    
    context.user_data['waiting_for_broadcast'] = False
    
    await update.message.reply_text("📢 Sending broadcast message to all users...")
    
    success, fail = broadcast_to_all(user_input)
    
    await update.message.reply_text(
        f"✅ BROADCAST COMPLETED!\n\n"
        f"📨 Sent to: {success} users\n"
        f"❌ Failed: {fail} users"
    )
    
    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        "📢 BROADCAST - Send message to all users\n"
        "📊 STATS - View bot statistics\n"
        "🔙 BACK TO USER - Return to user menu",
        reply_markup=get_admin_keyboard()
    )

async def back_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = [
        [KeyboardButton("🎲 GET NUMBER")],
        [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
        [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([KeyboardButton("🛠 ADMIN")])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text("🔙 Main Menu:", reply_markup=reply_markup)

async def handle_auto_create(update: Update, context: ContextTypes.DEFAULT_TYPE, count: int):
    user_id = update.effective_user.id
    current_lang = user_language.get(user_id, "bn-BD")
    user_agent = get_user_useragent(user_id)
    
    await update.message.reply_text(
        f"⚡ AUTO CREATING {count} ACCOUNTS...\n\n"
        f"🌐 Language: {current_lang}\n"
        f"🔄 Getting numbers from live ranges...\n"
        f"⏳ Please wait..."
    )
    
    ranges_data = get_combined_fb_ig_ranges()
    
    if not ranges_data:
        await update.message.reply_text("❌ No live ranges available!")
        return
    
    success_count = 0
    fail_count = 0
    results = []
    
    for i in range(count):
        range_code = random.choice(ranges_data)
        
        number = xmnit_fetch_number(range_code)
        
        if not number:
            fail_count += 1
            results.append({"success": False, "phone": "N/A", "error": "No number available"})
            continue
        
        formatted_num = format_phone(number)
        result = send_facebook_request(formatted_num, current_lang, user_agent)
        
        if result['success']:
            success_count += 1
            flag, _ = get_country_flag_from_prefix(number)
            results.append({
                "success": True,
                "phone": number,
                "name": f"{result['firstname']} {result['lastname']}",
                "flag": flag
            })
            
            send_account_created_to_group(number, f"{result['firstname']} {result['lastname']}", current_lang, flag)
        else:
            fail_count += 1
            results.append({
                "success": False,
                "phone": number if number else "N/A",
                "error": result.get('error', 'Unknown')
            })
        
        await asyncio.sleep(1)
    
    result_msg = f"⚡ AUTO CREATE COMPLETED!\n\n"
    result_msg += f"📊 Total: {count}\n"
    result_msg += f"✅ Success: {success_count}\n"
    result_msg += f"❌ Failed: {fail_count}\n"
    result_msg += f"📈 Rate: {(success_count/count)*100:.1f}%\n\n"
    result_msg += f"📋 DETAILS:\n"
    result_msg += f"{'='*40}\n"
    
    for idx, res in enumerate(results, 1):
        if res['success']:
            result_msg += f"{idx}. ✅ {res['flag']} `{res['phone']}`\n"
            result_msg += f"   👤 {res['name']}\n"
            result_msg += f"   🔑 `arafat55`\n"
        else:
            result_msg += f"{idx}. ❌ `{res['phone']}` - {res.get('error', 'Failed')}\n"
        result_msg += f"{'-'*30}\n"
    
    await update.message.reply_text(result_msg, parse_mode='Markdown')

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    user_id = update.effective_user.id
    
    button_list = ["🎲 GET NUMBER", "🚀 NOW CREATE", "🌐 SET LANGUAGE", "📋 MY NUMBERS", 
                   "⚡ FULL AUTO CREATE", "❓ HELP", "🔙 BACK", "🛠 ADMIN", 
                   "📢 BROADCAST", "📊 STATS", "🔙 BACK TO USER"]
    
    if user_input in button_list:
        return
    
    if context.user_data.get('waiting_for_broadcast', False):
        await handle_broadcast_input(update, context)
        return
    
    if user_auto_mode.get(user_id, False):
        user_auto_mode[user_id] = False
        try:
            count = int(user_input.strip())
            if count > 0 and count <= 50:
                await handle_auto_create(update, context, count)
            else:
                await update.message.reply_text("❌ Please send a number between 1 and 50!")
        except ValueError:
            await update.message.reply_text("❌ Invalid number! Please send a valid number (like: 5, 10, 20)")
        return
    
    if not user_create_mode.get(user_id, False):
        await update.message.reply_text(
            "❌ PLEASE PRESS '🚀 NOW CREATE' OR '⚡ FULL AUTO CREATE' FIRST!\n\n"
            "Click one of the buttons before sending numbers."
        )
        return
    
    numbers = [line.strip() for line in user_input.split('\n') if line.strip()]
    
    if not numbers:
        await update.message.reply_text("❌ NO NUMBERS FOUND!")
        return
    
    user_phones = get_user_numbers(user_id)
    user_phone_set = set(user_phones)
    
    valid_numbers = []
    invalid_numbers = []
    
    for num in numbers:
        formatted_num = num.replace("+", "").strip()
        if formatted_num in user_phone_set:
            valid_numbers.append(formatted_num)
        else:
            invalid_numbers.append(formatted_num)
    
    if invalid_numbers:
        await update.message.reply_text(
            f"❌ INVALID NUMBERS!\n\n"
            f"You can ONLY send numbers you received!\n"
            f"Press '📋 MY NUMBERS' to see your numbers."
        )
        return
    
    if not valid_numbers:
        await update.message.reply_text("❌ No valid numbers to process!")
        return
    
    current_lang = user_language.get(user_id, "bn-BD")
    user_agent = get_user_useragent(user_id)
    
    await update.message.reply_text(
        f"📊 PROCESSING {len(valid_numbers)} NUMBER(S)...\n"
        f"✨ Random names!\n"
        f"🌐 Language: {current_lang}\n"
        f"⏳ Please wait..."
    )
    
    success_count = 0
    fail_count = 0
    total = len(valid_numbers)
    
    for i, num in enumerate(valid_numbers, 1):
        formatted_num = format_phone(num)
        result = send_facebook_request(formatted_num, current_lang, user_agent)
        
        if result['success']:
            success_count += 1
            flag, _ = get_country_flag_from_prefix(num)
            
            send_account_created_to_group(num, f"{result['firstname']} {result['lastname']}", current_lang, flag)
            
            await update.message.reply_text(
                f"✅ ACCOUNT CREATED!\n\n"
                f"📞 PHONE: `{result['phone']}`\n"
                f"👤 NAME: {result['firstname']} {result['lastname']}\n"
                f"🔑 PASSWORD: `arafat55`\n"
                f"🌐 LANGUAGE: `{result.get('language', 'N/A')}`",
                parse_mode='Markdown'
            )
            remove_user_number(user_id, num)
        else:
            fail_count += 1
            error = result.get('error', f"HTTP {result.get('status_code', 'N/A')}")
            await update.message.reply_text(
                f"❌ FAILED: `{result['phone']}`\nERROR: {error}",
                parse_mode='Markdown'
            )
        
        if i < total:
            await asyncio.sleep(0.5)
    
    summary = f"{'='*40}\n"
    summary += f"📊 COMPLETED!\n"
    summary += f"✅ SUCCESS: {success_count}\n"
    summary += f"❌ FAILED: {fail_count}\n"
    if total > 0:
        summary += f"📈 RATE: {(success_count/total)*100:.1f}%\n"
    summary += f"{'='*40}"
    
    await update.message.reply_text(summary)
    user_create_mode[user_id] = False

# ==================== কলব্যাক হ্যান্ডলার ====================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    
    if data.startswith("copy_otp_"):
        otp_code = data.split("_")[2]
        await query.answer(f"✅ OTP Copied: {otp_code}", show_alert=True)
        return
    
    if data == "refresh_ranges":
        await query.edit_message_text("📡 Refreshing live ranges...")
        
        ranges_data = get_combined_fb_ig_ranges()
        
        if not ranges_data:
            await query.edit_message_text("❌ No live ranges available!")
            return
        
        keyboard = []
        for range_code in ranges_data[:15]:
            flag, _ = get_country_flag_from_prefix(range_code)
            keyboard.append([InlineKeyboardButton(f"{flag} {range_code}", callback_data=f"range_{range_code}")])
        
        keyboard.append([InlineKeyboardButton("🔄 REFRESH", callback_data="refresh_ranges")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📞 SELECT A RANGE:\n\nTotal {len(ranges_data)} live ranges.",
            reply_markup=reply_markup
        )
        return
    
    if data.startswith("range_"):
        range_code = data.split("_")[1]
        
        await query.edit_message_text(f"⏳ Getting number from {range_code}...")
        
        number = xmnit_fetch_number(range_code)
        
        if number:
            add_user_number(user_id, number)
            add_active_number(number, user_id, range_code)
            
            flag, _ = get_country_flag_from_prefix(number)
            total = len(get_user_numbers(user_id))
            
            button_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 OTP GROUP", url=OTP_GROUP_URL)],
                [InlineKeyboardButton("🔄 GET MORE", callback_data="back_to_ranges")]
            ])
            
            await query.edit_message_text(
                f"✅ NUMBER RECEIVED!\n\n"
                f"{flag} `{number}`\n\n"
                f"📞 Total numbers: {total}\n\n"
                f"Press '🚀 NOW CREATE' to create accounts!",
                reply_markup=button_markup,
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(f"❌ No number available for this range!\n\nTry another range.")
        
        return
    
    if data == "back_to_ranges":
        ranges_data = get_combined_fb_ig_ranges()
        
        if not ranges_data:
            await query.edit_message_text("❌ No live ranges available!")
            return
        
        keyboard = []
        for range_code in ranges_data[:15]:
            flag, _ = get_country_flag_from_prefix(range_code)
            keyboard.append([InlineKeyboardButton(f"{flag} {range_code}", callback_data=f"range_{range_code}")])
        
        keyboard.append([InlineKeyboardButton("🔄 REFRESH", callback_data="refresh_ranges")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📞 SELECT A RANGE:\n\nTotal {len(ranges_data)} live ranges.",
            reply_markup=reply_markup
        )
        return
    
    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        user_language[user_id] = lang_code
        
        country_name = "Unknown"
        for lang in LANGUAGES:
            if lang['code'] == lang_code:
                country_name = lang['country']
                break
        
        await query.edit_message_text(f"✅ Language set to {country_name}!")
        
        keyboard = [
            [KeyboardButton("🎲 GET NUMBER")],
            [KeyboardButton("🚀 NOW CREATE"), KeyboardButton("🌐 SET LANGUAGE")],
            [KeyboardButton("📋 MY NUMBERS"), KeyboardButton("⚡ FULL AUTO CREATE")],
            [KeyboardButton("❓ HELP")]
        ]
        if user_id == ADMIN_ID:
            keyboard.append([KeyboardButton("🛠 ADMIN")])
        
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await query.message.reply_text("🔙 Back to menu:", reply_markup=reply_markup)
        return

# ==================== OTP মনিটর ====================
sent_otps = set()

def otp_monitor():
    global sent_otps
    print("🔄 OTP Monitor Started")
    while True:
        try:
            otps = xmnit_check_otp()
            
            for otp_data in otps:
                phone = otp_data["phone"]
                key = f"{phone}_{otp_data['otp']}"
                
                if key not in sent_otps:
                    sent_otps.add(key)
                    active = get_active_numbers()
                    
                    if str(phone) in active:
                        a = active[str(phone)]
                        flag, country_code = get_country_flag_from_prefix(phone)
                        
                        send_otp_notification(a["chat_id"], phone, otp_data["otp"], 
                                             otp_data["message"], flag, country_code)
                        remove_active_number(phone)
                        print(f"📱 OTP: {phone} -> {otp_data['otp']}")
            
            if len(sent_otps) > 1000:
                sent_otps.clear()
                
        except Exception as e:
            print(f"Monitor Error: {e}")
        time.sleep(5)

# ==================== মেইন ====================
def main():
    print("=" * 50)
    print("X-MNIT + FB Creator Bot (Combined)")
    print("=" * 50)
    
    print("\n🔍 Logging in to X-MNIT...")
    xmnit_login()
    
    print("\n🤖 Starting OTP Monitor...")
    thread = threading.Thread(target=otp_monitor, daemon=True)
    thread.start()
    
    print("\n🤖 Starting Telegram Bot...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^🎲 GET NUMBER$'), get_number_button))
    app.add_handler(MessageHandler(filters.Regex('^🚀 NOW CREATE$'), now_create_button))
    app.add_handler(MessageHandler(filters.Regex('^🌐 SET LANGUAGE$'), set_language_button))
    app.add_handler(MessageHandler(filters.Regex('^⚡ FULL AUTO CREATE$'), full_auto_create_button))
    app.add_handler(MessageHandler(filters.Regex('^📋 MY NUMBERS$'), my_numbers_button))
    app.add_handler(MessageHandler(filters.Regex('^❓ HELP$'), help_button))
    app.add_handler(MessageHandler(filters.Regex('^🔙 BACK$'), back_button))
    app.add_handler(MessageHandler(filters.Regex('^🛠 ADMIN$'), admin_button))
    app.add_handler(MessageHandler(filters.Regex('^📢 BROADCAST$'), broadcast_button))
    app.add_handler(MessageHandler(filters.Regex('^📊 STATS$'), stats_button))
    app.add_handler(MessageHandler(filters.Regex('^🔙 BACK TO USER$'), back_to_user_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("✅ Bot Started Successfully!")
    print("✅ Features: Live Ranges + OTP Monitor + Facebook Creator + Auto Create + Broadcast")
    print("=" * 50)
    
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Bot Stopped!")
        sys.exit(0)
