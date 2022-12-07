import os
from typing import List

import pandas as pd

from jesper.scraper.yahoo_finance import scraper_to_latest_stock_price
from jesper.utils import get_project_root
from jesper.valuation import intrinsic_value


def create_eval_table(
    headers: List[str] = [
        "stock",
        "intrinsic value",
        "latest stock price",
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
    discount_rate: float = 0.05,
    terms: int = 5,
    save_results_file: str = "",
):
    """Reads in a list of stock ticker symbols and spits out the evaluation
    useful for value based investing.

    :param stocks: List of stocks that should be evaluated.
    :param compound_rate:
    :param discount_rate:
    :param terms:
    :returns pd.DataFrame:
        Table that holds holds the intrinsic value and compares to current price.
                intrinsic value latest stock price    safety margin
        stock
        LW              148.64              87.73  59.02%
        AXP             545.93             156.75  28.71%
        ON              159.58              73.04  45.77%
        SLB             135.73              52.79  38.89%
        EQR             180.27              64.11  35.56%
    """
    # Instantiate resulting table.
    df = create_eval_table()

    for idx, stock in enumerate(stocks):
        print(f"({idx+1}) Calculating intrinsic_value for {stock}.")
        # Compute the intrinsic value table.
        iv_df = intrinsic_value(stock, compound_rate, discount_rate, terms)
        # Scrape the latest stock price from yahoo finance.
        url = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
        latest_stock_price = scraper_to_latest_stock_price(url)

        # Fill up the dataframe.
        df.at[idx, "stock"] = stock
        df.at[idx, "latest stock price"] = latest_stock_price
        if len(iv_df.index) != 0:
            df.at[idx, "intrinsic value"] = iv_df["Per Share"].iloc[0]
            df.at[idx, "safety margin"] = float(latest_stock_price) / float(
                iv_df["Per Share"].iloc[0]
            )

    df.set_index("stock", inplace=True)

    if save_results_file:
        # Construct file path.
        fpath = os.path.join(get_project_root(), "results", f"{save_results_file}.csv")
        df.to_csv(fpath)
        print(f"Saved results to {fpath}.")
    return df
