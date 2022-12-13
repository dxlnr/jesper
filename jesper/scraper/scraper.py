"""Basic Scraping functions."""
import json
import random
from typing import Dict

import backoff
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from jesper.scraper.chrome_user_agents import CHROME_USER_AGENTS

ROIC_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Alt-Used": "roic.ai",
    "Connection": "keep-alive",
    # 'Cookie': '',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
}


def get_event_page(url: str):
    """Downloads a webpage and returns a BeautifulSoup doc."""
    # Web API headers.
    headers = {"User-Agent": random.choice(CHROME_USER_AGENTS)}
    # Pull data from link.
    try:
        page_response = requests.get(url, headers=headers, timeout=1000)
    except:
        raise Exception("Failed to load page {}".format(url))
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_response.content, features="html.parser")

    return page_content


def get_page_content(url: str):
    """Scrapes a webpage and returns a BeautifulSoup doc."""
    # Construct headers dictionary.
    headers = ROIC_HEADERS
    headers["User-Agent"] = random.choice(CHROME_USER_AGENTS)
    # Pull data from link.
    try:
        page_response = requests.get(url, headers=headers, timeout=1000)
    except:
        raise Exception(f"Failed to load page {url}.")
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_response.content, features="html.parser")
    # Return structured data.
    return json.loads(page_content.select_one("#__NEXT_DATA__").text)


def get_page_content_browserless(
    url: str, browser_driver: str = "/usr/lib/chromium-browser/chromedriver"
):
    """Scrapes a webpage and returns a BeautifulSoup doc."""
    # Construct User Agent.
    user_agent = random.choice(CHROME_USER_AGENTS)
    # Add Options
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")

    # Boot up the selenium browser
    driver = webdriver.Chrome(
        browser_driver, options=options, chrome_options=chrome_options
    )
    driver.minimize_window()
    driver.get(url)
    page_source = driver.page_source
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_source, features="html.parser")

    return json.loads(page_content.select_one("#__NEXT_DATA__").text)


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: e.response is not None and e.response.status_code < 500,
)
@backoff.on_predicate(backoff.fibo, lambda x: len(x) == 0, max_value=13)
def get_request_url(
    url: str,
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    },
):
    """Get request response as str from url."""
    # Pull data from url.
    try:
        r = requests.get(url=url, headers=headers)
    except:
        raise requests.exceptions.RequestException(f"Failed to load page {url}.")

    r.raise_for_status()
    # Return prepared string.
    return (
        r.text.split("root.App.main =")[1].split("(this)")[0].split(";\n}")[0].strip()
    )
