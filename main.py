import requests
import time
import threading
import re
import json
import os
from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random

# ==================== কনফিগারেশন ====================
TELEGRAM_TOKEN = "8936835871:AAHzNnPQCPjiWPxEks8PYiPjOt5KKWywWIs"
ADMIN_ID = 7787612625

XULTRA_BASE_URL = "https://x.mnitnetwork.com"
LOG_GROUP_ID = "-1003538330629"
OTP_GROUP_URL = "https://t.me/power_otp_botx"

# ==================== লগইন তথ্য ====================
LOGIN_EMAIL = "minhajurrahmanrabbi20@gmail.com"
LOGIN_PASSWORD = "minhajur_rahman_rabbi_"
AUTH_TOKEN = None

# ==================== কান্ট্রি ফ্ল্যাগ এবং কোড ম্যাপ (প্রিফিক্স অনুযায়ী) ====================
COUNTRY_FLAGS = {
    "AD": "🇦🇩", "AE": "🇦🇪", "AF": "🇦🇫", "AG": "🇦🇬", "AI": "🇦🇮", "AL": "🇦🇱",
    "AM": "🇦🇲", "AO": "🇦🇴", "AQ": "🇦🇶", "AR": "🇦🇷", "AS": "🇦🇸", "AT": "🇦🇹",
    "AU": "🇦🇺", "AW": "🇦🇼", "AX": "🇦🇽", "AZ": "🇦🇿", "BA": "🇧🇦", "BB": "🇧🇧",
    "BD": "🇧🇩", "BE": "🇧🇪", "BF": "🇧🇫", "BG": "🇧🇬", "BH": "🇧🇭", "BI": "🇧🇮",
    "BJ": "🇧🇯", "BL": "🇧🇱", "BM": "🇧🇲", "BN": "🇧🇳", "BO": "🇧🇴", "BQ": "🇧🇶",
    "BR": "🇧🇷", "BS": "🇧🇸", "BT": "🇧🇹", "BV": "🇧🇻", "BW": "🇧🇼", "BY": "🇧🇾",
    "BZ": "🇧🇿", "CA": "🇨🇦", "CC": "🇨🇨", "CD": "🇨🇩", "CF": "🇨🇫", "CG": "🇨🇬",
    "CH": "🇨🇭", "CI": "🇨🇮", "CK": "🇨🇰", "CL": "🇨🇱", "CM": "🇨🇲", "CN": "🇨🇳",
    "CO": "🇨🇴", "CR": "🇨🇷", "CU": "🇨🇺", "CV": "🇨🇻", "CW": "🇨🇼", "CX": "🇨🇽",
    "CY": "🇨🇾", "CZ": "🇨🇿", "DE": "🇩🇪", "DJ": "🇩🇯", "DK": "🇩🇰", "DM": "🇩🇲",
    "DO": "🇩🇴", "DZ": "🇩🇿", "EC": "🇪🇨", "EE": "🇪🇪", "EG": "🇪🇬", "EH": "🇪🇭",
    "ER": "🇪🇷", "ES": "🇪🇸", "ET": "🇪🇹", "FI": "🇫🇮", "FJ": "🇫🇯", "FK": "🇫🇰",
    "FM": "🇫🇲", "FO": "🇫🇴", "FR": "🇫🇷", "GA": "🇬🇦", "GB": "🇬🇧", "GD": "🇬🇩",
    "GE": "🇬🇪", "GF": "🇬🇫", "GG": "🇬🇬", "GH": "🇬🇭", "GI": "🇬🇮", "GL": "🇬🇱",
    "GM": "🇬🇲", "GN": "🇬🇳", "GP": "🇬🇵", "GQ": "🇬🇶", "GR": "🇬🇷", "GS": "🇬🇸",
    "GT": "🇬🇹", "GU": "🇬🇺", "GW": "🇬🇼", "GY": "🇬🇾", "HK": "🇭🇰", "HM": "🇭🇲",
    "HN": "🇭🇳", "HR": "🇭🇷", "HT": "🇭🇹", "HU": "🇭🇺", "ID": "🇮🇩", "IE": "🇮🇪",
    "IL": "🇮🇱", "IM": "🇮🇲", "IN": "🇮🇳", "IO": "🇮🇴", "IQ": "🇮🇶", "IR": "🇮🇷",
    "IS": "🇮🇸", "IT": "🇮🇹", "JE": "🇯🇪", "JM": "🇯🇲", "JO": "🇯🇴", "JP": "🇯🇵",
    "KE": "🇰🇪", "KG": "🇰🇬", "KH": "🇰🇭", "KI": "🇰🇮", "KM": "🇰🇲", "KN": "🇰🇳",
    "KP": "🇰🇵", "KR": "🇰🇷", "KW": "🇰🇼", "KY": "🇰🇾", "KZ": "🇰🇿", "LA": "🇱🇦",
    "LB": "🇱🇧", "LC": "🇱🇨", "LI": "🇱🇮", "LK": "🇱🇰", "LR": "🇱🇷", "LS": "🇱🇸",
    "LT": "🇱🇹", "LU": "🇱🇺", "LV": "🇱🇻", "LY": "🇱🇾", "MA": "🇲🇦", "MC": "🇲🇨",
    "MD": "🇲🇩", "ME": "🇲🇪", "MF": "🇲🇫", "MG": "🇲🇬", "MH": "🇲🇭", "MK": "🇲🇰",
    "ML": "🇲🇱", "MM": "🇲🇲", "MN": "🇲🇳", "MO": "🇲🇴", "MP": "🇲🇵", "MQ": "🇲🇶",
    "MR": "🇲🇷", "MS": "🇲🇸", "MT": "🇲🇹", "MU": "🇲🇺", "MV": "🇲🇻", "MW": "🇲🇼",
    "MX": "🇲🇽", "MY": "🇲🇾", "MZ": "🇲🇿", "NA": "🇳🇦", "NC": "🇳🇨", "NE": "🇳🇪",
    "NF": "🇳🇫", "NG": "🇳🇬", "NI": "🇳🇮", "NL": "🇳🇱", "NO": "🇳🇴", "NP": "🇳🇵",
    "NR": "🇳🇷", "NU": "🇳🇺", "NZ": "🇳🇿", "OM": "🇴🇲", "PA": "🇵🇦", "PE": "🇵🇪",
    "PF": "🇵🇫", "PG": "🇵🇬", "PH": "🇵🇭", "PK": "🇵🇰", "PL": "🇵🇱", "PM": "🇵🇲",
    "PN": "🇵🇳", "PR": "🇵🇷", "PS": "🇵🇸", "PT": "🇵🇹", "PW": "🇵🇼", "PY": "🇵🇾",
    "QA": "🇶🇦", "RE": "🇷🇪", "RO": "🇷🇴", "RS": "🇷🇸", "RU": "🇷🇺", "RW": "🇷🇼",
    "SA": "🇸🇦", "SB": "🇸🇧", "SC": "🇸🇨", "SD": "🇸🇩", "SE": "🇸🇪", "SG": "🇸🇬",
    "SH": "🇸🇭", "SI": "🇸🇮", "SJ": "🇸🇯", "SK": "🇸🇰", "SL": "🇸🇱", "SM": "🇸🇲",
    "SN": "🇸🇳", "SO": "🇸🇴", "SR": "🇸🇷", "SS": "🇸🇸", "ST": "🇸🇹", "SV": "🇸🇻",
    "SX": "🇸🇽", "SY": "🇸🇾", "SZ": "🇸🇿", "TC": "🇹🇨", "TD": "🇹🇩", "TF": "🇹🇫",
    "TG": "🇹🇬", "TH": "🇹🇭", "TJ": "🇹🇯", "TK": "🇹🇰", "TL": "🇹🇱", "TM": "🇹🇲",
    "TN": "🇹🇳", "TO": "🇹🇴", "TR": "🇹🇷", "TT": "🇹🇹", "TV": "🇹🇻", "TW": "🇹🇼",
    "TZ": "🇹🇿", "UA": "🇺🇦", "UG": "🇺🇬", "UM": "🇺🇲", "US": "🇺🇸", "UY": "🇺🇾",
    "UZ": "🇺🇿", "VA": "🇻🇦", "VC": "🇻🇨", "VE": "🇻🇪", "VG": "🇻🇬", "VI": "🇻🇮",
    "VN": "🇻🇳", "VU": "🇻🇺", "WF": "🇼🇫", "WS": "🇼🇸", "YE": "🇾🇪", "YT": "🇾🇹",
    "ZA": "🇿🇦", "ZM": "🇿🇲", "ZW": "🇿🇼"
}

