import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

from src.scraper.scraper import get_event_page
from src.scraper.yahoo_finance_utils import convert_to_float


def scraper_to_statement(link: str) -> pd.DataFrame:
    r"""Scrape from link and convert to data frame.

    :param link: API endpoint as str.
    :returns: Pandas dataframe.
    """
    # Scrape raw data for parsing.
    page_content = get_event_page(link)

    # Params
    items = []
    temp_list = []
    final = []
    index = 0

    # Filter for specific items
    features = page_content.find_all("div", class_="D(tbr)")
    # Create headers
    for item in features[0].find_all("div", class_="D(ib)"):
        items.append(item.text)

    # Statement contents
    while index <= len(features) - 1:
        # Filter for each line of the statement.
        temp = features[index].find_all("div", class_="D(tbc)")
        for line in temp:
            temp_list.append(line.text)

        final.append(temp_list)
        temp_list = []
        index += 1

    df = pd.DataFrame(final[1:])
    df.columns = items
    df = convert_to_float(df)

    return df


def scraper_to_latest_stock_price(link: str) -> float:
    """Scrape yahoo finance for latest stock price.

    :param link: API endpoint as str.
    """
    # Scrape raw data for parsing.
    page_content = get_event_page(link)
    # Get closing price.
    price = page_content.find(
        "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
    ).text

    return price
