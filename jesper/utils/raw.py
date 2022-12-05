"""Read and Write"""
import os

import pandas as pd

from jesper.utils import get_project_root


def save_statements_to_csv(df: pd.DataFrame, stock: str):
    """Saves statements DataFrames to .csv"""
    # Construct file path.
    fpath = os.path.join(get_project_root(), "data/fundamentalData", f"{stock}.csv")
    print(fpath)
    print(df)
    print("")
    with open(fpath, mode="a+") as cs:
        # pre_df = pd.read_csv(fpath, index_col=0, na_values='(missing)')
        # print(pre_df)

        # df = pd.read_csv(cs, names=['ID','CODE'])
        df.to_csv(fpath)


def _fill_df(df: pd.DataFrame, pre_df: pd.DataFrame) -> pd.DataFrame:
    """Compares two pandas DataFrame & fills in the missing information."""
    # Append new rows.
    for r in df.index.difference(pre_df.index):
        pre_df.loc[r] = df.loc[r]

    # Scan for differences and overwrite a new value.
    for row in pre_df.itertuples():
        for k in pre_df.keys():
            if (row.Index in df.index) and (k in df.columns):
                pre_df.at[row.Index, k] = df.loc[row.Index][k]

    # Append new column
    for c in df.columns.difference(pre_df.columns):
        pre_df[c] = df[c]

    # Sort the columns & return.
    return pre_df.reindex(sorted(pre_df.columns, reverse=True), axis=1)