COUNTRY_NAMES = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua and Barbuda",
    "AI": "Anguilla", "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AQ": "Antarctica",
    "AR": "Argentina", "AS": "American Samoa", "AT": "Austria", "AU": "Australia", "AW": "Aruba",
    "AX": "Aland Islands", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
    "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain",
    "BI": "Burundi", "BJ": "Benin", "BL": "Saint Barthelemy", "BM": "Bermuda", "BN": "Brunei Darussalam",
    "BO": "Bolivia", "BQ": "Bonaire", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan",
    "BV": "Bouvet Island", "BW": "Botswana", "BY": "Belarus", "BZ": "Belize", "CA": "Canada",
    "CC": "Cocos Islands", "CD": "Congo DR", "CF": "Central African Republic", "CG": "Congo Republic",
    "CH": "Switzerland", "CI": "Ivory Coast", "CK": "Cook Islands", "CL": "Chile", "CM": "Cameroon",
    "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba", "CV": "Cape Verde",
    "CW": "Curacao", "CX": "Christmas Island", "CY": "Cyprus", "CZ": "Czech Republic", "DE": "Germany",
    "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "DZ": "Algeria",
    "EC": "Ecuador", "EE": "Estonia", "EG": "Egypt", "EH": "Western Sahara", "ER": "Eritrea",
    "ES": "Spain", "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands",
    "FM": "Micronesia", "FO": "Faroe Islands", "FR": "France", "GA": "Gabon", "GB": "United Kingdom",
    "GD": "Grenada", "GE": "Georgia", "GF": "French Guiana", "GG": "Guernsey", "GH": "Ghana",
    "GI": "Gibraltar", "GL": "Greenland", "GM": "Gambia", "GN": "Guinea", "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea", "GR": "Greece", "GS": "South Georgia", "GT": "Guatemala", "GU": "Guam",
    "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island", "HN": "Honduras",
    "HR": "Croatia", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel",
    "IM": "Isle of Man", "IN": "India", "IO": "British Indian Ocean Territory", "IQ": "Iraq",
    "IR": "Iran", "IS": "Iceland", "IT": "Italy", "JE": "Jersey", "JM": "Jamaica", "JO": "Jordan",
    "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia", "KI": "Kiribati",
    "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "North Korea", "KR": "South Korea",
    "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon",
    "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho",
    "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya", "MA": "Morocco",
    "MC": "Monaco", "MD": "Moldova", "ME": "Montenegro", "MF": "Saint Martin", "MG": "Madagascar",
    "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali", "MM": "Myanmar", "MN": "Mongolia",
    "MO": "Macao", "MP": "Northern Mariana Islands", "MQ": "Martinique", "MR": "Mauritania",
    "MS": "Montserrat", "MT": "Malta", "MU": "Mauritius", "MV": "Maldives", "MW": "Malawi",
    "MX": "Mexico", "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia",
    "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands",
    "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand", "OM": "Oman",
    "PA": "Panama", "PE": "Peru", "PF": "French Polynesia", "PG": "Papua New Guinea", "PH": "Philippines",
    "PK": "Pakistan", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "PN": "Pitcairn",
    "PR": "Puerto Rico", "PS": "Palestine", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay",
    "QA": "Qatar", "RE": "Reunion", "RO": "Romania", "RS": "Serbia", "RU": "Russia", "RW": "Rwanda",
    "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan", "SE": "Sweden",
    "SG": "Singapore", "SH": "Saint Helena", "SI": "Slovenia", "SJ": "Svalbard", "SK": "Slovakia",
    "SL": "Sierra Leone", "SM": "San Marino", "SN": "Senegal", "SO": "Somalia", "SR": "Suriname",
    "SS": "South Sudan", "ST": "Sao Tome and Principe", "SV": "El Salvador", "SX": "Sint Maarten",
    "SY": "Syria", "SZ": "Eswatini", "TC": "Turks and Caicos Islands", "TD": "Chad", "TF": "French Southern Territories",
    "TG": "Togo", "TH": "Thailand", "TJ": "Tajikistan", "TK": "Tokelau", "TL": "Timor-Leste",
    "TM": "Turkmenistan", "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago",
    "TV": "Tuvalu", "TW": "Taiwan", "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda",
    "UM": "US Minor Outlying Islands", "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan",
    "VA": "Vatican City", "VC": "Saint Vincent and the Grenadines", "VE": "Venezuela", "VG": "Virgin Islands British",
    "VI": "Virgin Islands US", "VN": "Vietnam", "VU": "Vanuatu", "WF": "Wallis and Futuna",
    "WS": "Samoa", "YE": "Yemen", "YT": "Mayotte", "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe"
}

