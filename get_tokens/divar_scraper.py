from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os


#chorome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def get_script_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def scrap_data(url):
    driver.get(url)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'kt-page-title__title')))
    except:
        print("⏱️ Timeout waiting for page elements.")
        return None

    try:
        title = driver.find_element(By.CLASS_NAME, 'kt-page-title__title').text
    except:
        title = "Title not found"

    try:
        subtitle = driver.find_element(By.CLASS_NAME, 'kt-page-title__subtitle--responsive-sized').text
        subtitle_parts = subtitle.split('،')
        if len(subtitle_parts) >= 2:
            posted_date = subtitle_parts[0].strip()
            location = subtitle_parts[1].strip()
        else:
            posted_date = subtitle.strip()
            location = "Unknown"
    except:
        posted_date = "Date not found"
        location = "Location not found"

    try:
        all_values = driver.find_elements(By.CLASS_NAME, 'kt-unexpandable-row__value')
        offset = 1 if all_values and all_values[0].text.strip() in ['بله', 'خیر'] else 0
        price = all_values[offset].text.strip() if len(all_values) > offset else "Price not found"
        price_per_meter = all_values[offset + 1].text.strip() if len(all_values) > offset + 1 else "Price/m² not found"
        floor = all_values[offset + 2].text.strip() if len(all_values) > offset + 2 else "Floor not found"
    except:
        price = "Price not found"
        price_per_meter = "Price/m² not found"
        floor = "Floor not found"

    try:
        features = driver.find_elements(By.CLASS_NAME, 'kt-body--stable')
        elevator = parking = storage = None
        for item in features:
            text = item.text.strip()
            if 'آسانسور' in text:
                elevator = 'ندارد' not in text
            elif 'پارکینگ' in text:
                parking = 'ندارد' not in text
            elif 'انباری' in text:
                storage = 'ندارد' not in text
    except:
        elevator = parking = storage = None

    data = {
        "title": title,
        "posted_date": posted_date,
        "location": location,
        "price": price,
        "price_per_meter": price_per_meter,
        "floor": floor,
        "elevator": elevator,
        "parking": parking,
        "storage": storage,
        "url": url
    }

    return data


def load_existing_data(filename='output.json'):
    path = get_script_path(filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
                if isinstance(existing_data, list):
                    return existing_data
            except json.JSONDecodeError:
                pass
    return []


def save_batch_to_json(batch_data, filename='output.json'):
    path = get_script_path(filename)
    existing_data = load_existing_data(filename)

    existing_urls = {item['url'] for item in existing_data if 'url' in item}
    new_data = [item for item in batch_data if item['url'] not in existing_urls]

    if not new_data:
        print("⚠️ No new ads to save in this batch.")
        return

    existing_data.extend(new_data)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved {len(new_data)} new ads to {filename}")


def remove_token_from_file(token, filename='tokens.txt'):
    path = get_script_path(filename)
    with open(path, 'r', encoding='utf-8') as f:
        tokens = f.read().split(',')

    tokens = [t.strip() for t in tokens if t.strip() != token]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(','.join(tokens))


#load tokens
tokens_path = get_script_path('tokens.txt')
with open(tokens_path, 'r', encoding='utf-8') as token_file:
    tokens = token_file.read().split(',')

#remove first element if needed
if tokens:
    tokens.pop(0)

tokens = [t.strip() for t in tokens if t.strip()]
total_tokens = len(tokens)

base_url = "https://divar.ir/v/-/{}"
batch_data = []

for index, token in enumerate(tokens, start=1):
    url = base_url.format(token)
    print(f"\n🔹 [{index}/{total_tokens}] Processing token: {token}")
    print(f"🔍 URL: {url}")

    try:
        ad_data = scrap_data(url)
        if ad_data:
            batch_data.append(ad_data)
            remove_token_from_file(token)
    except Exception as e:
        print(f"❌ Error with token {token}: {e}")

    #save every n items
    if len(batch_data) >= 250:
        save_batch_to_json(batch_data)
        batch_data.clear()

#save items
if batch_data:
    save_batch_to_json(batch_data)

driver.quit()
