"""Calculate various Evaluations of Stocks."""
import os
from typing import List

import pandas as pd

from jesper.scraper.roic import scrape_roic
from jesper.scraper.yahoo_finance import (
    get_financial_info,
    get_timeseries_financial_statements,
)
from jesper.utils import get_project_root


def _return_table(
    headers: List[str] = [
        "operatingIncome",
        "depreciation",
        "capex",
        "Owners Earnings",
        "Average Growth Rate",
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


def get_financials(stock: str, path_to_csv: str = "") -> pd.DataFrame:
    """Get all the fundamental financial information about a stock.

    :param stock: Acronym of specific stock. E.g. "AAPL" for the Apple Inc.
    :param scrape: Boolean to define whether the data should be scraped from
        webpage or read from .csv file.
    """
    # Construct file path.
    fpath = os.path.join(get_project_root(), path_to_csv, f"{stock}.csv")
    if os.path.exists(fpath):
        print(f"Reading financial information for {stock} from {fpath}.")
        # Read the information.
        df = pd.read_csv(fpath, index_col=0, na_values="(missing)")
        df.columns = df.columns.astype(float).astype(int)
    else:
        print(f"Scraping financial information for {stock}.")
        # Scrape the information.
        df = scrape_roic(ticker=stock)
        # Save to file.
        df.to_csv(fpath)
        print(f"Saved financials for {stock} to {fpath}.")

    return df


def compound(x: float, y: float) -> float:
    """Performs a compounding calculation."""
    z = (1 + x) ** y
    return z


def discount(x: float, y: float) -> float:
    """Performs a discounting calculation."""
    z = 1 / (1 + x) ** y
    return z


def calc_avg_growth_rate(y: List[int]) -> float:
    """Computes average growth rate."""
    gr = [(y[idx - 1] / y[idx]) - 1 for idx in range(1, len(y))]
    return sum(gr) / len(gr)


def annual_report_readings(stock: str):
    """Returns an investing stock screener dataframe."""
    # Run scraping and return data frame.
    df = get_financials(stock)

    # Define values from various sheets.
    values = {
        "totalRevenue": df,
        "ebit": df,
        "totalStockholderEquity": df,
        "longTermDebt": df,
    }

    r_l = list()
    for k, v in values.items():
        try:
            r_l.append(pd.concat([v.loc[k]], axis=1))
        except:
            print(f"No {k} found in the data.")

    df = pd.concat(r_l, axis=1)

    if len(values) < 4:
        return df
    else:
        df["Operating Margin"] = df["ebit"] / df["totalRevenue"]
        df["Debit to Equity"] = df["longTermDebt"] / df["totalStockholderEquity"]
        df["Return on Equity"] = df["ebit"] / df["totalStockholderEquity"]
        df["Return on Invested Capital"] = df["ebit"] / (
            df["totalStockholderEquity"] + df["longTermDebt"]
        )

    return df


def iv_roic(
    stock: str,
    compound_rate: float = 0.05,
    discount_rate: float = 0.15,
    terminal_value: int = 10,
    terms: int = 5,
    free_cash_flow: bool = False,
    path_to_csv: str = "data/roic",
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
    :param scrape: Boolean to define whether the data should be scraped from
        webpage or read from .csv file.
    :returns: pd.DataFrame holding all the relevant information regarding the
        intrinsic value of a specific stock.
    """
    # Read from .csv or scrape and return data frame.
    fin_df = get_financials(stock, path_to_csv=path_to_csv)

    # Construct results table.
    df = _return_table()

    try:
        df.at[0, "operatingIncome"] = int(fin_df.loc["operatingIncome"].iat[0])
    except:
        df.at[0, "operatingIncome"] = None
    try:
        df.at[0, "depreciation"] = int(fin_df.loc["depreciationAndAmortization"].iat[0])
    except:
        df.at[0, "depreciation"] = None
    try:
        df.at[0, "capex"] = int(fin_df.loc["capitalExpenditure"].iat[0])
    except:
        df.at[0, "capex"] = None

    # Calculate the average growth rate.
    df.at[0, "Average Growth Rate"] = calc_avg_growth_rate(
        list(fin_df.loc["freeCashFlow"].iloc[:terms].astype(float))
    )

    # Adjust the compound rate
    if df.at[0, "Average Growth Rate"] >= 0.1:
        compound_rate = 0.1
    elif df.at[0, "Average Growth Rate"] < 0:
        compound_rate = 0.025
    else:
        compound_rate = df.at[0, "Average Growth Rate"]

    # Calculating Owners Earnings / Free Cash Flow (FCF)
    if free_cash_flow:
        try:
            df.at[0, "Owners Earnings"] = int(fin_df.loc["freeCashFlow"].iat[0])
        except:
            df.at[0, "Owners Earnings"] = None
    else:
        earnings = df["operatingIncome"] + df["depreciation"] - df["capex"]
        df.at[0, "Owners Earnings"] = earnings.iloc[0]

    # Find the DCF (Discounted Cash Flow) Multiplier
    dfc = [compound(compound_rate, y) for y in range(1, terms + 1)]
    dfd = [discount(discount_rate, y) for y in range(1, terms + 1)]
    amounts = list(map(lambda x, y: x * y, dfc, dfd))

    df["Intrinsic Value"] = float(
        df["Owners Earnings"] * sum(amounts)
        + df["Owners Earnings"] * amounts[-1] * terminal_value
    )

    # Find Outstanding Shares
    try:
        df.at[0, "Outstanding Shares"] = int(
            fin_df.loc["weightedAverageShsOutDil"].iat[0]
        )
    except:
        df.at[0, "Outstanding Shares"] = None

    try:
        df.at[0, "Outstanding Shares"] = int(
            fin_df.loc["weightedAverageShsOutDil"].iat[1]
        )
    except:
        df.at[0, "Outstanding Shares"] = None

    # Value per share.
    df["Per Share"] = df["Intrinsic Value"] / df["Outstanding Shares"]

    return df


def intrinsic_value(
    stock: str,
    compound_rate: float = 0.1,
    discount_rate: float = 0.05,
    terms: int = 5,
    scrape: bool = False,
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
    :param scrape: Boolean to define whether the data should be scraped from
        webpage or read from .csv file.
    :returns: pd.DataFrame holding all the relevant information regarding the
        intrinsic value of a specific stock.
    """
    # Read from .csv or scrape and return data frame.
    fin_df = get_financials(stock, scrape)

    # Construct results table.
    df = _return_table()

    try:
        df.at[0, "incomeBeforeTax"] = fin_df.loc["incomeBeforeTax"].iat[0]
    except:
        df.at[0, "incomeBeforeTax"] = None
    try:
        df.at[0, "depreciation"] = fin_df.loc["depreciation"].iat[0]
    except:
        df.at[0, "depreciation"] = None
    try:
        df.at[0, "capitalExpenditures"] = fin_df.loc["capitalExpenditures"].iat[0]
    except:
        df.at[0, "capitalExpenditures"] = None

    # Calculating Average Capital Expenditure.
    try:
        df.at[0, "Average Capex"] = fin_df.loc["capitalExpenditures"].mean()
    except:
        df.at[0, "Average Capex"] = None

    # Calculating Owners Earnings: Free Cash Flow (FCF)
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
    try:
        df.at[0, "Outstanding Shares"] = fin_df.loc["annualDilutedAverageShares"].iat[0]
    except:
        df.at[0, "Outstanding Shares"] = None

    try:
        df.at[0, "Outstanding Shares"] = fin_df.loc["annualDilutedAverageShares"].iat[1]
    except:
        df.at[0, "Outstanding Shares"] = None

    # Value per share.
    df["Per Share"] = df["Intrinsic Value"] / df["Outstanding Shares"]

    return df