# প্রিফিক্স থেকে কান্ট্রি শর্ট কোড ম্যাপিং
PREFIX_TO_COUNTRY = {
    "1": "US", "7": "RU", "20": "EG", "27": "ZA", "30": "GR", "31": "NL", "32": "BE",
    "33": "FR", "34": "ES", "36": "HU", "39": "IT", "40": "RO", "41": "CH", "43": "AT",
    "44": "GB", "45": "DK", "46": "SE", "47": "NO", "48": "PL", "49": "DE", "51": "PE",
    "52": "MX", "53": "CU", "54": "AR", "55": "BR", "56": "CL", "57": "CO", "58": "VE",
    "60": "MY", "61": "AU", "62": "ID", "63": "PH", "64": "NZ", "65": "SG", "66": "TH",
    "81": "JP", "82": "KR", "84": "VN", "86": "CN", "90": "TR", "91": "IN", "92": "PK",
    "93": "AF", "94": "LK", "95": "MM", "98": "IR", "211": "SS", "212": "MA", "213": "DZ",
    "216": "TN", "218": "LY", "220": "GM", "221": "SN", "222": "MR", "223": "ML", "224": "GN",
    "225": "CI", "226": "BF", "227": "NE", "228": "TG", "229": "BJ", "230": "MU", "231": "LR",
    "232": "SL", "233": "GH", "234": "NG", "235": "TD", "236": "CF", "237": "CM", "238": "CV",
    "239": "ST", "240": "GQ", "241": "GA", "242": "CG", "243": "CD", "244": "AO", "245": "GW",
    "246": "IO", "247": "AC", "248": "SC", "249": "SD", "250": "RW", "251": "ET", "252": "SO",
    "253": "DJ", "254": "KE", "255": "TZ", "256": "UG", "257": "BI", "258": "MZ", "260": "ZM",
    "261": "MG", "262": "RE", "263": "ZW", "264": "NA", "265": "MW", "266": "LS", "267": "BW",
    "268": "SZ", "269": "KM", "290": "SH", "291": "ER", "297": "AW", "298": "FO", "299": "GL",
    "350": "GI", "351": "PT", "352": "LU", "353": "IE", "354": "IS", "355": "AL", "356": "MT",
    "357": "CY", "358": "FI", "359": "BG", "370": "LT", "371": "LV", "372": "EE", "373": "MD",
    "374": "AM", "375": "BY", "376": "AD", "377": "MC", "378": "SM", "379": "VA", "380": "UA",
    "381": "RS", "382": "ME", "383": "XK", "385": "HR", "386": "SI", "387": "BA", "389": "MK",
    "420": "CZ", "421": "SK", "423": "LI", "500": "FK", "501": "BZ", "502": "GT", "503": "SV",
    "504": "HN", "505": "NI", "506": "CR", "507": "PA", "508": "PM", "509": "HT", "590": "GP",
    "591": "BO", "592": "GY", "593": "EC", "594": "GF", "595": "PY", "596": "MQ", "597": "SR",
    "598": "UY", "599": "CW", "670": "TL", "672": "NF", "673": "BN", "674": "NR", "675": "PG",
    "676": "TO", "677": "SB", "678": "VU", "679": "FJ", "680": "PW", "681": "WF", "682": "CK",
    "683": "NU", "685": "WS", "686": "KI", "687": "NC", "688": "TV", "689": "PF", "690": "TK",
    "691": "FM", "692": "MH", "850": "KP", "852": "HK", "853": "MO", "855": "KH", "856": "LA",
    "880": "BD", "886": "TW", "960": "MV", "961": "LB", "962": "JO", "963": "SY", "964": "IQ",
    "965": "KW", "966": "SA", "967": "YE", "968": "OM", "970": "PS", "971": "AE", "972": "IL",
    "973": "BH", "974": "QA", "975": "BT", "976": "MN", "977": "NP", "992": "TJ", "993": "TM",
    "994": "AZ", "995": "GE", "996": "KG", "998": "UZ"
}

