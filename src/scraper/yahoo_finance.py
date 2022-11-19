import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

# import re
# from selenium import webdriver
# import chromedriver_binary

from src.scraper.utils import convert_to_float


def scraper_to_statement(link: str):
    r"""Scrape from link and convert to data frame.

    :param link: API endpoint as str.
    :returns: Pandas dataframe.
    """
    items = []
    temp_list = []
    final = []
    index = 0

    # Web API headers.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    # Pull data from link.
    page_response = requests.get(link, headers=headers, timeout=1000)
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_response.content, features="lxml")
    # Filter for items we want
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
