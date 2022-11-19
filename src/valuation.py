from typing import List

import pandas as pd


def return_table(
    headers: List[str] = [
        "incomeBeforeTax",
        "depreciation",
        "capitalExpenditures",
        "Average Capex",
        "Owners Earnings",
        "PV_multiplier",
        "DCF_multiplier",
        "OE*PV",
        "OE*DCF",
        "Intrinsic Value",
        "Shares",
        "Per Share",
    ]
) -> pd.DataFrame:
    """Returns empty Pandas Dataframe based on specified headers.

    :param headers: List of header names for constructing the DataFrame.
    :returns: empty pd.DataFrame.
    """
    return pd.DataFrame(columns=headers)