def get_country_info_from_range(range_code):
    """রেঞ্জ কোড থেকে কান্ট্রি তথ্য বের করে (যেমন: 880XXXXXXX থেকে 880)"""
    range_str = str(range_code).replace("X", "").strip()
    for length in range(4, 0, -1):
        prefix = range_str[:length]
        if prefix in PREFIX_TO_COUNTRY:
            country_code = PREFIX_TO_COUNTRY[prefix]
            country_name = COUNTRY_NAMES.get(country_code, "Unknown")
            flag = COUNTRY_FLAGS.get(country_code, "🌍")
            return country_code, country_name, flag
    return "XX", "Unknown", "🌍"

def format_range_with_flag(range_code):
    """রেঞ্জের সাথে ফ্ল্যাগ যোগ করে (যেমন: 🇧🇩 880XXXXXXX)"""
    country_code, country_name, flag = get_country_info_from_range(range_code)
    return f"{flag} {range_code}"

# ==================== FB একাউন্ট ক্রিয়েট ফাংশন (সেশন ক্লিয়ার সহ) ====================
def random_name():
    first = ['Rakib', 'Rafiq', 'Jahid', 'Shakib', 'Tamim', 'Riyad', 'Sakib', 'Mehedi', 'Nayeem', 'Shahin', 
             'Arif', 'Shahid', 'Nurul', 'Mostafa', 'Mizan', 'Shahjahan', 'Nazmul', 'Sharif', 'Rony', 'Sohel',
             'Masud', 'Asif', 'Sumon', 'Babul', 'Azad', 'Shahin', 'Kamal', 'Jamal', 'Selim', 'Faruk',
             'Anis', 'Reza', 'Nasim', 'Farhan', 'Rashed', 'Shafiq', 'Morshed', 'Shaheen', 'Mithun', 'Shanto']
    last = ['Hasan', 'Ahmed', 'Islam', 'Hossain', 'Rahman', 'Khan', 'Ali', 'Uddin', 'Chowdhury', 'Mia',
            'Sarker', 'Mollah', 'Karim', 'Miah', 'Haque', 'Mahmud', 'Hossain', 'Rashid', 'Ahmed', 'Khaled',
            'Mannan', 'Uddin', 'Chowdhury', 'Hasan', 'Mahmud', 'Kamal', 'Jamal', 'Faruk', 'Siddique', 'Islam',
            'Parvez', 'Hossain', 'Alam', 'Nur', 'Islam', 'Rahman', 'Ahmed', 'Hasan', 'Hossain', 'Ali']
    return random.choice(first), random.choice(last)

def random_birth():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1980, 2005)
    return day, month, year

def get_time():
    now = datetime.now()
    return now.strftime("%I:%M %p").lstrip('0')

# ইউজার এজেন্ট লিস্ট (বিভিন্ন ডিভাইসের জন্য)
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 12; itel S665L Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; SM-A135F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; 2201117TY) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; CPH2333) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; V2127) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.7778.215 Mobile Safari/537.36',
]

def create_fb_account(phone, language='fr-FR'):
    """একাউন্ট ক্রিয়েট করে, প্রতিবার নতুন সেশন ব্যবহার করে"""
    
    # নতুন সেশন তৈরি করুন
    session = requests.Session()
    
    # র‍্যান্ডম ইউজার এজেন্ট সিলেক্ট করুন
    user_agent = random.choice(USER_AGENTS)
    
    fname, lname = random_name()
    day, month, year = random_birth()
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
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
        response = session.post(url, headers=headers, data=data, timeout=30)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200 and elapsed_time >= 3:
            cookies_dict = session.cookies.get_dict()
            
            if 'c_user' in cookies_dict:
                uid = cookies_dict['c_user']
                current_time = get_time()
                
                cookie_parts = []
                for key in ['datr', 'sb', 'ps_l', 'ps_n', 'm_pixel_ratio', 'wd', 'c_user', 'fr', 'xs']:
                    if key in cookies_dict:
                        cookie_parts.append(f"{key}={cookies_dict[key].replace(' ', '')}")
                
                cookie_string = "; ".join(cookie_parts)
                
                # সেশন ক্লিয়ার করুন (পরবর্তী রিকোয়েস্টের জন্য)
                session.close()
                
                return {
                    'phone': phone, 
                    'success': True, 
                    'uid': uid, 
                    'cookies': cookie_string, 
                    'time': current_time,
                    'name': f"{fname} {lname}"
                }
        
        session.close()
        return {'phone': phone, 'success': False}
        
    except Exception as e:
        session.close()
        return {'phone': phone, 'success': False}

# ==================== XULTRA লগইন ====================
def xultra_login():
    global AUTH_TOKEN
    login_url = f"{XULTRA_BASE_URL}/mapi/v1/mauth/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Origin": XULTRA_BASE_URL,
        "Referer": f"{XULTRA_BASE_URL}/mauth/login",
        "x-requested-with": "mark.via.gp"
    }
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    
    try:
        response = requests.post(login_url, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            AUTH_TOKEN = data.get("data", {}).get("token")
            if AUTH_TOKEN:
                print("✅ XULTRA Login Success!")
                return True
    except Exception as e:
        print(f"❌ Login Failed: {e}")
    return False

# ==================== XULTRA API ফাংশন ====================
def xultra_get_live_ranges(service):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xultra_login()
    
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XULTRA_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xultra_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XULTRA_BASE_URL}/mapi/v1/mdashboard/console/info", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            logs = data.get("data", {}).get("logs", [])
            if logs is None:
                logs = []
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
            ranges_with_flags = [(format_range_with_flag(r), r) for r in ranges]
            ranges_with_flags.sort(key=lambda x: x[0])
            return [(r[1], r[0]) for r in ranges_with_flags]
    except Exception as e:
        print(f"Ranges error: {e}")
    return []

