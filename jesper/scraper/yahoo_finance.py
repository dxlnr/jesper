import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

from jesper.scraper import get_event_page
from jesper.scraper.scraper import _parse_json


def scraper_to_statement(link: str) -> pd.DataFrame:
    r"""Scrape from link and convert to data frame.

    :param link: API endpoint as str.
    :returns: Pandas dataframe.
    """
    # Scrape raw data for parsing.
    page_content = get_event_page(link)

    # Params
    items = []
    temp_list = []
    final = []
    index = 0

    # Filter for specific items
    features = page_content.find_all("div", class_="D(tbr)")

    # Catch exception and return empty Dataframe.
    if len(features) == 0:
        return pd.DataFrame()

    # Create headers
    for item in features[0].find_all("div", class_="D(ib)"):
        items.append(item.text)

    # Statement contents
    while index <= len(features) - 1:
        # Filter for each line of the statement.
        temp = features[index].find_all("div", class_="D(tbc)")
        for line in temp:
            temp_list.append(line.text)

        final.append(temp_list)
        temp_list = []
        index += 1

    df = pd.DataFrame(final[1:])
    df.columns = items
    df = convert_to_float(df)

    return df


def scraper_to_latest_stock_price(link: str) -> float:
    """Scrape yahoo finance for latest stock price.

    :param link: API endpoint as str.
    """
    # Scrape raw data for parsing.
    page_content = get_event_page(link)
    # Get closing price.
    price = page_content.find(
        "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
    ).text

    return price


def _parse_table(json_info):
    """."""
    df = pd.DataFrame(json_info)
    # Make sure dataframe is actually fetched correctly.
    if df.empty:
        return df
    # Delete "maxAge"
    if "maxAge" in df:
        del df["maxAge"]

    # Use date as index & convert it to pandas datetime.
    df.set_index("endDate", inplace=True)
    df.index = pd.to_datetime(df.index, unit="s")
    # Use only the year.
    df.index = df.index.year

    return df.transpose()


def _parse_timeseries_table(json_info, name: str = "", value: str = "reportedValue"):
    """."""
    df = pd.DataFrame(json_info)
    # Make sure dataframe is actually fetched correctly.
    if df.empty:
        return df

    # Use date as index & convert it to pandas datetime.
    if "asOfDate" in df:
        df.set_index("asOfDate", inplace=True)
        df.index = pd.to_datetime(df.index)
        # Use only the year.
        df.index = df.index.year

    # Keep only the reported value.
    df = df[[value]]
    df = df.sort_index(ascending=False)
    df.index.names = ["endDate"]

    df = df.transpose()
    # Rename the value to name for index name.
    df = df.rename(index={value: name})
    return df


def get_balance_sheet(ticker: str, annual: bool = True):
    """Scrapes balance sheet from Yahoo Finance for an input ticker.

    :param ticker: Determines the stock.
    :param annual: Yahoo Finance offers stats annual & quarterly.
    :returns: pandas.df containing balance shee history.
    """
    bs_link = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    # json_info = _parse_json(bs_link)
    summary_data, timeseries_data = _parse_json(bs_link)
    try:
        if annual:
            summary = summary_data["balanceSheetHistory"]["balanceSheetStatements"]
        else:
            summary = summary_data["balanceSheetHistoryQuarterly"][
                "balanceSheetStatements"
            ]
    except:
        summary = []

    return _parse_table(summary)


