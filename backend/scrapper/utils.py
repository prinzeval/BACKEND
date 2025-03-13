# 4. scrapper/utils.py - New file for common utilities used across scraper modules
import random
import time
from urllib.parse import urljoin, urlparse
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# URL validation patterns
URL_PATTERN = re.compile(
    r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)',
    re.IGNORECASE
)
IMAGE_EXTENSIONS = re.compile(r'\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE)
UNWANTED_PREFIXES = ['data:image/svg+xml;charset=utf8,']

def is_valid_url(url, base_url=None):
    """Check if URL is valid and optionally if it starts with base_url."""
    is_valid = URL_PATTERN.match(url) is not None
    if base_url and is_valid:
        return url.startswith(base_url)
    return is_valid

def is_valid_link(url):
    """Check if URL is not an image."""
    return not bool(IMAGE_EXTENSIONS.search(url))

def is_in_whitelist(url, whitelist):
    """Check if URL is in whitelist or whitelist is empty."""
    return any(item in url for item in whitelist) if whitelist else True

def is_in_blacklist(url, blacklist):
    """Check if URL is in blacklist."""
    return any(item in url for item in blacklist) if blacklist else False

def fetch_with_selenium(url):
    """Fetch page content using Selenium for sites that block regular requests."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    time.sleep(random.randint(0, 1))  # Small random delay
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return page_source

def fetch_page(url):
    """Fetch page with fallback to Selenium if needed."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            return fetch_with_selenium(url)
        raise e
