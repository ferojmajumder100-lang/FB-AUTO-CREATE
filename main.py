#!/usr/bin/env python3

import requests
import time
import sys
import os
import re
import random
import string
import asyncio
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8880280543:AAHCoMHUepS5VjEcTNpHh_kTZQJygBQ_9Vw"

def print_banner():
    print("\033[91m" + "=" * 70 + "\033[0m")
    print("\033[91m" + """
 █████╗ ██████╗  █████╗ ███████╗ █████╗ ████████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
███████║██████╔╝███████║█████╗  ███████║   ██║   
██╔══██║██╔══██╗██╔══██║██╔══╝  ██╔══██║   ██║   
██║  ██║██║  ██║██║  ██║██║     ██║  ██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   
    """ + "\033[0m")
    print("\033[93m" + " " * 20 + "FB 2.0" + " " * 20 + "\033[0m")
    print("\033[92m" + "~" * 70 + "\033[0m")
    print("\033[96m" + " " * 22 + "TG: @Flase_ARAFAT" + " " * 22 + "\033[0m")
    print("\033[91m" + "=" * 70 + "\033[0m")
    print()

def random_name():
    first = ['Rakib', 'Rafiq', 'Jahid', 'Shakib', 'Tamim', 'Riyad', 'Sakib', 'Mehedi', 'Nayeem', 'Shahin']
    last = ['Hasan', 'Ahmed', 'Islam', 'Hossain', 'Rahman', 'Khan', 'Ali', 'Uddin', 'Chowdhury', 'Mia']
    return random.choice(first), random.choice(last)

def random_birth():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1980, 2005)
    return day, month, year

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p").lstrip('0')

def create_account(phone, language):
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
        
        if response.status_code == 200 and elapsed_time >= 3:
            cookies_dict = response.cookies.get_dict()
            
            if 'c_user' in cookies_dict:
                uid = cookies_dict['c_user']
                current_time = get_time()
                
                cookie_parts = []
                
                if 'datr' in cookies_dict:
                    cookie_parts.append(f"datr={cookies_dict['datr'].replace(' ', '')}")
                if 'sb' in cookies_dict:
                    cookie_parts.append(f"sb={cookies_dict['sb'].replace(' ', '')}")
                if 'ps_l' in cookies_dict:
                    cookie_parts.append(f"ps_l={cookies_dict['ps_l'].replace(' ', '')}")
                if 'ps_n' in cookies_dict:
                    cookie_parts.append(f"ps_n={cookies_dict['ps_n'].replace(' ', '')}")
                if 'm_pixel_ratio' in cookies_dict:
                    cookie_parts.append(f"m_pixel_ratio={cookies_dict['m_pixel_ratio'].replace(' ', '')}")
                if 'wd' in cookies_dict:
                    cookie_parts.append(f"wd={cookies_dict['wd'].replace(' ', '')}")
                if 'c_user' in cookies_dict:
                    cookie_parts.append(f"c_user={cookies_dict['c_user'].replace(' ', '')}")
                if 'fr' in cookies_dict:
                    cookie_parts.append(f"fr={cookies_dict['fr'].replace(' ', '')}")
                if 'xs' in cookies_dict:
                    cookie_parts.append(f"xs={cookies_dict['xs'].replace(' ', '')}")
                
                cookie_string = "; ".join(cookie_parts)
                
                return {
                    'phone': phone, 
                    'success': True, 
                    'uid': uid, 
                    'cookies': cookie_string, 
                    'time': current_time
                }
            else:
                return {'phone': phone, 'success': False}
        else:
            return {'phone': phone, 'success': False}
            
    except Exception as e:
        return {'phone': phone, 'success': False}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🌐 LANGUAGE")],
        [KeyboardButton("📖 HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 FB CREATE AUTO BOT 2.0\n\n"
        "📌 Click LANGUAGE to select your language\n"
        "📌 Send numbers line by line to create accounts\n\n"
        "Example:\n"
        "+8801836283617\n"
        "+8801817559946",
        reply_markup=reply_markup
    )

async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🇺🇸 ENGLISH (en-US)")],
        [KeyboardButton("🇧🇩 BENGALI (bn-BD)")],
        [KeyboardButton("🇫🇷 FRENCH (fr-FR)")],
        [KeyboardButton("🔙 BACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🌐 SELECT YOUR LANGUAGE:\n\n"
        "🇺🇸 English (en-US)\n"
        "🇧🇩 Bengali (bn-BD)\n"
        "🇫🇷 French (fr-FR)",
        reply_markup=reply_markup
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "ENGLISH" in text:
        context.user_data['language'] = 'en-US'
        await update.message.reply_text("✅ Language set to ENGLISH (en-US)")
    elif "BENGALI" in text:
        context.user_data['language'] = 'bn-BD'
        await update.message.reply_text("✅ ভাষা সেট করা হয়েছে বাংলা (bn-BD)")
    elif "FRENCH" in text:
        context.user_data['language'] = 'fr-FR'
        await update.message.reply_text("✅ Langue définie sur FRANÇAIS (fr-FR)")
    
    keyboard = [
        [KeyboardButton("🌐 LANGUAGE")],
        [KeyboardButton("📖 HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔙 Main Menu", reply_markup=reply_markup)

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🌐 LANGUAGE")],
        [KeyboardButton("📖 HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔙 Main Menu", reply_markup=reply_markup)

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    # Check if it's a button
    if user_input in ["🌐 LANGUAGE", "📖 HELP", "🔙 BACK", "🇺🇸 ENGLISH (en-US)", "🇧🇩 BENGALI (bn-BD)", "🇫🇷 FRENCH (fr-FR)"]:
        return
    
    numbers = [line.strip() for line in user_input.split('\n') if line.strip()]
    
    if not numbers:
        await update.message.reply_text("❌ No numbers found!")
        return
    
    # Check language
    if 'language' not in context.user_data:
        await update.message.reply_text("❌ Please select language first using LANGUAGE button")
        return
    
    language = context.user_data['language']
    total = len(numbers)
    
    for i, num in enumerate(numbers, 1):
        await update.message.reply_text(f"🟡 [{i}/{total}] {num}")
        
        result = await asyncio.to_thread(create_account, num, language)
        
        if result['success']:
            # Single message with all info in monospace
            message = (
                f"✅ `{result['phone']} {result['time']}`\n\n"
                f"🆔 `UID {result['uid']}`\n\n"
                f"🍪 `{result['cookies']}`"
            )
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"❌ `{num}`", parse_mode='Markdown')

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🔙 BACK")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📖 HELP\n\n"
        "1️⃣ Click LANGUAGE to select your language\n"
        "2️⃣ Send numbers line by line\n"
        "3️⃣ Bot will create Facebook accounts\n\n"
        "Example:\n"
        "`+8801836283617`\n"
        "`+8801817559946`",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🌐 LANGUAGE":
        await language_menu(update, context)
    elif text == "📖 HELP":
        await help_menu(update, context)
    elif text == "🔙 BACK":
        await back_to_menu(update, context)
    elif text in ["🇺🇸 ENGLISH (en-US)", "🇧🇩 BENGALI (bn-BD)", "🇫🇷 FRENCH (fr-FR)"]:
        await set_language(update, context)
    else:
        await handle_numbers(update, context)

def main():
    print_banner()
    print("✅ BOT STARTED...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Bot stopped!")
        sys.exit(0)
