"""roic.ai Scraping functions"""
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup

from jesper.scraper import get_page_content


def save_financial_info_roic(
    stocks: List[str], max_threads: int = 10
) -> None:
    """."""
    threads = min(max_threads, len(stocks))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(scrape_roic, stocks)


def scrape_roic(ticker: str) -> pd.DataFrame:
    """Scrapes roic.ai for fundamental financial information of a stock."""
    # Construct the url.
    url = f"https://roic.ai/financials/{ticker}?fs=annual"
    # Get the data.
    data = get_page_content(url)
    #
    # data["props"]["pageProps"]["data"]["data"]
    #
    # '_id',
    # 'symbol',
    # '__v',
    # 'bsq',
    # 'bsy',
    # 'cfq',
    # 'cfy',
    # 'earningscalls',
    # 'historical',
    # 'historicalyears',
    # 'historicalyearsavg',
    # 'isq',
    # 'isy',
    # 'outlook',
    # 'ttmpriceavg'

    # Convert data to pandas DataFrame
    #
    # 'bsy': Balance Sheet yearly
    # 'isy': Income Statement yearly
    # 'cfy': Cashflow Statement yearly
    is_df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["isy"])
    bs_df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["bsy"])
    cf_df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["cfy"])
    # Concat to one DataFrame
    df = pd.concat([is_df, bs_df, cf_df])
    # Remove duplicates
    df = df[~df.index.duplicated(keep="first")]
    return df


def _convert_data_to_df(data: List[Dict]) -> pd.DataFrame:
    """Picks up a lcist of dicts and converts it to DataFrame."""
    df = pd.DataFrame(data)
    # Make sure dataframe is actually fetched correctly.
    if df.empty:
        return df
    # Delete various information.
    if "symbol" in df:
        del df["symbol"]
    if "link" in df:
        del df["link"]
    if "finalLink" in df:
        del df["finalLink"]
    if "calendarYear" in df:
        del df["calendarYear"]
    if "period" in df:
        del df["period"]
    if "cik" in df:
        del df["cik"]

    # Use date as index & convert it to pandas datetime.
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index, format="%m/%d/%Y")
    # Use only the year.
    df.index = df.index.year

    return df.transpose()
