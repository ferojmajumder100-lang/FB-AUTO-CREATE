#!/usr/bin/env python3

import requests
import time
import sys
import os
import re
import random
import threading
import hashlib
import subprocess
from datetime import datetime

# ==================== ডিভাইস অ্যাক্টিভেশন সিস্টেম ====================
# আপনার GitHub রিপোজিটরির device.json ফাইলের RAW লিংক
DEVICE_CHECK_URL = "https://raw.githubusercontent.com/ferojmajumder100-lang/FB-AUTO-CREATE/main/device.json"

def get_device_id():
    """ইউনিক ডিভাইস আইডি তৈরি করুন"""
    try:
        # Termux/Android ডিভাইস আইডি পাওয়ার চেষ্টা
        result = subprocess.run(['getprop', 'ro.serialno'], capture_output=True, text=True)
        if result.stdout and result.stdout.strip():
            device_id = result.stdout.strip()
        else:
            # অ্যান্ড্রয়েড আইডি
            result = subprocess.run(['settings', 'get', 'secure', 'android_id'], capture_output=True, text=True)
            if result.stdout and result.stdout.strip():
                device_id = result.stdout.strip()
            else:
                # ব্যাকআপ: হোস্টনেম + ইউজার হোম ব্যবহার করে আইডি তৈরি
                hostname = os.uname().nodename
                home = os.path.expanduser("~")
                device_id = hashlib.md5(f"{hostname}{home}".encode()).hexdigest()[:32]
    except:
        # সব ব্যর্থ হলে
        import uuid
        device_id = str(uuid.getnode())  # MAC address based
        if not device_id:
            device_id = hashlib.md5(os.path.expanduser("~").encode()).hexdigest()[:32]
    
    return device_id

def check_device_activation():
    """ডিভাইস অ্যাক্টিভেটেড কিনা চেক করুন"""
    device_id = get_device_id()
    
    try:
        response = requests.get(DEVICE_CHECK_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            activated_devices = data.get("activated_devices", [])
            if device_id in activated_devices:
                return True
    except Exception as e:
        # নেটওয়ার্ক সমস্যা হলে বট চলতে দিবেন কিনা? চাইলে False দিতে পারেন
        # এখানে True দিলে নেটওয়ার্ক সমস্যায় সবাই বট চালাতে পারবে
        print(f"\033[91m[!] Device check failed: {e}\033[0m")
        return False  # False দিলে কেউ চালাতে পারবে না
    
    # ডিভাইস অ্যাক্টিভেটেড না হলে
    print("\033[91m" + "=" * 60 + "\033[0m")
    print("\033[91m❌ DEVICE NOT ACTIVATED!\033[0m")
    print("\033[93m📱 Your Device ID:\033[0m")
    print(f"\033[96m{device_id}\033[0m")
    print("\033[93m💡 Send this ID to admin to add in device.json\033[0m")
    print("\033[91m" + "=" * 60 + "\033[0m")
    return False

# ডিভাইস চেক (একাউন্ট ক্রিয়েটের আগে)
if not check_device_activation():
    sys.exit(1)

# ==================== মূল প্রোগ্রাম শুরু ====================

# গ্লোবাল ভেরিয়েবল
monitoring_active = True
created_accounts = []

def clear_screen():
    os.system('clear')

def print_banner():
    clear_screen()
    print("\033[91m" + """
 █████╗ ██████╗  █████╗ ███████╗ █████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
███████║██████╔╝███████║█████╗  ███████║   ██║   
██╔══██║██╔══██╗██╔══██║██╔══╝  ██╔══██║   ██║   
██║  ██║██║  ██║██║  ██║██║     ██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   
    """ + "\033[0m")
    print("\033[93m" + " " * 22 + "FB 2.0" + " " * 22 + "\033[0m")
    print()

def format_range_code(raw_range):
    range_str = str(raw_range).strip()
    if 'X' in range_str:
        return range_str
    digits = re.sub(r'[^0-9]', '', range_str)
    if not digits:
        return None
    if len(digits) >= 10:
        prefix = digits[:5]
        return f"{prefix}XXXXX"
    elif len(digits) >= 5:
        return f"{digits}XXXXX"
    else:
        return f"{digits}XXXXXXX"

def get_live_ranges():
    try:
        login_url = "https://x.mnitnetwork.com/mapi/v1/mauth/login"
        login_data = {
            "email": "minhajurrahmanrabbi20@gmail.com",
            "password": "minhajur_rahman_rabbi_"
        }
        session = requests.Session()
        login_response = session.post(login_url, json=login_data, timeout=15)
        if login_response.status_code == 200:
            auth_token = login_response.json().get('data', {}).get('token')
            if auth_token:
                headers = {"mauthtoken": auth_token}
                ranges_response = session.get("https://x.mnitnetwork.com/mapi/v1/mdashboard/console/info", 
                                             headers=headers, timeout=15)
                if ranges_response.status_code == 200:
                    logs = ranges_response.json().get('data', {}).get('logs', [])
                    ranges = []
                    for log in logs:
                        app_name = log.get('app_name', '').lower()
                        if 'facebook' in app_name or 'instagram' in app_name:
                            rng = log.get('range')
                            if rng:
                                formatted = format_range_code(rng)
                                if formatted:
                                    ranges.append(formatted)
                    return list(set(ranges))
        return []
    except Exception:
        return []

def fetch_number_from_range(range_code):
    try:
        login_url = "https://x.mnitnetwork.com/mapi/v1/mauth/login"
        login_data = {
            "email": "minhajurrahmanrabbi20@gmail.com",
            "password": "minhajur_rahman_rabbi_"
        }
        session = requests.Session()
        login_response = session.post(login_url, json=login_data, timeout=15)
        if login_response.status_code == 200:
            auth_token = login_response.json().get('data', {}).get('token')
            if auth_token:
                headers = {
                    "mauthtoken": auth_token,
                    "Content-Type": "application/json"
                }
                payload = {
                    "range": range_code,
                    "is_national": False,
                    "remove_plus": False
                }
                number_response = session.post(
                    "https://x.mnitnetwork.com/mapi/v1/mdashboard/getnum/number",
                    json=payload,
                    headers=headers,
                    timeout=15
                )
                if number_response.status_code == 200:
                    data = number_response.json()
                    number = data.get('data', {}).get('full_number') or \
                             data.get('data', {}).get('number')
                    if number:
                        return str(number).replace('+', '').strip()
        return None
    except Exception:
        return None

def random_name():
    first = ['Rakib', 'Rafiq', 'Jahid', 'Shakib', 'Tamim', 'Riyad', 'Sakib', 'Mehedi', 
             'Nayeem', 'Shahin', 'Arif', 'Shahid', 'Nurul', 'Mostafa', 'Mizan']
    last = ['Hasan', 'Ahmed', 'Islam', 'Hossain', 'Rahman', 'Khan', 'Ali', 'Uddin', 
            'Chowdhury', 'Mia', 'Sarker', 'Mollah', 'Karim', 'Miah', 'Haque']
    return random.choice(first), random.choice(last)

def random_birth():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1980, 2005)
    return day, month, year

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p").lstrip('0')

