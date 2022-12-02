import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

from jesper.scraper import get_event_page
from jesper.scraper.scraper import _parse_json


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

    # Catch exception and return empty Dataframe.
    if len(features) == 0:
        return pd.DataFrame()

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


def _parse_table(json_info):
    """."""
    df = pd.DataFrame(json_info)

    if df.empty:
        return df
    del df["maxAge"]

    df.set_index("endDate", inplace=True)
    df.index = pd.to_datetime(df.index, unit="s")
    df.index = df.index.year

    return df.transpose()


def get_balance_sheet(ticker: str, annual: bool = True):
    """Scrapes balance sheet from Yahoo Finance for an input ticker.

    :param ticker:
    :param annual: Yahoo Finance offers stats annual & quarterly.
    """
    bs_link = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    json_info = _parse_json(bs_link)
    try:
        if annual:
            tmp = json_info["balanceSheetHistory"]["balanceSheetStatements"]
        else:
            tmp = json_info["balanceSheetHistoryQuarterly"]["balanceSheetStatements"]
    except:
        tmp = []

    return _parse_table(tmp)


def get_income_statement(ticker: str, annual: bool = True):
    """Scrape income statement from Yahoo Finance for an input ticker.

    :param ticker:
    :param annual: Yahoo Finance offers stats annual & quarterly.
    """
    in_link = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    json_info = _parse_json(in_link)

    if annual:
        tmp = json_info["incomeStatementHistory"]["incomeStatementHistory"]
    else:
        tmp = json_info["incomeStatementHistoryQuarterly"]["incomeStatementHistory"]

    return _parse_table(tmp)


def get_cash_flow(ticker: str, annual: bool = True):
    """Scrapes the cash flow statement from Yahoo Finance for an input ticker.

    :param ticker:
    :param annual: Yahoo Finance offers stats annual & quarterly.
    """
    cf_link = f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}"
    json_info = _parse_json(cf_link)

    if annual:
        tmp = json_info["cashflowStatementHistory"]["cashflowStatements"]
    else:
        tmp = json_info["cashflowStatementHistoryQuarterly"]["cashflowStatements"]

    return _parse_table(tmp)


def get_balance_sheet_from_yfinance_web(ticker):
    from datetime import datetime
    url = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    header = {'Connection': 'keep-alive',
                'Expires': '-1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                }

    r = requests.get(url, headers=header)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    div = soup.find_all('div', attrs={'class': 'D(tbhg)'})
    if len(div) < 1:
        print("Fail to retrieve table column header")
        exit(0)

    col = []
    for h in div[0].find_all('span'):
        text = h.get_text()
        if text != "Breakdown":
            col.append(datetime.strptime(text, "%m/%d/%Y"))

    df = pd.DataFrame(columns=col)
    for div in soup.find_all('div', attrs={'data-test': 'fin-row'}):
        i = 0
        idx = ""
        val = []
        for h in div.find_all('span'):
            if i == 0:
                idx = h.get_text()
            else:
                num = int(h.get_text().replace(",", "")) * 1000
                val.append( num )
            i += 1
        row = pd.DataFrame([val], columns=col, index=[idx] )
        df = df.append(row)

    return df


def extract_latest_value(df: pd.DataFrame, v_name: str) -> float:
    """Extract value latest value from sheet."""
    for k in df.keys():
        if isinstance(num := extract_k_value(df, k, v_name), float):
            return num

    raise Exception(f"No \'{v_name}\' value found.")


def extract_k_value(df: pd.DataFrame, v_key: str, v_name: str) -> float:
    """Extract value from specific key."""
    return df[v_key].loc[df["Breakdown"] == v_name].values[0]


def extract_ttm_value(df: pd.DataFrame, v_name: str) -> float:
    """Extract value from Trailing 12 months (TTM)."""
    return df["ttm"].loc[df["Breakdown"] == v_name].values[0]


def has_digits(in_str: str) -> bool:
    """Returns Bool if str contains digits."""
    return any(char.isdigit() for char in in_str)


def convert_to_float(df: pd.DataFrame):
    """Takes scraped dataframe and converts the str numbers to floats."""
    for idx, key in enumerate(df.columns):
        if idx == 0:
            continue

        df[key] = [
            float(str(i).replace(",", "")) if has_digits(i) else i for i in df[key]
        ]
    return df
