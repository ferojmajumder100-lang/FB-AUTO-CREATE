#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests
import time
import random
import string
import os

app = Flask(__name__)

TOKEN = "8816064734:AAGoIdwfZLYyku8VfyxLqmMaCtVnv3ShBws"
WEBHOOK_URL = "https://your-domain.com/webhook"

def random_name():
    first = ['Rakib', 'Rafiq', 'Jahid', 'Shakib', 'Tamim', 'Riyad', 'Sakib', 'Mehedi', 'Nayeem', 'Shahin']
    last = ['Hasan', 'Ahmed', 'Islam', 'Hossain', 'Rahman', 'Khan', 'Ali', 'Uddin', 'Chowdhury', 'Mia']
    return random.choice(first), random.choice(last)

def random_birth():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1980, 2005)
    return day, month, year

def create_account(phone):
    fname, lname = random_name()
    day, month, year = random_birth()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; itel S665L Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
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
        'accept-language': 'bn-BD',
        'priority': 'u=1, i'
    }
    
    data = {
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
        'firstname': fname,
        'lastname': lname,
        'field_names[1]': 'birthday_wrapper',
        'birthday_day': str(day),
        'birthday_month': str(month),
        'birthday_year': str(year),
        'age_step_input': '',
        'did_use_age': '',
        'field_names[2]': 'reg_email__',
        'reg_email__': phone,
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
    
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, data=data, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            return True
        else:
            return False
            
    except Exception as e:
        return False

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if 'message' in data:
        msg = data['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        
        if text == '/start':
            send_message(chat_id, "🔵 FB CREATE AUTO 2.0\n\nSend numbers:\n+8801836283617")
        elif text:
            numbers = [line.strip() for line in text.split('\n') if line.strip()]
            total = len(numbers)
            
            for i, num in enumerate(numbers, 1):
                send_message(chat_id, f"🟡 [{i}/{total}] {num}")
                
                result = create_account(num)
                
                if result:
                    send_message(chat_id, f"🟢 {num}")
                else:
                    send_message(chat_id, f"🔴 {num}")
    
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
