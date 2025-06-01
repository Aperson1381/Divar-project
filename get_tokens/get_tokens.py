import requests
import os
import time
from bs4 import BeautifulSoup

# مسیر فایل‌ها
current_dir = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_dir, 'tokens.txt')

# تابع خواندن توکن‌های قبلی


def load_existing_tokens():
    if os.path.exists(tokens_file_path):
        with open(tokens_file_path, 'r', encoding='utf-8') as f:
            tokens = f.read().strip()
            return set(tokens.split(',')) if tokens else set()
    return set()

# تابع ذخیره توکن‌های جدید


def save_new_tokens(new_tokens):
    if not new_tokens:
        return
    with open(tokens_file_path, 'a', encoding='utf-8') as f:
        existing = os.path.getsize(tokens_file_path) > 0
        f.write((',' if existing else '') + ','.join(new_tokens))

# تابع اصلی استخراج


def extract_and_update_tokens():
    url = 'https://divar.ir/s/tehran/buy-apartment'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page. Status: {response.status_code}")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all(
        'article', class_='kt-post-card kt-post-card--outlined kt-post-card')

    existing_tokens = load_existing_tokens()
    print(f"Loaded {len(existing_tokens)} existing tokens.")

    new_tokens = []

    for article in articles:
        a_tag = article.find('a', class_='kt-post-card__action')
        if a_tag and 'href' in a_tag.attrs:
            ad_id = a_tag['href'].split('/')[-1]
            if ad_id not in existing_tokens:
                new_tokens.append(ad_id)

    if new_tokens:
        print(f"Found {len(new_tokens)} new tokens.")
        save_new_tokens(new_tokens)
    else:
        print("No new tokens found.")

    return len(new_tokens)


# تعداد مورد نظر توکن‌ها
target_token_count = 1000

# اجرای حلقه تا رسیدن به تعداد مورد نظر
while True:
    extract_and_update_tokens()

    all_tokens = load_existing_tokens()
    print(f"Total tokens collected: {len(all_tokens)}")

    if len(all_tokens) >= target_token_count:
        print(f"Target of {target_token_count} tokens reached!")
        break

    time.sleep(5)