def get_income_statement(ticker: str, annual: bool = True):
    """Scrape income statement from Yahoo Finance for an input ticker.

    :param ticker: Determines the stock.
    :param annual: Yahoo Finance offers stats annual & quarterly.
    :returns: pandas.df containing income statement history.
    :returns: pandas.df containing historic annual diluted Shares.
    """
    in_link = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    summary_data, timeseries_data = _parse_json(in_link)

    if annual:
        summary = summary_data["incomeStatementHistory"]["incomeStatementHistory"]

        #  timeseries_data["timeSeries"].keys()
        #
        # ['trailingNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'trailingReconciledDepreciation',
        # 'annualNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'annualNetIncomeContinuousOperations', 'annualOperatingExpense',
        # 'trailingSellingGeneralAndAdministration',
        # 'annualNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'trailingOtherNonOperatingIncomeExpenses', 'annualDilutedEPS',
        # 'trailingOperatingExpense', 'annualOtherSpecialCharges', 'trailingOperatingRevenue',
        # 'trailingNetIncomeContinuousOperations', 'annualTotalOperatingIncomeAsReported',
        # 'annualBasicAverageShares', 'trailingNormalizedEBITDA',
        # 'annualRestructuringAndMergernAcquisition', 'annualTaxEffectOfUnusualItems',
        # 'annualDepreciationAndAmortizationInIncomeStatement', 'annualGeneralAndAdministrativeExpense',
        # 'annualTaxProvision', 'annualInterestExpense', 'annualAmortization',
        # 'trailingCostOfRevenue', 'trailingDilutedNIAvailtoComStockholders', 'trailingInterestIncome',
        # 'trailingNetIncomeIncludingNoncontrollingInterests', 'annualBasicEPS',
        # 'trailingTotalUnusualItems', 'annualWriteOff', 'annualTotalRevenue', 'annualTaxRateForCalcs',
        # 'annualInterestIncome', 'annualNetIncomeCommonStockholders', 'trailingEBIT',
        # 'annualOperatingRevenue', 'annualResearchAndDevelopment',
        # 'annualDepreciationAmortizationDepletionIncomeStatement',
        # 'annualOtherOperatingExpenses', 'annualGrossProfit',
        # 'annualOtherNonOperatingIncomeExpenses', 'trailingTotalOperatingIncomeAsReported',
        # 'annualNetIncomeIncludingNoncontrollingInterests', 'trailingSellingAndMarketingExpense',
        # 'annualNormalizedEBITDA', 'annualSpecialIncomeCharges', 'trailingTaxEffectOfUnusualItems',
        # 'annualReconciledDepreciation', 'trailingEBITDA', 'trailingGainOnSaleOfSecurity',
        # 'annualNormalizedIncome', 'trailingNetInterestIncome', 'trailingNetNonOperatingInterestIncomeExpense',
        # 'trailingTotalExpenses', 'annualAmortizationOfIntangiblesIncomeStatement',
        # 'trailingNormalizedIncome', 'annualNetInterestIncome',
        # 'annualNetNonOperatingInterestIncomeExpense', 'annualOtherIncomeExpense',
        # 'trailingOtherOperatingExpenses', 'trailingGrossProfit', 'annualOperatingIncome',
        # 'trailingNetIncomeCommonStockholders', 'trailingTaxRateForCalcs', 'annualEBIT',
        # 'annualReconciledCostOfRevenue', 'trailingNetIncome',
        # 'annualGainOnSaleOfSecurity', 'annualSalariesAndWages', 'trailingInterestIncomeNonOperating',
        # 'trailingPretaxIncome', 'trailingOtherGandA', 'annualSellingAndMarketingExpense',
        # 'trailingInterestExpense', 'annualDilutedNIAvailtoComStockholders',
        # 'annualEarningsFromEquityInterestNetOfTax', 'annualNetIncome', 'annualPretaxIncome',
        # 'annualTotalUnusualItems', 'annualNetIncomeExtraordinary',
        # 'annualTotalUnusualItemsExcludingGoodwill', 'trailingTotalRevenue', 'trailingInterestExpenseNonOperating',
        # 'annualEarningsFromEquityInterest', 'annualInterestExpenseNonOperating',
        # 'annualCostOfRevenue', 'annualOtherunderPreferredStockDividend',
        # 'trailingTotalUnusualItemsExcludingGoodwill', 'trailingOtherIncomeExpense',
        # 'annualTotalExpenses', 'trailingOperatingIncome', 'annualImpairmentOfCapitalAssets',
        # 'trailingNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'annualSellingGeneralAndAdministration', 'trailingGeneralAndAdministrativeExpense',
        # 'annualOtherGandA', 'trailingTaxProvision', 'trailingEarningsFromEquityInterestNetOfTax',
        # 'trailingReconciledCostOfRevenue', 'annualInterestIncomeNonOperating',
        # 'annualDilutedAverageShares', 'annualBasicDiscontinuousOperations',
        # 'annualDilutedDiscontinuousOperations', 'trailingBasicEPSOtherGainsLosses',
        # 'annualProvisionForDoubtfulAccounts', 'annualMinorityInterests', 'trailingDilutedEPSOtherGainsLosses',
        # 'annualDepletionIncomeStatement', 'annualDividendPerShare', 'trailingOtherSpecialCharges',
        # 'annualBasicExtraordinary', 'trailingNormalizedDilutedEPS', 'annualReportedNormalizedBasicEPS',
        # 'trailingTaxLossCarryforwardBasicEPS', 'trailingBasicExtraordinary', 'trailingSpecialIncomeCharges',
        # 'annualDilutedExtraordinary', 'trailingSecuritiesAmortization', 'trailingBasicEPS',
        # 'trailingProvisionForDoubtfulAccounts', 'trailingDilutedAverageShares',
        # 'trailingSalariesAndWages', 'trailingDilutedContinuousOperations', 'trailingGainOnSaleOfBusiness',
        # 'annualBasicAccountingChange', 'trailingEarningsFromEquityInterest', 'annualDilutedAccountingChange',
        # 'trailingAverageDilutionEarnings', 'annualBasicContinuousOperations', 'annualTaxLossCarryforwardBasicEPS',
        # 'annualContinuingAndDiscontinuedBasicEPS', 'trailingDilutedAccountingChange',
        # 'trailingBasicAverageShares', 'trailingDilutedExtraordinary',
        # 'annualDepreciationIncomeStatement', 'trailingContinuingAndDiscontinuedDilutedEPS',
        # 'trailingBasicDiscontinuousOperations', 'trailingDilutedDiscontinuousOperations',
        # 'trailingPreferredStockDividends', 'annualOtherTaxes', 'annualRentExpenseSupplemental',
        # 'trailingNetIncomeFromTaxLossCarryforward', 'trailingTotalOtherFinanceCost',
        # 'trailingAmortization', 'trailingAmortizationOfIntangiblesIncomeStatement',
        # 'trailingInsuranceAndClaims', 'annualExciseTaxes', 'trailingImpairmentOfCapitalAssets',
        # 'trailingRentExpenseSupplemental', 'trailingNetIncomeExtraordinary', 'annualSecuritiesAmortization',
        # 'annualTaxLossCarryforwardDilutedEPS', 'annualNormalizedDilutedEPS', 'trailingGainOnSaleOfPPE',
        # 'annualReportedNormalizedDilutedEPS', 'trailingReportedNormalizedBasicEPS',
        # 'trailingMinorityInterests', 'trailingTaxLossCarryforwardDilutedEPS', 'trailingWriteOff',
        # 'trailingDepreciationIncomeStatement', 'annualPreferredStockDividends', 'annualNormalizedBasicEPS',
        # 'trailingDepreciationAmortizationDepletionIncomeStatement', 'annualInsuranceAndClaims',
        # 'trailingRentAndLandingFees', 'trailingNetIncomeDiscontinuousOperations',
        # 'annualBasicEPSOtherGainsLosses', 'annualRentAndLandingFees',
        # 'annualNetIncomeDiscontinuousOperations', 'trailingBasicContinuousOperations',
        # 'annualTotalOtherFinanceCost', 'annualContinuingAndDiscontinuedDilutedEPS',
        # 'trailingDepreciationAndAmortizationInIncomeStatement', 'annualDilutedContinuousOperations',
        # 'trailingOtherunderPreferredStockDividend', 'annualDilutedEPSOtherGainsLosses',
        # 'trailingBasicAccountingChange', 'trailingContinuingAndDiscontinuedBasicEPS',
        # 'trailingNormalizedBasicEPS', 'trailingReportedNormalizedDilutedEPS',
        # 'trailingDepletionIncomeStatement', 'trailingDividendPerShare', 'trailingExciseTaxes',
        # 'trailingRestructuringAndMergernAcquisition', 'annualGainOnSaleOfPPE', 'trailingResearchAndDevelopment',
        # 'annualGainOnSaleOfBusiness', 'annualAverageDilutionEarnings', 'trailingOtherTaxes',
        # 'trailingDilutedEPS', 'annualNetIncomeFromTaxLossCarryforward', 'timestamp']
        #
        timeseries = timeseries_data["timeSeries"]

        # Extract annual_shares
        annual_diluted_shares = timeseries["annualDilutedAverageShares"]
    else:
        summary = summary_data["incomeStatementHistoryQuarterly"][
            "incomeStatementHistory"
        ]

    df = pd.concat(
        [
            _parse_table(summary),
            _parse_timeseries_table(
                annual_diluted_shares, name="annualDilutedAverageShares"
            ),
        ]
    )
    return df


