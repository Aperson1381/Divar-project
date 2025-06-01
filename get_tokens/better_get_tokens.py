from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os

# file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
tokens_file_path = os.path.join(current_dir, 'tokens.txt')

# def for read previous tokens
def load_existing_tokens():
    if os.path.exists(tokens_file_path):
        with open(tokens_file_path, 'r', encoding='utf-8') as f:
            tokens = f.read().strip()
            return set(tokens.split(',')) if tokens else set()
    return set()

# def get new tokens
def save_new_tokens(new_tokens):
    if not new_tokens:
        return
    with open(tokens_file_path, 'a', encoding='utf-8') as f:
        existing = os.path.getsize(tokens_file_path) > 0
        f.write((',' if existing else '') + ','.join(new_tokens))

# chorome setting
def get_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# close map feature if needed
def close_map_button_if_exists(driver):
    try:
        time.sleep(2)
        wait = WebDriverWait(driver, 5)
        close_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'kt-fab-button__icon')))
        driver.execute_script("arguments[0].scrollIntoView();", close_button)
        close_button.click()
        print("Map closed")
        time.sleep(1)
    except (NoSuchElementException, ElementClickInterceptedException):
        print("Map close button not found or not clickable.")
    except Exception as e:
        print(f"Unexpected error while closing map: {e}")

# clicl on load more button
def click_load_more_if_exists(driver):
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.post-list__load-more-btn-be092')
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button.click()
        print("Clicked 'Load more ads' button.")
        time.sleep(3)
    except NoSuchElementException:
        print("No 'Load more ads' button found.")
    except ElementClickInterceptedException:
        print("Could not click 'Load more ads' button.")
    except Exception as e:
        print(f"Unexpected error while clicking load more: {e}")

# get tags
def extract_and_update_tokens(driver):
    existing_tokens = load_existing_tokens()
    print(f"Loaded {len(existing_tokens)} existing tokens.")

    new_tokens = []

    articles = driver.find_elements(By.CLASS_NAME, 'unsafe-kt-post-card')
    for i in range(len(articles)):
        try:
            current_articles = driver.find_elements(By.CLASS_NAME, 'unsafe-kt-post-card')
            if i >= len(current_articles):
                break
            article = current_articles[i]
            a_tag = article.find_element(By.CLASS_NAME, 'unsafe-kt-post-card__action')
            href = a_tag.get_attribute('href')
            ad_id = href.split('/')[-1]
            if ad_id not in existing_tokens:
                new_tokens.append(ad_id)
        except (NoSuchElementException, StaleElementReferenceException):
            continue

    if new_tokens:
        print(f"Found {len(new_tokens)} new tokens.")
        save_new_tokens(new_tokens)
    else:
        print("No new tokens found.")

    return len(new_tokens)

# run and needs
target_token_count = 135000
driver = get_driver()
driver.get('https://divar.ir/s/tehran/buy-apartment')
time.sleep(5)

scroll_pause = 3
scroll_try = 0
max_scroll_tries = 30
close_map_button_if_exists(driver)

previous_token_count = 0
same_count_tries = 0

while True:
    extract_and_update_tokens(driver)

    all_tokens = load_existing_tokens()
    current_token_count = len(all_tokens)
    print(f"Total tokens collected: {current_token_count}")

    if current_token_count >= target_token_count:
        print(f"Target of {target_token_count} tokens reached!")
        break

    if current_token_count == previous_token_count:
        same_count_tries += 1
        if same_count_tries >= 2:
            print("Token count not increasing. Trying to click 'Load more ads' button.")
            click_load_more_if_exists(driver)
            same_count_tries = 0
    else:
        same_count_tries = 0

    previous_token_count = current_token_count

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(scroll_pause)

    #if u need run with scroll
    """scroll_try += 1
    if scroll_try >= max_scroll_tries:
        print("Reached max scroll limit.")
        break"""

driver.quit()
