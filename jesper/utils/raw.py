"""Read and Write"""
import os

import pandas as pd

from jesper.utils import get_project_root


def save_statements_to_csv(df: pd.DataFrame, stock: str):
    """Saves statements DataFrames to .csv"""
    # Construct file path.
    fpath = os.path.join(get_project_root(), "data/fundamentalData", f'{stock}.csv')
    print(fpath)
    print(df)
    print("")
    with open(fpath, mode='a+') as cs:
        # pre_df = pd.read_csv(fpath, index_col=0, na_values='(missing)')
        # print(pre_df)

        # df = pd.read_csv(cs, names=['ID','CODE'])
        df.to_csv(fpath)


def _fill_df(df: pd.DataFrame, pre_df: pd.DataFrame) -> pd.DataFrame:
    """Compares two pandas DataFrame & fills in the missing information."""
    # newdf = pd.concat([df, pre_df]).drop_duplicates(keep=True)
    c_headers = sorted(list(set(list(pre_df.columns)) | set(list(df.columns))), reverse=True)
    # c_headers = pre_df.columns.join(df.columns).drop_duplicates(keep=False)
    # c_headers = pd.concat([df.columns, pre_df.columns]).drop_duplicates(keep=False)
    c_h = pre_df.columns.intersection(df.columns)
    pre_h = pre_df.columns.difference(df.columns)
    new_h = df.columns.difference(pre_df.columns)
    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH ", c_headers)
    print("c h ", c_h)
    print("pre h ", pre_h)
    print("new h ", new_h)

    for c in df.columns.difference(pre_df.columns):
        pre_df[c] = df[c]
    # pre_df[new_h[0]] = df[new_h[0]]

    new_df = pre_df
    return new_df
