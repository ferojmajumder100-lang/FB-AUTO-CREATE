#!/usr/bin/env python3

import requests
import time
import sys
import os
import asyncio
import re
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8816064734:AAGoIdwfZLYyku8VfyxLqmMaCtVnv3ShBws"

# Random names database (20+ names)
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

# Static headers
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

# Static data template (without static names)
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

def format_phone(phone):
    phone = phone.strip()
    if not phone.startswith('+'):
        phone = '+' + phone
    return phone

def generate_random_name():
    """Generate random first and last name"""
    first_name = random.choice(RANDOM_FIRST_NAMES)
    last_name = random.choice(RANDOM_LAST_NAMES)
    return first_name, last_name

async def send_request(phone_number):
    # Generate random names for each request
    first_name, last_name = generate_random_name()
    
    # Create a copy of static data with random names
    data = static_data_template.copy()
    data['firstname'] = first_name
    data['lastname'] = last_name
    data['reg_email__'] = phone_number
    
    try:
        response = await asyncio.to_thread(requests.post, url, headers=headers, data=data, timeout=30)
        status_code = response.status_code
        
        return {
            'phone': phone_number,
            'status_code': status_code,
            'success': status_code == 200,
            'firstname': first_name,
            'lastname': last_name
        }
        
    except Exception as e:
        return {'phone': phone_number, 'success': False, 'error': str(e)[:50]}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 NOW CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "🤖 BOT ACTIVE\n\n"
        "Press '🚀 NOW CREATE' to start creating accounts\n\n"
        "Then send phone numbers like:\n"
        "8801836283719\n"
        "8801837282738\n\n"
        "Each account will have a RANDOM name automatically!",
        reply_markup=reply_markup
    )

async def now_create_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 NOW CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "✅ READY TO CREATE ACCOUNTS!\n\n"
        "📞 SEND PHONE NUMBERS (one per line):\n"
        "Example:\n"
        "8801836283719\n"
        "8801837282738\n\n"
        "⚡ Each account will get RANDOM names automatically!\n"
        "🔑 Password will be: arafat55",
        reply_markup=reply_markup
    )

async def help_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 NOW CREATE")],
        [KeyboardButton("❓ HELP")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📖 HELP GUIDE\n\n"
        "1️⃣ Press '🚀 NOW CREATE'\n"
        "2️⃣ Send phone numbers (one per line)\n"
        "3️⃣ Bot creates accounts with RANDOM names\n\n"
        "📞 FORMAT:\n"
        "8801836283719\n"
        "8801837282738\n\n"
        "🔑 DEFAULT PASSWORD: arafat55\n\n"
        "✨ Each account gets different random name!\n"
        "✨ No proxy needed - direct connection\n"
        "✨ Instant results",
        reply_markup=reply_markup
    )

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    # Check if it's a button text
    if user_input in ["🚀 NOW CREATE", "❓ HELP"]:
        return
    
    numbers = [line.strip() for line in user_input.split('\n') if line.strip()]
    
    if not numbers:
        await update.message.reply_text("❌ NO NUMBERS FOUND!\n\nPlease send phone numbers one per line.")
        return
    
    await update.message.reply_text(f"📊 PROCESSING {len(numbers)} NUMBER(S)...\n✨ Each account will have RANDOM name!\n⏳ Please wait...")
    
    success_count = 0
    fail_count = 0
    total = len(numbers)
    
    for i, num in enumerate(numbers, 1):
        formatted_num = format_phone(num)
        result = await send_request(formatted_num)
        
        if result['success']:
            success_count += 1
            await update.message.reply_text(
                f"✅ ACCOUNT CREATED SUCCESSFULLY!\n\n"
                f"📞 PHONE: `{result['phone']}`\n"
                f"👤 NAME: {result['firstname']} {result['lastname']}\n"
                f"🔑 PASSWORD: `arafat55`\n"
                f"📊 HTTP: {result['status_code']}",
                parse_mode='Markdown'
            )
        else:
            fail_count += 1
            error = result.get('error', f"HTTP {result.get('status_code', 'N/A')}")
            await update.message.reply_text(
                f"❌ FAILED: `{result['phone']}`\nERROR: {error}",
                parse_mode='Markdown'
            )
        
        if i < total:
            await asyncio.sleep(0.5)  # Small delay between requests
    
    summary = f"{'='*50}\n"
    summary += f"📊 COMPLETED!\n"
    summary += f"📞 TOTAL: {total}\n"
    summary += f"✅ SUCCESS: {success_count}\n"
    summary += f"❌ FAILED: {fail_count}\n"
    if total > 0:
        summary += f"📈 RATE: {(success_count/total)*100:.1f}%\n"
    summary += f"{'='*50}"
    
    await update.message.reply_text(summary)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex('^🚀 NOW CREATE$'), now_create_button))
    app.add_handler(MessageHandler(filters.Regex('^❓ HELP$'), help_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))
    
    print("✅ BOT STARTED...")
    print("✅ PROXY SYSTEM REMOVED")
    print(f"✅ RANDOM NAME SYSTEM ACTIVE ({len(RANDOM_FIRST_NAMES)} first names, {len(RANDOM_LAST_NAMES)} last names)")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ BOT STOPPED!")
        sys.exit(0)