def get_combined_fb_ig_ranges():
    fb_data = xultra_get_live_ranges("facebook")
    ig_data = xultra_get_live_ranges("instagram")
    all_ranges = {}
    for rng, display in fb_data:
        all_ranges[rng] = display
    for rng, display in ig_data:
        if rng not in all_ranges:
            all_ranges[rng] = display
    sorted_items = sorted(all_ranges.items(), key=lambda x: x[1])
    return [(rng, display) for rng, display in sorted_items]

def xultra_fetch_number(range_code):
    global AUTH_TOKEN
    if not AUTH_TOKEN:
        xultra_login()
    
    url = f"{XULTRA_BASE_URL}/mapi/v1/mdashboard/getnum/number"
    headers = {
        "mauthtoken": AUTH_TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
        "Origin": XULTRA_BASE_URL,
        "x-requested-with": "mark.via.gp"
    }
    payload = {"range": range_code, "is_national": False, "remove_plus": False}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 401:
            xultra_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            number_data = data.get("data", {})
            if number_data is None:
                number_data = {}
            number = number_data.get("full_number") or number_data.get("number")
            
            if number:
                return str(number).replace("+", "").strip()
    except Exception as e:
        print(f"Fetch error: {e}")
    return None

def xultra_check_otp():
    global AUTH_TOKEN
    results = []
    if not AUTH_TOKEN:
        xultra_login()
    
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        headers = {
            "mauthtoken": AUTH_TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36",
            "x-requested-with": "mark.via.gp"
        }
        response = requests.get(f"{XULTRA_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 401:
            xultra_login()
            headers["mauthtoken"] = AUTH_TOKEN
            response = requests.get(f"{XULTRA_BASE_URL}/mapi/v1/mdashboard/getnum/info?date={today}&page=1&search=&status=success", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            numbers_data = data.get("data", {})
            if numbers_data is None:
                numbers_data = {}
            numbers_list = numbers_data.get("numbers", [])
            if numbers_list is None:
                numbers_list = []
            active = get_active_numbers()
            if active is None:
                active = {}
            
            for item in numbers_list:
                if item is None:
                    continue
                number = item.get("number", "")
                message = item.get("message", "")
                app_name = item.get("app_name", "")
                
                if str(number) in active:
                    service = "Facebook/Instagram"
                    otp = extract_otp_from_text(message)
                    if otp != "N/A":
                        results.append({
                            "phone": number,
                            "message": message,
                            "otp": otp,
                            "service": service,
                            "range": active[str(number)].get("range", "")
                        })
    except Exception as e:
        print(f"OTP error: {e}")
    return results

# ==================== OTP এক্সট্রাক্ট ====================
def extract_otp_from_text(text):
    if text is None:
        return "N/A"
    text = str(text)
    clean_text = re.sub(r'[-\s\.]', '', text)
    
    patterns = [
        r'FB[-]?(\d{5,6})',
        r'code[:\s]*(\d{4,8})',
        r'otp[:\s]*(\d{4,8})',
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

def mask_number_for_group(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:4] + "*******" + phone_str[-4:]
    return phone_str[:4] + "*******"

def mask_number(phone):
    phone_str = str(phone)
    if len(phone_str) >= 10:
        return phone_str[:7] + "XXX" + phone_str[-2:]
    return phone_str

# ==================== Monkey Patch ====================
def ibtn(text, callback_data=None, url=None, style=None):
    b = InlineKeyboardButton(text=text, callback_data=callback_data, url=url)
    if style: b.style = style
    return b

def rbtn(text, style=None):
    b = KeyboardButton(text=text)
    if style: b.style = style
    return b

# ==================== ডাটাবেস ====================
USER_DB = "xultra_users.json"
SETTINGS_DB = "xultra_settings.json"
ACTIVE_NUMBERS_DB = "xultra_active_numbers.json"

def init_databases():
    files = {
        USER_DB: [],
        SETTINGS_DB: {"otp_price": 5.0},
        ACTIVE_NUMBERS_DB: {}
    }
    for file, default in files.items():
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump(default, f)

init_databases()

def get_all_users():
    with open(USER_DB, "r") as f:
        data = json.load(f)
        return data if data is not None else []

def add_user(user_id):
    with open(USER_DB, "r") as f:
        users = json.load(f)
        if users is None:
            users = []
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)

def get_settings():
    with open(SETTINGS_DB, "r") as f:
        data = json.load(f)
        return data if data is not None else {"otp_price": 5.0}

def save_settings(settings):
    with open(SETTINGS_DB, "w") as f:
        json.dump(settings, f)

def get_active_numbers():
    with open(ACTIVE_NUMBERS_DB, "r") as f:
        data = json.load(f)
        return data if data is not None else {}

def save_active_numbers(numbers):
    with open(ACTIVE_NUMBERS_DB, "w") as f:
        json.dump(numbers, f)

def add_active_number(phone, chat_id, service, range_code):
    country_code, country_name, flag = get_country_info_from_range(range_code)
    
    data = get_active_numbers()
    data[str(phone)] = {
        "chat_id": chat_id,
        "service": service,
        "range": range_code,
        "country_code": country_code,
        "country_name": country_name,
        "country_flag": flag,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_active_numbers(data)
    print(f"✅ Saved: {phone} ({service}) - {country_name} {flag}")

def remove_active_number(phone):
    data = get_active_numbers()
    if str(phone) in data:
        del data[str(phone)]
        save_active_numbers(data)

# ==================== OTP নোটিফিকেশন ====================
def send_otp_notification(chat_id, phone, service, otp, message, country_name, flag, country_code):
    dm_msg = f"""✅ OTP RECEIVED!
━━━━━━━━━━━━━━━━━━━━
📱 Number: `{phone}`
🎯 Service: {service}
🌍 Country: {country_name} {flag}
━━━━━━━━━━━━━━━━━━━━
🔐 OTP Code: `{otp}`
━━━━━━━━━━━━━━━━━━━━
📩 Full SMS:
`{message[:200] if message else "No message"}`"""
    
    service_short = "FB" if "facebook" in service.lower() else "IG"
    masked_phone = mask_number_for_group(phone)
    group_msg = f"{flag} {country_code} {service_short} {masked_phone}"
    
    markup = InlineKeyboardMarkup()
    markup.add(ibtn(f"🔐 {otp}", callback_data=f"copy_otp_{otp}", style="primary"))
    
    try:
        bot.send_message(chat_id, dm_msg, parse_mode="Markdown")
        bot.send_message(LOG_GROUP_ID, group_msg, reply_markup=markup)
    except Exception as e:
        print(f"Send error: {e}")

def send_numbers_received_notification(chat_id, numbers, service_name, range_code):
    country_code, country_name, flag = get_country_info_from_range(range_code)
    
    numbers_text = "\n".join([f"✅ `{num}`" for num in numbers])
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        ibtn("📢 OTP GROUP", url=OTP_GROUP_URL, style="primary"),
        ibtn("🔄 Change Number", callback_data=f"change_number_{service_name}_{range_code}", style="success")
    )
    markup.add(ibtn("🔙 Back to Services", callback_data="back_to_services", style="danger"))
    
    msg = f"""🎯 Numbers Received!

{flag} {country_code}
{numbers_text}

🎯 Service: {service_name}
🌍 Country: {country_name} {flag}

💡 OTP will appear here automatically!"""
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

# ==================== AUTO CREATE ফাংশন ====================
def auto_create_accounts(chat_id, ranges_data, count, message_id=None):
    """সিলেক্টেড রেঞ্জ থেকে কাঙ্খিত সংখ্যক নম্বর নিয়ে একাউন্ট তৈরি করে এবং অ্যাক্টিভ নম্বরে যোগ করে"""
    if not ranges_data:
        bot.send_message(chat_id, "❌ No ranges available!")
        return
    
    # র‍্যান্ডম রেঞ্জ সিলেক্ট
    selected_range_raw, selected_range_display = random.choice(ranges_data)
    
    # প্রগ্রেস মেসেজ আপডেট
    if message_id:
        bot.edit_message_text(f"🔄 Selected Range: {selected_range_display}\n⏳ Fetching {count} number(s)...", chat_id, message_id)
    else:
        msg = bot.send_message(chat_id, f"🔄 Selected Range: {selected_range_display}\n⏳ Fetching {count} number(s)...")
        message_id = msg.message_id
    
    # কাঙ্খিত সংখ্যক নম্বর ফেচ করুন এবং অ্যাক্টিভে যোগ করুন
    numbers_found = []
    for i in range(count):
        number = xultra_fetch_number(selected_range_raw)
        if number:
            numbers_found.append(number)
            # অ্যাক্টিভ নম্বরে যোগ করুন যাতে OTP আসলে নোটিফিকেশন যায়
            add_active_number(number, chat_id, "Facebook/Instagram (Auto Created)", selected_range_raw)
        time.sleep(0.5)
    
    if not numbers_found:
        bot.edit_message_text(f"❌ No numbers available for {selected_range_display}!\nTry again.", chat_id, message_id)
        return
    
    # একাউন্ট ক্রিয়েট করুন একটার পর একটা (প্রতিবার নতুন সেশন)
    bot.edit_message_text(f"📝 Creating {len(numbers_found)} Facebook account(s) in French language...\n⏳ Processing...", chat_id, message_id)
    
    success_count = 0
    for idx, num in enumerate(numbers_found, 1):
        country_code, country_name, flag = get_country_info_from_range(selected_range_raw)
        
        result = create_fb_account(num, 'fr-FR')
        result['country_flag'] = flag
        result['country_name'] = country_name
        
        if result['success']:
            success_count += 1
            message = (
                f"✅ ACCOUNT #{idx} CREATED!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📱 Number: `{result['phone']}`\n"
                f"👤 Name: {result['name']}\n"
                f"🆔 UID: `{result['uid']}`\n"
                f"🌍 Country: {result.get('country_name', 'Unknown')} {result.get('country_flag', '🌍')}\n"
                f"⏰ Time: {result['time']}\n"
                f"🌐 Language: French (fr-FR)\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🍪 Cookies:\n`{result['cookies'][:300]}...`"
            )
            bot.send_message(chat_id, message, parse_mode='Markdown')
        else:
            message = f"❌ ACCOUNT #{idx} FAILED: `{result['phone']}`"
            bot.send_message(chat_id, message, parse_mode='Markdown')
        
        # প্রতিটি একাউন্টের পর সামান্য ডিলে (IP ব্লক এড়ানোর জন্য)
        time.sleep(1)
    
    # সম্পন্ন হওয়ার মেসেজ
    summary = f"✅ AUTO CREATE COMPLETED!\n━━━━━━━━━━━━━━━━━━━━\n✅ Success: {success_count}/{len(numbers_found)}\n🌍 Range: {selected_range_display}\n🌐 Language: French (fr-FR)\n\n💡 OTP will appear here automatically when received!"
    bot.edit_message_text(summary, chat_id, message_id)

# ==================== AUTO CREATE কীবোর্ড ====================
def get_auto_create_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    buttons = [
        KeyboardButton("2️⃣"),
        KeyboardButton("3️⃣"),
        KeyboardButton("5️⃣"),
        KeyboardButton("8️⃣"),
        KeyboardButton("1️⃣2️⃣"),
        KeyboardButton("1️⃣5️⃣"),
        KeyboardButton("2️⃣0️⃣"),
        KeyboardButton("🔙 BACK")
    ]
    markup.add(*buttons)
    return markup

# ==================== কীবোর্ড ====================
def get_main_keyboard(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(rbtn("🎲 GET NUMBER", style="primary"), rbtn("⚡ AUTO CREATE", style="primary"))
    if user_id == ADMIN_ID:
        markup.row(rbtn("🛠 ADMIN PANEL", style="success"))
    return markup

def get_admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(rbtn("📢 BROADCAST", style="primary"), rbtn("📊 STATS", style="primary"))
    markup.row(rbtn("🔙 BACK", style="danger"))
    return markup

def get_service_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(ibtn("📘 Facebook + Instagram", callback_data="srv_combined", style="primary"))
    markup.row(ibtn("🔙 Back", callback_data="main_menu", style="danger"))
    return markup

def get_range_keyboard(ranges_data, service_type):
    markup = InlineKeyboardMarkup()
    for i, (raw_range, display_text) in enumerate(ranges_data[:12]):
        style = "primary" if i % 2 == 0 else "success"
        markup.add(ibtn(display_text, callback_data=f"range_{service_type}_{raw_range}", style=style))
    
    markup.add(ibtn("🔄 Refresh", callback_data=f"refresh_{service_type}", style="primary"))
    markup.add(ibtn("🔙 Back to Services", callback_data="back_to_services", style="danger"))
    return markup

# ==================== বট হ্যান্ডলার ====================
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id)
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👋 Welcome Admin!\n🌍 Panel: X ULTRA\n✅ Service: Facebook + Instagram\n✅ 2 Numbers per request\n✅ Auto Create Account (2-20) - French Language\n✅ Session cleared after each account\n✅ Country flags on ranges", reply_markup=get_admin_keyboard())
    else:
        bot.send_message(message.chat.id, 
            f"✨ Welcome {message.from_user.first_name}! ✨\n\n🌍 Panel: X ULTRA\n✅ Service: Facebook + Instagram\n✅ 2 Numbers per request\n✅ Auto Create Account (2-20) - French Language\n✅ Country flags on ranges",
            reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(func=lambda m: m.text == "🎲 GET NUMBER")
def handle_get_number(message):
    bot.send_message(message.chat.id, "📱 Select Service:", reply_markup=get_service_keyboard())

@bot.message_handler(func=lambda m: m.text == "⚡ AUTO CREATE")
def handle_auto_create(message):
    chat_id = message.chat.id
    
    # প্রাথমিক মেসেজ
    msg = bot.send_message(chat_id, "🔄 Fetching live ranges...")
    
    ranges_data = get_combined_fb_ig_ranges()
    bot.delete_message(chat_id, msg.message_id)
    
    if not ranges_data:
        bot.send_message(chat_id, "❌ No ranges available! Please try again later.")
        return
    
    # রেঞ্জ সংরক্ষণ করুন ইউজার ডাটাতে
    bot.send_message(chat_id, "📊 SELECT HOW MANY:", reply_markup=get_auto_create_keyboard())
    
    # টেম্পোরারি ডাটা সেভ করুন
    if not hasattr(bot, 'temp_ranges'):
        bot.temp_ranges = {}
    bot.temp_ranges[chat_id] = ranges_data

@bot.message_handler(func=lambda m: m.text in ["2️⃣", "3️⃣", "5️⃣", "8️⃣", "1️⃣2️⃣", "1️⃣5️⃣", "2️⃣0️⃣", "🔙 BACK"])
def handle_auto_create_count(message):
    chat_id = message.chat.id
    
    if message.text == "🔙 BACK":
        bot.send_message(chat_id, "🏠 Main Menu", reply_markup=get_main_keyboard(chat_id))
        return
    
    # সংখ্যা পার্স করুন
    count_map = {
        "2️⃣": 2,
        "3️⃣": 3,
        "5️⃣": 5,
        "8️⃣": 8,
        "1️⃣2️⃣": 12,
        "1️⃣5️⃣": 15,
        "2️⃣0️⃣": 20
    }
    
    count = count_map.get(message.text, 2)
    
    # রেঞ্জ ডাটা রিট্রিভ করুন
    if not hasattr(bot, 'temp_ranges') or chat_id not in bot.temp_ranges:
        bot.send_message(chat_id, "❌ Please click AUTO CREATE first!", reply_markup=get_main_keyboard(chat_id))
        return
    
    ranges_data = bot.temp_ranges[chat_id]
    
    # মেইন কীবোর্ড রিস্টোর করুন
    bot.send_message(chat_id, f"⚡ Starting creation of {count} account(s) in French language...\n🔄 Each account uses fresh session", reply_markup=get_main_keyboard(chat_id))
    
    # ব্যাকগ্রাউন্ড থ্রেডে একাউন্ট ক্রিয়েট করুন
    msg = bot.send_message(chat_id, "⏳ Initializing...")
    threading.Thread(target=auto_create_accounts, args=(chat_id, ranges_data, count, msg.message_id), daemon=True).start()
    
    # টেম্প ডাটা ক্লিয়ার করুন
    del bot.temp_ranges[chat_id]

@bot.message_handler(func=lambda m: m.text == "🔙 BACK")
def back_main(message):
    bot.send_message(message.chat.id, "🏠 Main Menu", reply_markup=get_main_keyboard(message.chat.id))

@bot.message_handler(func=lambda m: m.text == "🛠 ADMIN PANEL")
def admin_menu(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 Admin Panel:", reply_markup=get_admin_keyboard())

# ==================== এডমিন হ্যান্ডলার ====================
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.text in ["📢 BROADCAST", "📊 STATS"])
def admin_buttons(message):
    if message.text == "📢 BROADCAST":
        msg = bot.send_message(message.chat.id, "📢 Send broadcast message:")
        bot.register_next_step_handler(msg, broadcast_msg)
    elif message.text == "📊 STATS":
        users = len(get_all_users())
        active = len(get_active_numbers())
        settings = get_settings()
        bot.send_message(message.chat.id, f"📊 STATS\n👥 Users: {users}\n📱 Active: {active}\n💰 Price: {settings['otp_price']} BDT")

def broadcast_msg(message):
    users = get_all_users()
    success = 0
    for uid in users:
        try:
            bot.send_message(uid, f"📢 BROADCAST\n\n{message.text}")
            success += 1
            time.sleep(0.05)
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Sent to {success} users!")

# ==================== কলব্যাক হ্যান্ডলার ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    
    if data.startswith("copy_otp_"):
        otp_code = data.split("_")[2]
        bot.answer_callback_query(call.id, f"✅ OTP Copied: {otp_code}", show_alert=True)
        return
    
    if data == "main_menu":
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, "🏠 Main Menu", reply_markup=get_main_keyboard(chat_id))
        bot.answer_callback_query(call.id)
        return
    
    if data == "back_to_services":
        bot.edit_message_text("📱 Select Service:", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("refresh_"):
        service_type = data.split("_")[1]
        ranges_data = get_combined_fb_ig_ranges()
        display_name = "Facebook + Instagram"
        
        if ranges_data:
            bot.edit_message_text(f"🔥 Live Ranges for {display_name}:", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(ranges_data, service_type))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id)
        bot.answer_callback_query(call.id)
        return
    
    if data == "srv_combined":
        ranges_data = get_combined_fb_ig_ranges()
        if ranges_data:
            bot.edit_message_text("🔥 Live Ranges for Facebook + Instagram:", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(ranges_data, "combined"))
        else:
            bot.edit_message_text("❌ No ranges found!", chat_id, msg_id, reply_markup=get_service_keyboard())
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("range_"):
        parts = data.split("_")
        service_type = parts[1]
        range_code = parts[2]
        
        service_name = "Facebook/Instagram"
        
        bot.edit_message_text(f"⏳ Getting 2 numbers from {format_range_with_flag(range_code)}...", chat_id, msg_id, parse_mode="Markdown")
        
        numbers_found = []
        for i in range(2):
            number = xultra_fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service_name, range_code)
            time.sleep(0.5)
        
        if numbers_found:
            bot.delete_message(chat_id, msg_id)
            send_numbers_received_notification(chat_id, numbers_found, service_name, range_code)
        else:
            new_ranges = get_combined_fb_ig_ranges()
            bot.edit_message_text(f"❌ No numbers available!\nTry another range.", chat_id, msg_id, 
                                reply_markup=get_range_keyboard(new_ranges, service_type))
        
        bot.answer_callback_query(call.id)
        return
    
    if data.startswith("change_number_"):
        parts = data.split("_")
        service_name = parts[2]
        range_code = parts[3]
        
        bot.delete_message(chat_id, msg_id)
        loading_msg = bot.send_message(chat_id, f"⏳ Getting 2 new numbers...")
        
        numbers_found = []
        for i in range(2):
            number = xultra_fetch_number(range_code)
            if number:
                numbers_found.append(number)
                add_active_number(number, chat_id, service_name, range_code)
            time.sleep(0.5)
        
        bot.delete_message(chat_id, loading_msg.message_id)
        
        if numbers_found:
            send_numbers_received_notification(chat_id, numbers_found, service_name, range_code)
        else:
            bot.send_message(chat_id, "❌ No numbers available!", reply_markup=get_service_keyboard())
        
        bot.answer_callback_query(call.id)
        return

# ==================== OTP মনিটর ====================
sent_otps = set()

def otp_monitor():
    global sent_otps
    print("🔄 XULTRA OTP Monitor Started")
    while True:
        try:
            otps = xultra_check_otp()
            
            for otp_data in otps:
                phone = otp_data["phone"]
                key = f"{phone}_{otp_data['otp']}"
                
                if key not in sent_otps:
                    sent_otps.add(key)
                    active = get_active_numbers()
                    
                    if str(phone) in active:
                        a = active[str(phone)]
                        send_otp_notification(a["chat_id"], phone, a["service"], otp_data["otp"], 
                                             otp_data["message"], a["country_name"], 
                                             a["country_flag"], a["country_code"])
                        remove_active_number(phone)
                        print(f"📱 OTP Received: {phone} | {a['service']} | {otp_data['otp']}")
            
            if len(sent_otps) > 1000:
                sent_otps.clear()
                
        except Exception as e:
            print(f"Monitor Error: {e}")
        time.sleep(5)

# ==================== মেইন ====================
if __name__ == "__main__":
    print("=" * 50)
    print("XULTRA OTP BOT (Facebook + Instagram Only)")
    print("=" * 50)
    print("✅ Service: Facebook + Instagram")
    print("✅ Countries: All 240+ countries supported")
    print("✅ Auto-detect country from range prefix")
    print("✅ 2 Numbers per request")
    print("✅ Auto Create Facebook Account (2-20) - French Language")
    print("✅ Fresh Session for each account (cookies cleared)")
    print("✅ Random User Agent for each request")
    print("✅ OTP Notification for Auto Created Accounts")
    print("=" * 50)
    
    settings = get_settings()
    print(f"💰 OTP Price: {settings['otp_price']} BDT")
    
    print("\n🔍 Logging in...")
    if xultra_login():
        print("✅ Login Successful!")
    else:
        print("⚠️ Login Failed - check credentials")
    
    print("\n🤖 Bot Starting...")
    threading.Thread(target=otp_monitor, daemon=True).start()
    
    print("✅ Bot Running!")
    print("=" * 50)
    
    bot.infinity_polling(timeout=60)
