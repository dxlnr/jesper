"""roic.ai Scraping functions"""
from typing import Dict, List

import pandas as pd

from jesper.scraper import get_page_content, get_page_content_browserless


def scrape_roic(ticker: str) -> pd.DataFrame:
    """Scrapes roic.ai for fundamental financial information of a stock."""
    # Construct the url.
    url = f"https://roic.ai/financials/{ticker}?fs=annual"
    # Get the data.
    # data = get_page_content(url)
    data = get_page_content_browserless(url)
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
    is_df = is_df.loc[:, ~is_df.columns.duplicated()]
    bs_df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["bsy"])
    bs_df = bs_df.loc[:, ~bs_df.columns.duplicated()]
    cf_df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["cfy"])
    cf_df = cf_df.loc[:, ~cf_df.columns.duplicated()]

    # Concat to one DataFrame
    df = pd.concat([is_df, bs_df, cf_df], ignore_index=True)
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

    # Use date as index & convert it to pandas datetime.
    df.set_index("date", inplace=True)
    df.index = pd.to_datetime(df.index, format="%m/%d/%Y")
    # Use only the year.
    df.index = df.index.year

    return df.transpose()