def get_cash_flow(ticker: str, annual: bool = True):
    """Scrapes the cash flow statement from Yahoo Finance for an input ticker.

    :param ticker: Determines the stock.
    :param annual: Yahoo Finance offers stats annual & quarterly.
    :returns: pandas.df containing cashflow statement history.
    """
    cf_link = f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}"
    summary_data, _ = _parse_json(cf_link)

    if annual:
        summary = summary_data["cashflowStatementHistory"]["cashflowStatements"]
    else:
        summary = summary_data["cashflowStatementHistoryQuarterly"][
            "cashflowStatements"
        ]

    return _parse_table(summary)


def get_stats(ticker, headers={"User-agent": "Mozilla/5.0"}):
    """
    :param ticker:
    :param annual: Yahoo Finance offers stats annual & quarterly.
    """
    stats_site = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"

    tables = pd.read_html(requests.get(stats_site, headers=headers).text)
    tables = [table for table in tables[1:] if table.shape[1] == 2]

    table = tables[0]
    for elt in tables[1:]:
        table = table.append(elt)

    table.columns = ["Attribute", "Value"]
    table = table.reset_index(drop=True)

    return table


def extract_latest_value(df: pd.DataFrame, v_name: str) -> float:
    """Extract value latest value from sheet."""
    for k in df.keys():
        if isinstance(num := extract_k_value(df, k, v_name), float):
            return num

    raise Exception(f"No '{v_name}' value found.")


def extract_k_value(df: pd.DataFrame, v_key: str, v_name: str) -> float:
    """Extract value from specific key."""
    return df[v_key].loc[df["Breakdown"] == v_name].values[0]


def extract_ttm_value(df: pd.DataFrame, v_name: str) -> float:
    """Extract value from Trailing 12 months (TTM)."""
    return df["ttm"].loc[df["Breakdown"] == v_name].values[0]


def has_digits(in_str: str) -> bool:
    """Returns Bool if str contains digits."""
    return any(char.isdigit() for char in in_str)


def convert_to_float(df: pd.DataFrame):
    """Takes scraped dataframe and converts the str numbers to floats."""
    for idx, key in enumerate(df.columns):
        if idx == 0:
            continue

        df[key] = [
            float(str(i).replace(",", "")) if has_digits(i) else i for i in df[key]
        ]
    return df
