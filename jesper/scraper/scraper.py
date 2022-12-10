"""Basic Scraping functions."""
import json
from typing import Dict

import backoff
import requests
from bs4 import BeautifulSoup

from jesper.scraper.user_agents import USER_AGENTS


def get_event_page(url: str):
    """Downloads a webpage and returns a BeautifulSoup doc."""
    # Web API headers.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
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
    # Pick up a random user agent header.
    user_agent = random.choice(USER_AGENTS)
    # 
    headers = {'User-Agent': user_agent}
    # Pull data from link.
    try:
        page_response = requests.get(url, headers=headers, timeout=1000)
    except:
        raise Exception(f"Failed to load page {url}.")
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_response.content, features="html.parser")
    # Return structured data.
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
