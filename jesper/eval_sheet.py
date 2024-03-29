import os
from typing import List

import numpy as np
import pandas as pd

from jesper.scraper.yahoo_finance import scraper_to_latest_stock_price
from jesper.utils import get_project_root
from jesper.valuation import iv_roic


def create_eval_table(
    headers: List[str] = [
        "stock",
        "terms",
        "cr",
        "dr",
        "tv",
        "avg growth",
        "intrinsic value",
        "stock price",
        "safety margin",
    ]
) -> pd.DataFrame:
    """Returns empty Pandas Dataframe based on specified headers.

    :param headers: List of header names for constructing the DataFrame.
    :returns: empty pd.DataFrame.
    """
    return pd.DataFrame(columns=headers)


def eval_value_based_stocks(
    stocks: List[str],
    compound_rate: float = 0.1,
    discount_rate: float = 0.15,
    terminal_value: int = 10,
    terms: int = 10,
    path_to_csv: str = "",
    save_results_file: str = "",
):
    """Reads in a list of stock ticker symbols and spits out the evaluation
    useful for value based investing.

    :param stocks: List of stocks that should be evaluated.
    :param compound_rate: Assumption about the company’s future growth.
    :param discount_rate:
    :param terminal_value:
    :param terms:
    :param path_to_csv: Path to presaved .csv file in order to avoid scraping.
    :param save_results_file: Specifies if results should be saved and where.
    :returns pd.DataFrame:
        Table that holds holds the intrinsic value and compares to current price.
               terms  avg growth  intrinsic value  stock price  safety margin
        stock
        TGT       10      0.2033           428.34       150.63     35.17%
        TSM       10      0.3529           174.05        80.09     45.92%
    """
    # Instantiate resulting table.
    df = create_eval_table()

    for idx, stock in enumerate(stocks):
        print(f"({idx+1}) Calculating intrinsic_value for {stock}.")
        # Compute the intrinsic value table.
        iv_df = iv_roic(
            stock,
            compound_rate,
            discount_rate,
            terminal_value,
            terms,
            path_to_csv=path_to_csv,
        )
        # Scrape the latest stock price from yahoo finance.
        url = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
        latest_stock_price = scraper_to_latest_stock_price(url, stock)

        # Fill up the dataframe.
        df.at[idx, "stock"] = stock
        df.at[idx, "terms"] = iv_df["terms"].iloc[0]
        df.at[idx, "cr"] = iv_df["Compound Rate"].iloc[0]
        df.at[idx, "dr"] = iv_df["Discount Rate"].iloc[0]
        df.at[idx, "tv"] = iv_df["Terminal Value"].iloc[0]
        df.at[idx, "avg growth"] = iv_df["Average Growth Rate"].iloc[0]
        df.at[idx, "stock price"] = latest_stock_price
        if len(iv_df.index) != 0:
            df.at[idx, "intrinsic value"] = float(iv_df["Per Share"].iloc[0])
            if iv_df["Per Share"].iloc[0] == 0.0:
                df.at[idx, "safety margin"] = np.nan
            else:
                df.at[idx, "safety margin"] = float(latest_stock_price) / float(
                    iv_df["Per Share"].iloc[0]
                )

    df["intrinsic value"] = df["intrinsic value"].astype(float).round(2)
    df["avg growth"] = df["avg growth"].astype(float).round(4)
    df["safety margin"] = df["safety margin"].astype(float).round(4)
    df.set_index("stock", inplace=True)

    if save_results_file:
        # Construct file path.
        fpath = os.path.join(get_project_root(), "results", f"{save_results_file}.csv")
        df.to_csv(fpath)
        print(f"Saved results to {fpath}.")
    return df
