from typing import List

import pandas as pd

from src.scraper.yahoo_finance_utils import extract_ttm_value
from src.scraper.yahoo_finance import scraper_to_statement


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
        "Outstanding Shares",
        "Per Share",
    ]
) -> pd.DataFrame:
    """Returns empty Pandas Dataframe based on specified headers.

    :param headers: List of header names for constructing the DataFrame.
    :returns: empty pd.DataFrame.
    """
    return pd.DataFrame(columns=headers)


def compound(x: float, y: float) -> float:
    """Performs a compounding calculation."""
    z = (1 + x) ** y
    return z


def discount(x: float, y: float) -> float:
    """Performs a discounting calculation."""
    z = 1 / (1 + x) ** y
    return z


def intrinsic_value(
    stock: str, compound_rate: float = 0.1, discount_rate: float = 0.05, terms: int = 5
) -> pd.DataFrame:
    """Computes the intrinsic value of a stock.

    The intrinsic value is the discounted value of the cash that
    can be taken out of a business during its remaining life.
    As our definition suggests, intrinsic value is an estimate
    rather than a price figure. And it is definitely an estimate
    that must be changed as interest rates move or forecast or future cash
    flows are revised. Two people looking at the same set of facts
    almost inevitably come up with slightly different intrinsic value figures.

    :param stock: Acronym of specific stock. E.g. "AAPL" for the Apple Inc.
    :param compound_rate:
    :param discount_rate:
    :param terms:
    :returns: pd.DataFrame holding all the relevant information regarding the
        intrinsic value of a specific stock.
    """
    # Construct links based on stock acronym.
    is_link = f"https://finance.yahoo.com/quote/{stock}/financials?p={stock}"
    bs_link = f"https://finance.yahoo.com/quote/{stock}/balance-sheet?p={stock}"
    cf_link = f"https://finance.yahoo.com/quote/{stock}/cash-flow?p={stock}"

    # Run scraping and return data frame.
    income_df = scraper_to_statement(is_link)
    balance_sheet_df = scraper_to_statement(bs_link)
    cashflow_df = scraper_to_statement(cf_link)

    # Instantiate resulting table.
    df = return_table()

    # Pulling in the desired fields ebit, depreciation & capex
    df.at[0, "incomeBeforeTax"] = extract_ttm_value(income_df, "EBIT")
    df.at[0, "depreciation"] = extract_ttm_value(income_df, "Reconciled Depreciation")
    df.at[0, "capitalExpenditures"] = extract_ttm_value(
        cashflow_df, "Capital Expenditure"
    )

    # Calculating Average Capital Expenditure.
    cp_exp_row = cashflow_df[cashflow_df["Breakdown"] == "Capital Expenditure"]
    mean_capex = cp_exp_row.iloc[:, 2:].mean(axis=1).astype(float)
    df.at[0, "Average Capex"] = mean_capex.iloc[0]

    # Calculating Owners Earnings
    earnings = df["incomeBeforeTax"] + df["depreciation"] - df["Average Capex"]
    df.at[0, "Owners Earnings"] = earnings.iloc[0]

    # Find the DCF Multiplier
    dfc = [compound(compound_rate, y) for y in range(1, terms + 1)]
    dfd = [discount(discount_rate, y) for y in range(1, terms + 1)]
    amounts = list(map(lambda x, y: x * y, dfc, dfd))

    # Find the DCF Multiplier
    df["DCF_multiplier"] = sum(amounts)

    # Find the PV (Present Value) Multiplier
    df["PV_multiplier"] = amounts[-1] / discount_rate

    # Calculate the intrinsic value
    df["OE*PV"] = df["Owners Earnings"] * df["PV_multiplier"]
    df["OE*DCF"] = df["Owners Earnings"] * df["DCF_multiplier"]
    df["Intrinsic Value"] = df["OE*PV"] + df["OE*DCF"]

    # Find Outstanding Shares
    df.at[0, "Outstanding Shares"] = (
        income_df[income_df["Breakdown"] == "Diluted Average Shares"].iloc[:, 2].iloc[0]
    )
    df["Per Share"] = df["Intrinsic Value"] / df["Outstanding Shares"]

    return df
