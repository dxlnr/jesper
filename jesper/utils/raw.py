"""Read and Write"""
import os

import pandas as pd


def save_statements_to_csv(df: pd.DataFrame, stock: str):
    """Saves statements DataFrames to .csv"""
    # Construct file path.
    fpath = os.path.join("data", f'{stock}.csv')

    with open(fpath, mode='w') as cs:
        df.to_csv(fpath)
