import json
import csv
import time
import logging
import re
import urllib.robotparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from urllib import parse

# Setup logging
logging.basicConfig(filename='email_parser.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def is_valid_email(email):
    invalid_criteria = ["sentry.io", "meu@email.com.br"]
    return not any(criterion in email for criterion in invalid_criteria)

def wait_for_page_load(driver, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except TimeoutException:
        logging.warning(f"Page load timed out after {timeout} seconds for {driver.current_url}")

def find_emails_with_selenium(url):
    try:
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        wait_for_page_load(driver, timeout=15)  # Increased timeout

        page_source = driver.page_source
        email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,6}\b")
        emails = set(re.findall(email_pattern, page_source))

        driver.quit()
        return {email for email in emails if is_valid_email(email)}
    except Exception as e:
        logging.error(f"Error with Selenium fetching {url}: {e}, {str(e)}")
        return set()

def is_allowed_by_robots(url):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, 'robots.txt'))
    rp.read()
    return rp.can_fetch("*", url)

def process_url(url):
    if is_allowed_by_robots(url):
        emails = find_emails_with_selenium(url)
    else:
        logging.info(f"Scraping blocked by robots.txt: {url}")
        emails = set()
    return {'url': url, 'emails': list(emails)} if emails else {'url': url, 'must_find_email': True}

def process_batch(urls):
    collected_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for result in executor.map(process_url, urls):
            collected_data.append(result)
            time.sleep(1)  # Rate limiting
    return collected_data

input_csv_file = "C:\\Users\\luizm\\webscraper\\phase2\\filtered_low_scores.csv"
output_json_file = "C:\\Users\\luizm\\webscraper\\phase2\\final_data.json"
batch_size = 50  # Define batch size

all_data = []
with open(input_csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader, None)  # Skip the header row
    batch = []
    for row in reader:
        batch.append(row[0])
        if len(batch) == batch_size:
            all_data.extend(process_batch(batch))
            batch = []
    if batch:
        all_data.extend(process_batch(batch))

with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(all_data, file, indent=4)

logging.info("Data saved to " + output_json_file)
