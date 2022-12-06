"""Read and Write"""
import os
from typing import List

import numpy as np
import pandas as pd

from jesper.scraper.yahoo_finance import (
    get_financial_info,
    get_timeseries_financial_statements,
)
from jesper.utils import get_project_root


def save_stocks_finance_info(stocks: List[str]):
    """Read in the fundamental data from stocks & save it csv."""
    for idx, stock in enumerate(stocks):
        print(f"({idx+1}) Scraping financial information for {stock}.")
        # Retrieve main financial information.
        df = get_financial_info(stock)
        # Retrieve from timeseries data.
        adds_df = get_timeseries_financial_statements(
            stock, "financials", str(list(df.columns)[-1])
        )
        # Append by timeseries data.
        df = pd.concat([df, adds_df])

        # Save it to csv.
        save_statements_to_csv(df, stock)


def save_statements_to_csv(df: pd.DataFrame, stock: str):
    """Saves statements DataFrames to .csv"""
    # Construct file path.
    fpath = os.path.join(get_project_root(), "data/fundamentalData", f"{stock}.csv")

    # Check if file already exists.
    if os.path.exists(fpath):
        # Read csv
        pre_df = pd.read_csv(fpath, index_col=0, na_values="(missing)")
        pre_df.columns = pre_df.columns.astype(int)

        new_df = _fill_df(df, pre_df)

        new_df.to_csv(fpath)
    else:
        df.to_csv(fpath)
    print(f"Saved financial information of {stock} to {fpath}.")


def _fill_df(df: pd.DataFrame, pre_df: pd.DataFrame) -> pd.DataFrame:
    """Compares two pandas DataFrame & fills in the missing information."""
    result_df = pre_df.copy(deep=True)

    # Append new rows.
    for r in df.index.difference(result_df.index):
        result_df.loc[r] = df.loc[r]

    # Scan for differences and overwrite a new value.
    for row in result_df.itertuples():
        for k in result_df.keys():
            if (row.Index in df.index) and (k in df.columns):
                if not np.isnan(np.float_(df.loc[row.Index][k])):
                    result_df.at[row.Index, k] = df.loc[row.Index][k]

    # Append new column
    for c in df.columns.difference(result_df.columns):
        result_df[c] = df[c]

    # Sort the columns & return.
    return result_df.reindex(sorted(result_df.columns, reverse=True), axis=1)