def extract_otp_from_text(text):
    if not text:
        return "N/A"
    
    text = str(text)
    clean_text = re.sub(r'[-\s\.\,]', '', text)
    
    patterns = [
        r'FB[-]?(\d{5,6})',
        r'FACEBOOK[-]?(\d{5,6})',
        r'IG[-]?(\d{5,6})',
        r'INSTAGRAM[-]?(\d{5,6})',
        r'[Cc][Oo][Dd][Ee][:\s]*(\d{4,8})',
        r'[Oo][Tt][Pp][:\s]*(\d{4,8})',
        r'[Vv][Ee][Rr][Ii][Ff][Yy][:\s]*(\d{4,8})',
        r'[Cc][Oo][Nn][Ff][Ii][Rr][Mm][:\s]*(\d{4,8})',
        r'[Aa][Uu][Tt][Hh][:\s]*(\d{4,8})',
        r'(\d{8})', r'(\d{7})', r'(\d{6})', r'(\d{5})', r'(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            otp = match.group(1)
            if len(otp) >= 4:
                return otp
    
    digits = re.findall(r'\d+', clean_text)
    if digits:
        longest = max(digits, key=len)
        if len(longest) >= 4:
            return longest
    
    return "N/A"

def check_otp_for_numbers():
    global monitoring_active, created_accounts
    if not created_accounts:
        return
    try:
        login_url = "https://x.mnitnetwork.com/mapi/v1/mauth/login"
        login_data = {
            "email": "minhajurrahmanrabbi20@gmail.com",
            "password": "minhajur_rahman_rabbi_"
        }
        session = requests.Session()
        login_response = session.post(login_url, json=login_data, timeout=10)
        if login_response.status_code == 200:
            auth_token = login_response.json().get('data', {}).get('token')
            if auth_token:
                headers = {"mauthtoken": auth_token}
                today = datetime.now().strftime("%Y-%m-%d")
                otp_response = session.get(
                    f"https://x.mnitnetwork.com/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success",
                    headers=headers,
                    timeout=10
                )
                if otp_response.status_code == 200:
                    numbers_data = otp_response.json().get('data', {}).get('numbers', [])
                    for account in created_accounts[:]:
                        phone = account['phone']
                        for item in numbers_data:
                            if item.get('number') == phone:
                                message = item.get('message', '')
                                otp = extract_otp_from_text(message)
                                if otp != "N/A":
                                    print(f"\n\033[96m📱 OTP: {phone} → \033[93m{otp}\033[0m")
                                    created_accounts.remove(account)
                                    break
    except Exception:
        pass

def otp_monitor_thread():
    global monitoring_active
    while monitoring_active:
        check_otp_for_numbers()
        time.sleep(1)

def create_account(phone, index, total, language='fr-FR'):
    print(f"\033[93m[{index}/{total}] \033[93m{phone}\033[0m", end='\r')
    
    fname, lname = random_name()
    day, month, year = random_birth()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; itel S665L Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
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
        'accept-language': language,
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
        
        print(" " * 50, end='\r')
        
        if response.status_code == 200 and elapsed_time >= 3:
            cookies_dict = response.cookies.get_dict()
            
            if 'c_user' in cookies_dict:
                uid = cookies_dict['c_user']
                current_time = get_time()
                
                cookie_parts = []
                for key in ['datr', 'sb', 'ps_l', 'ps_n', 'm_pixel_ratio', 'wd', 'c_user', 'fr', 'xs']:
                    if key in cookies_dict:
                        cookie_parts.append(f"{key}={cookies_dict[key].replace(' ', '')}")
                
                cookie_string = "; ".join(cookie_parts)
                
                print(f"\033[93m{phone}\033[0m \033[92m{current_time}\033[0m")
                print(f"\033[95mUID {uid}\033[0m")
                print(f"\033[92m{cookie_string}\033[0m")
                print()
                
                return {
                    'phone': phone, 
                    'success': True, 
                    'uid': uid,
                    'cookies': cookie_string,
                    'time': current_time
                }
            else:
                print(f"\033[91m✗ {phone}\033[0m")
                print()
                return {'phone': phone, 'success': False}
        else:
            print(f"\033[91m✗ {phone}\033[0m")
            print()
            return {'phone': phone, 'success': False}
            
    except Exception:
        print(" " * 50, end='\r')
        print(f"\033[91m✗ {phone}\033[0m")
        print()
        return {'phone': phone, 'success': False}

def main():
    global monitoring_active, created_accounts
    
    print_banner()
    
    # ভাষা নির্বাচন
    print("\033[93m[?] Select Language:\033[0m")
    print("1. English")
    print("2. Bengali")
    print("3. French")
    lang_choice = input("\033[96m[?] Enter (1-3): \033[0m").strip()
    
    lang_map = {'1': 'en-US', '2': 'bn-BD', '3': 'fr-FR'}
    language = lang_map.get(lang_choice, 'fr-FR')
    
    print("\n\033[93m[+] Fetching ranges...\033[0m")
    ranges = get_live_ranges()
    
    numbers = []
    
    if ranges:
        selected_range = random.choice(ranges)
        print(f"\033[92m[+] Range: {selected_range}\033[0m")
        
        count = input("\033[96m[?] How many? (1-20): \033[0m").strip()
        try:
            count = int(count)
            if count > 20:
                count = 20
            if count < 1:
                count = 1
        except:
            count = 2
        
        for i in range(count):
            number = fetch_number_from_range(selected_range)
            if number:
                numbers.append(number)
    else:
        print("\033[91m[!] No ranges!\033[0m")
        return
    
    if not numbers:
        print("\n\033[91m[!] No numbers!\033[0m")
        return
    
    clear_screen()
    print_banner()
    print()
    
    results = []
    success_list = []
    failed_list = []
    
    for i, num in enumerate(numbers, 1):
        result = create_account(num, i, len(numbers), language)
        results.append(result)
        if result['success']:
            success_list.append(num)
            created_accounts.append({
                'phone': result['phone'],
                'uid': result['uid'],
                'time': result['time']
            })
        else:
            failed_list.append(num)
        # কোন ডিলে নেই - একটার পর একটা সাথে সাথে ক্রিয়েট হবে
    
    print(f"\n\033[92m✓ {len(success_list)} created\033[0m")
    
    if created_accounts:
        print(f"\033[93m[ℹ] Monitoring {len(created_accounts)} numbers for OTP...\033[0m")
        print(f"\033[90m[!] Press \033[97mCtrl + C\033[90m to stop\033[0m\n")
        monitor_thread = threading.Thread(target=otp_monitor_thread, daemon=True)
        monitor_thread.start()
        
        try:
            while monitoring_active:
                time.sleep(1)
        except KeyboardInterrupt:
            monitoring_active = False
            print("\n\033[91m[!] Stopped\033[0m")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Stopped\033[0m")
        sys.exit(0)
