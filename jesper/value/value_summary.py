"""Calculating the Value Summary"""
from typing import List

import pandas as pd


def _get_value_summary_table(
    columns: List[str],
    index: List[str] = [
        "revenue per share",
        "eps",
        "fcf per share",
        "dividends per share",
        "capex per share",
        "book value per share",
        "shares outstanding",
        "Avg. annual P/E ratio",
        "revenue",
        "operating margin",
        "depreciation",
        "net profit",
        "income tax rate",
        "net profit margin",
        "working capital",
        "long-term debt",
        "equity",
        "roic",
        "return on capital",
        "return on equity",
    ],
) -> pd.DataFrame:
    """Returns empty Pandas Dataframe based on specified headers.

    :param headers: List of header names for constructing the DataFrame.
    :returns: empty pd.DataFrame.
    """
    return pd.DataFrame(index=index, columns=columns)


def get_value_summary(input_df: pd.DataFrame) -> pd.DataFrame:
    """."""
    # Construct results table storing the value summary.
    df = _get_value_summary_table(input_df.columns.tolist())

    # Per share calculations
    df.loc["revenue per share"] = (
        input_df.loc["revenue"].astype(float)
        / input_df.loc["weightedAverageShsOut"].astype(float)
    ).round(2)
    df.loc["eps"] = input_df.loc["eps"].astype(float).round(2)
    df.loc["fcf per share"] = (
        input_df.loc["freeCashFlow"].astype(float)
        / input_df.loc["weightedAverageShsOut"].astype(float)
    ).round(2)
    df.loc["dividends per share"] = input_df.loc["dividendsPaid"].astype(
        float
    ) / input_df.loc["weightedAverageShsOut"].astype(float)
    df.loc["dividends per share"] = (
        df.loc["dividends per share"].apply(lambda x: x * -1).round(2)
    )
    df.loc["capex per share"] = input_df.loc["capitalExpenditure"].astype(
        float
    ) / input_df.loc["weightedAverageShsOut"].astype(float)
    df.loc["capex per share"] = (
        df.loc["capex per share"].apply(lambda x: x * -1).round(2)
    )

    df.loc["book value per share"] = (
        (
            input_df.loc["totalAssets"].astype(float)
            - input_df.loc["totalLiabilities"].astype(float)
        )
        / input_df.loc["weightedAverageShsOut"].astype(float)
    ).round(2)

    df.loc["revenue"] = input_df.loc["revenue"].astype(int)

    df.loc["roic"] = (
        (
            input_df.loc["netIncome"].astype(float)
            * input_df.loc["netIncomeRatio"].astype(float).apply(lambda x: 1 - x)
            / (
                input_df.loc["totalLiabilities"].astype(float)
                - input_df.loc["totalCurrentLiabilities"].astype(float)
            )
        )
    ).round(4)

    print(df)
    return df
