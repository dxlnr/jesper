"""Yahoo Finance Scraping functions"""
import json
import multiprocessing
import re
from itertools import repeat
from typing import Dict, List

import backoff
import pandas as pd

from jesper.scraper import get_event_page, get_request_url

# Keys to summary data based on sublink keys.
FIN_KEYS = {
    "balance-sheet": ["balanceSheetHistory", "balanceSheetStatements"],
    "financials": ["incomeStatementHistory", "incomeStatementHistory"],
    "cash-flow": ["cashflowStatementHistory", "cashflowStatements"],
}


def _create_empty_timeseries_dict() -> dict:
    """
    Returns an empty TimeSeries dictionary.
    {
    'dataId': int,
    'asOfDate': str,
    'periodType': str,
    'currencyCode': str,
    'reportedValue': int
    }
    """
    return dict.fromkeys(
        ["dataId", "asOfDate", "periodType", "currencyCode", "reportedValue"]
    )


# def _parse_page_content_as_json(
#     url: str,
#     headers: dict[str, str] = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
#      (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
#     },
# ):
#     json_str = get_request_url(url)
#     try:
#         summary_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
#             "QuoteSummaryStore"
#         ]
#         timeseries_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
#             "QuoteTimeSeriesStore"
#         ]
#     except:
#         return "{}"
#     else:
#         # return summary data.
#         new_summary_data = json.dumps(summary_data).replace("{}", "null")
#         new_summary_data = re.sub(
#             r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_summary_data
#         )
#         json_summary_data = json.loads(new_summary_data)
#
#         # return timeseries data.
#         new_time_data = json.dumps(timeseries_data).replace("{}", "null")
#         new_time_data = re.sub(
#             r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_time_data
#         )
#         json_time_data = json.loads(new_time_data)
#
#         return json_summary_data, json_time_data


@backoff.on_predicate(backoff.fibo, lambda x: x == "{}", max_value=13)
def _parse_page_summary_as_json(json_str: str):
    """Parsing the page summary from single str."""
    try:
        summary_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
            "QuoteSummaryStore"
        ]
    except:
        return "{}"
    else:
        # return summary data after cleaning.
        new_summary_data = json.dumps(summary_data).replace("{}", "null")
        new_summary_data = re.sub(
            r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_summary_data
        )
        return json.loads(new_summary_data)


@backoff.on_predicate(backoff.fibo, lambda x: x == "{}", max_value=13)
def _parse_page_timeseries_as_json(json_str: str):
    """Parsing the page summary from single str."""
    try:
        timeseries_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
            "QuoteTimeSeriesStore"
        ]
    except:
        return "{}"
    else:
        # return timeseries data after cleaning.
        new_time_data = json.dumps(timeseries_data).replace("{}", "null")
        new_time_data = re.sub(
            r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_time_data
        )
        return json.loads(new_time_data)


def _convert_summary_to_pd(table: List[Dict]):
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


def _convert_timeseries_to_pd(
    table: List[Dict],
    name: str = "",
    value: str = "reportedValue",
    starting_year: str = "2019",
):
    """."""
    # Make sure table has lenght of 4.
    table = table + [None] * (4 - len(table))
    # Fill up table with empty dicts.
    table = [_create_empty_timeseries_dict() if t is None else t for t in table]
    df = pd.DataFrame(table)

    try:
        # Make sure every date is set and not NaN.
        df["asOfDate"] = pd.date_range(start=df["asOfDate"].iat[0], periods=4, freq="Y")
    except:
        df["asOfDate"] = pd.date_range(start=starting_year, periods=4, freq="Y")
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


def get_financial_info(ticker: str, workers: int = 3) -> pd.DataFrame:
    """Scrape the balance sheet, financial statement & cashflow of specific stock
    and return it as one dataframe.

    :param ticker: Determines the stock.
    :param workers: A number of worker processes to which jobs can be submitted.
    """
    with multiprocessing.Pool(processes=workers) as pool:
        dfs = pool.starmap(
            get_financial_statements, zip(repeat(ticker), list(FIN_KEYS.keys()))
        )
    # Combine to one asset.
    df = pd.concat(dfs)
    # Remove duplicated rows.
    df = df[~df.index.duplicated(keep="first")]
    return df


def get_financial_statements(ticker: str, sublink: str) -> pd.DataFrame:
    """Wrapper for getting the financial statements for specific stock.

    :param ticker: Determines the stock.
    :param sublink:
    """
    assert sublink in [
        "balance-sheet",
        "financials",
        "cash-flow",
    ], f"{sublink}: Leads to an unkown page error on yahoo-finance."
    # Construct url.
    url = f"https://finance.yahoo.com/quote/{ticker}/{sublink}?p={ticker}"
    # Fetch all the information.
    json_str = get_request_url(url)
    # Filter the summary information.
    summary_data = _parse_page_summary_as_json(json_str)
    # Extract the relevant information & convert to pandas DataFrame.
    try:
        summary = summary_data[FIN_KEYS[sublink][0]][FIN_KEYS[sublink][1]]
    except:
        summary = []
    return _convert_summary_to_pd(summary)


def get_timeseries_financial_statements(ticker: str, sublink: str) -> pd.DataFrame:
    assert sublink in [
        "balance-sheet",
        "financials",
        "cash-flow",
    ], f"{sublink}: Leads to an unkown page error on yahoo-finance."
    # Construct url.
    url = f"https://finance.yahoo.com/quote/{ticker}/{sublink}?p={ticker}"
    # Fetch all the information.
    json_str = get_request_url(url)
    # Filter the summary information.
    timeseries_data = _parse_page_timeseries_as_json(json_str)
    try:
        #  timeseries_data["timeSeries"].keys()
        #
        # 'trailingNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'trailingReconciledDepreciation',
        # 'annualNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'annualNetIncomeContinuousOperations',
        # 'annualOperatingExpense',
        # 'trailingSellingGeneralAndAdministration',
        # 'annualNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'trailingOtherNonOperatingIncomeExpenses',
        # 'annualDilutedEPS',
        # 'trailingOperatingExpense',
        # 'annualOtherSpecialCharges',
        # 'trailingOperatingRevenue',
        # 'trailingNetIncomeContinuousOperations',
        # 'annualTotalOperatingIncomeAsReported',
        # 'annualBasicAverageShares',
        # 'trailingNormalizedEBITDA',
        # 'annualRestructuringAndMergernAcquisition',
        # 'annualTaxEffectOfUnusualItems',
        # 'annualDepreciationAndAmortizationInIncomeStatement',
        # 'annualGeneralAndAdministrativeExpense',
        # 'annualTaxProvision',
        # 'annualInterestExpense',
        # 'annualAmortization',
        # 'trailingCostOfRevenue',
        # 'trailingDilutedNIAvailtoComStockholders',
        # 'trailingInterestIncome',
        # 'trailingNetIncomeIncludingNoncontrollingInterests',
        # 'annualBasicEPS',
        # 'trailingTotalUnusualItems',
        # 'annualWriteOff',
        # 'annualTotalRevenue',
        # 'annualTaxRateForCalcs',
        # 'annualInterestIncome',
        # 'annualNetIncomeCommonStockholders',
        # 'trailingEBIT',
        # 'annualOperatingRevenue',
        # 'annualResearchAndDevelopment',
        # 'annualDepreciationAmortizationDepletionIncomeStatement',
        # 'annualOtherOperatingExpenses',
        # 'annualGrossProfit',
        # 'annualOtherNonOperatingIncomeExpenses',
        # 'trailingTotalOperatingIncomeAsReported',
        # 'annualNetIncomeIncludingNoncontrollingInterests',
        # 'trailingSellingAndMarketingExpense',
        # 'annualNormalizedEBITDA',
        # 'annualSpecialIncomeCharges',
        # 'trailingTaxEffectOfUnusualItems',
        # 'annualReconciledDepreciation',
        # 'trailingEBITDA',
        # 'trailingGainOnSaleOfSecurity',
        # 'annualNormalizedIncome',
        # 'trailingNetInterestIncome',
        # 'trailingNetNonOperatingInterestIncomeExpense',
        # 'trailingTotalExpenses',
        # 'annualAmortizationOfIntangiblesIncomeStatement',
        # 'trailingNormalizedIncome',
        # 'annualNetInterestIncome',
        # 'annualNetNonOperatingInterestIncomeExpense',
        # 'annualOtherIncomeExpense',
        # 'trailingOtherOperatingExpenses',
        # 'trailingGrossProfit',
        # 'annualOperatingIncome',
        # 'trailingNetIncomeCommonStockholders',
        # 'trailingTaxRateForCalcs',
        # 'annualEBIT',
        # 'annualReconciledCostOfRevenue',
        # 'trailingNetIncome',
        # 'annualGainOnSaleOfSecurity',
        # 'annualSalariesAndWages',
        # 'trailingInterestIncomeNonOperating',
        # 'trailingPretaxIncome',
        # 'trailingOtherGandA',
        # 'annualSellingAndMarketingExpense',
        # 'trailingInterestExpense',
        # 'annualDilutedNIAvailtoComStockholders',
        # 'annualEarningsFromEquityInterestNetOfTax',
        # 'annualNetIncome',
        # 'annualPretaxIncome',
        # 'annualTotalUnusualItems',
        # 'annualNetIncomeExtraordinary',
        # 'annualTotalUnusualItemsExcludingGoodwill',
        # 'trailingTotalRevenue',
        # 'trailingInterestExpenseNonOperating',
        # 'annualEarningsFromEquityInterest',
        # 'annualInterestExpenseNonOperating',
        # 'annualCostOfRevenue',
        # 'annualOtherunderPreferredStockDividend',
        # 'trailingTotalUnusualItemsExcludingGoodwill',
        # 'trailingOtherIncomeExpense',
        # 'annualTotalExpenses',
        # 'trailingOperatingIncome',
        # 'annualImpairmentOfCapitalAssets',
        # 'trailingNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'annualSellingGeneralAndAdministration',
        # 'trailingGeneralAndAdministrativeExpense',
        # 'annualOtherGandA',
        # 'trailingTaxProvision',
        # 'trailingEarningsFromEquityInterestNetOfTax',
        # 'trailingReconciledCostOfRevenue',
        # 'annualInterestIncomeNonOperating',
        # 'annualDilutedAverageShares',
        # 'annualBasicDiscontinuousOperations',
        # 'annualDilutedDiscontinuousOperations',
        # 'trailingBasicEPSOtherGainsLosses',
        # 'annualProvisionForDoubtfulAccounts',
        # 'annualMinorityInterests',
        # 'trailingDilutedEPSOtherGainsLosses',
        # 'annualDepletionIncomeStatement',
        # 'annualDividendPerShare',
        # 'trailingOtherSpecialCharges',
        # 'annualBasicExtraordinary',
        # 'trailingNormalizedDilutedEPS',
        # 'annualReportedNormalizedBasicEPS',
        # 'trailingTaxLossCarryforwardBasicEPS',
        # 'trailingBasicExtraordinary',
        # 'trailingSpecialIncomeCharges',
        # 'annualDilutedExtraordinary',
        # 'trailingSecuritiesAmortization',
        # 'trailingBasicEPS',
        # 'trailingProvisionForDoubtfulAccounts',
        # 'trailingDilutedAverageShares',
        # 'trailingSalariesAndWages',
        # 'trailingDilutedContinuousOperations',
        # 'trailingGainOnSaleOfBusiness',
        # 'annualBasicAccountingChange',
        # 'trailingEarningsFromEquityInterest',
        # 'annualDilutedAccountingChange',
        # 'trailingAverageDilutionEarnings',
        # 'annualBasicContinuousOperations',
        # 'annualTaxLossCarryforwardBasicEPS',
        # 'annualContinuingAndDiscontinuedBasicEPS',
        # 'trailingDilutedAccountingChange',
        # 'trailingBasicAverageShares',
        # 'trailingDilutedExtraordinary',
        # 'annualDepreciationIncomeStatement',
        # 'trailingContinuingAndDiscontinuedDilutedEPS',
        # 'trailingBasicDiscontinuousOperations',
        # 'trailingDilutedDiscontinuousOperations',
        # 'trailingPreferredStockDividends',
        # 'annualOtherTaxes',
        # 'annualRentExpenseSupplemental',
        # 'trailingNetIncomeFromTaxLossCarryforward',
        # 'trailingTotalOtherFinanceCost',
        # 'trailingAmortization',
        # 'trailingAmortizationOfIntangiblesIncomeStatement',
        # 'trailingInsuranceAndClaims',
        # 'annualExciseTaxes',
        # 'trailingImpairmentOfCapitalAssets',
        # 'trailingRentExpenseSupplemental',
        # 'trailingNetIncomeExtraordinary',
        # 'annualSecuritiesAmortization',
        # 'annualTaxLossCarryforwardDilutedEPS',
        # 'annualNormalizedDilutedEPS',
        # 'trailingGainOnSaleOfPPE',
        # 'annualReportedNormalizedDilutedEPS',
        # 'trailingReportedNormalizedBasicEPS',
        # 'trailingMinorityInterests',
        # 'trailingTaxLossCarryforwardDilutedEPS',
        # 'trailingWriteOff',
        # 'trailingDepreciationIncomeStatement',
        # 'annualPreferredStockDividends',
        # 'annualNormalizedBasicEPS',
        # 'trailingDepreciationAmortizationDepletionIncomeStatement',
        # 'annualInsuranceAndClaims',
        # 'trailingRentAndLandingFees',
        # 'trailingNetIncomeDiscontinuousOperations',
        # 'annualBasicEPSOtherGainsLosses',
        # 'annualRentAndLandingFees',
        # 'annualNetIncomeDiscontinuousOperations',
        # 'trailingBasicContinuousOperations',
        # 'annualTotalOtherFinanceCost',
        # 'annualContinuingAndDiscontinuedDilutedEPS',
        # 'trailingDepreciationAndAmortizationInIncomeStatement',
        # 'annualDilutedContinuousOperations',
        # 'trailingOtherunderPreferredStockDividend',
        # 'annualDilutedEPSOtherGainsLosses',
        # 'trailingBasicAccountingChange',
        # 'trailingContinuingAndDiscontinuedBasicEPS',
        # 'trailingNormalizedBasicEPS',
        # 'trailingReportedNormalizedDilutedEPS',
        # 'trailingDepletionIncomeStatement',
        # 'trailingDividendPerShare',
        # 'trailingExciseTaxes',
        # 'trailingRestructuringAndMergernAcquisition',
        # 'annualGainOnSaleOfPPE',
        # 'trailingResearchAndDevelopment',
        # 'annualGainOnSaleOfBusiness',
        # 'annualAverageDilutionEarnings',
        # 'trailingOtherTaxes',
        # 'trailingDilutedEPS',
        # 'annualNetIncomeFromTaxLossCarryforward',
        # 'timestamp'
        #
        timeseries = timeseries_data["timeSeries"]
        # Extract annual_shares
        annual_diluted_shares = timeseries["annualDilutedAverageShares"]
    except:
        annual_diluted_shares = [None, None, None, None]

    return _convert_timeseries_to_pd(annual_diluted_shares)


def get_balance_sheet(ticker: str, annual: bool = True):
    """Scrapes balance sheet from Yahoo Finance for an input ticker.

    :param ticker: Determines the stock.
    :param annual: Yahoo Finance offers stats annual & quarterly.
    :returns: pandas.df containing balance shee history.
    """
    bs_url = f"https://finance.yahoo.com/quote/{ticker}/balance-sheet?p={ticker}"
    summary_data, timeseries_data = _parse_page_content_as_json(bs_url)
    try:
        if annual:
            summary = summary_data["balanceSheetHistory"]["balanceSheetStatements"]
        else:
            summary = summary_data["balanceSheetHistoryQuarterly"][
                "balanceSheetStatements"
            ]
    except:
        summary = []

    return _convert_summary_to_pd(summary)


def get_income_statement(ticker: str, annual: bool = True):
    """Scrape income statement from Yahoo Finance for an input ticker.

    :param ticker: Determines the stock.
    :param annual: Yahoo Finance offers stats annual & quarterly.
    :returns: pandas.df containing income statement history.
    :returns: pandas.df containing historic annual diluted Shares.
    """
    in_url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"
    summary_data, timeseries_data = _parse_page_content_as_json(in_url)

    if annual:
        summary = summary_data["incomeStatementHistory"]["incomeStatementHistory"]

        #  timeseries_data["timeSeries"].keys()
        #
        # 'trailingNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'trailingReconciledDepreciation',
        # 'annualNetIncomeFromContinuingOperationNetMinorityInterest',
        # 'annualNetIncomeContinuousOperations',
        # 'annualOperatingExpense',
        # 'trailingSellingGeneralAndAdministration',
        # 'annualNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'trailingOtherNonOperatingIncomeExpenses',
        # 'annualDilutedEPS',
        # 'trailingOperatingExpense',
        # 'annualOtherSpecialCharges',
        # 'trailingOperatingRevenue',
        # 'trailingNetIncomeContinuousOperations',
        # 'annualTotalOperatingIncomeAsReported',
        # 'annualBasicAverageShares',
        # 'trailingNormalizedEBITDA',
        # 'annualRestructuringAndMergernAcquisition',
        # 'annualTaxEffectOfUnusualItems',
        # 'annualDepreciationAndAmortizationInIncomeStatement',
        # 'annualGeneralAndAdministrativeExpense',
        # 'annualTaxProvision',
        # 'annualInterestExpense',
        # 'annualAmortization',
        # 'trailingCostOfRevenue',
        # 'trailingDilutedNIAvailtoComStockholders',
        # 'trailingInterestIncome',
        # 'trailingNetIncomeIncludingNoncontrollingInterests',
        # 'annualBasicEPS',
        # 'trailingTotalUnusualItems',
        # 'annualWriteOff',
        # 'annualTotalRevenue',
        # 'annualTaxRateForCalcs',
        # 'annualInterestIncome',
        # 'annualNetIncomeCommonStockholders',
        # 'trailingEBIT',
        # 'annualOperatingRevenue',
        # 'annualResearchAndDevelopment',
        # 'annualDepreciationAmortizationDepletionIncomeStatement',
        # 'annualOtherOperatingExpenses',
        # 'annualGrossProfit',
        # 'annualOtherNonOperatingIncomeExpenses',
        # 'trailingTotalOperatingIncomeAsReported',
        # 'annualNetIncomeIncludingNoncontrollingInterests',
        # 'trailingSellingAndMarketingExpense',
        # 'annualNormalizedEBITDA',
        # 'annualSpecialIncomeCharges',
        # 'trailingTaxEffectOfUnusualItems',
        # 'annualReconciledDepreciation',
        # 'trailingEBITDA',
        # 'trailingGainOnSaleOfSecurity',
        # 'annualNormalizedIncome',
        # 'trailingNetInterestIncome',
        # 'trailingNetNonOperatingInterestIncomeExpense',
        # 'trailingTotalExpenses',
        # 'annualAmortizationOfIntangiblesIncomeStatement',
        # 'trailingNormalizedIncome',
        # 'annualNetInterestIncome',
        # 'annualNetNonOperatingInterestIncomeExpense',
        # 'annualOtherIncomeExpense',
        # 'trailingOtherOperatingExpenses',
        # 'trailingGrossProfit',
        # 'annualOperatingIncome',
        # 'trailingNetIncomeCommonStockholders',
        # 'trailingTaxRateForCalcs',
        # 'annualEBIT',
        # 'annualReconciledCostOfRevenue',
        # 'trailingNetIncome',
        # 'annualGainOnSaleOfSecurity',
        # 'annualSalariesAndWages',
        # 'trailingInterestIncomeNonOperating',
        # 'trailingPretaxIncome',
        # 'trailingOtherGandA',
        # 'annualSellingAndMarketingExpense',
        # 'trailingInterestExpense',
        # 'annualDilutedNIAvailtoComStockholders',
        # 'annualEarningsFromEquityInterestNetOfTax',
        # 'annualNetIncome',
        # 'annualPretaxIncome',
        # 'annualTotalUnusualItems',
        # 'annualNetIncomeExtraordinary',
        # 'annualTotalUnusualItemsExcludingGoodwill',
        # 'trailingTotalRevenue',
        # 'trailingInterestExpenseNonOperating',
        # 'annualEarningsFromEquityInterest',
        # 'annualInterestExpenseNonOperating',
        # 'annualCostOfRevenue',
        # 'annualOtherunderPreferredStockDividend',
        # 'trailingTotalUnusualItemsExcludingGoodwill',
        # 'trailingOtherIncomeExpense',
        # 'annualTotalExpenses',
        # 'trailingOperatingIncome',
        # 'annualImpairmentOfCapitalAssets',
        # 'trailingNetIncomeFromContinuingAndDiscontinuedOperation',
        # 'annualSellingGeneralAndAdministration',
        # 'trailingGeneralAndAdministrativeExpense',
        # 'annualOtherGandA',
        # 'trailingTaxProvision',
        # 'trailingEarningsFromEquityInterestNetOfTax',
        # 'trailingReconciledCostOfRevenue',
        # 'annualInterestIncomeNonOperating',
        # 'annualDilutedAverageShares',
        # 'annualBasicDiscontinuousOperations',
        # 'annualDilutedDiscontinuousOperations',
        # 'trailingBasicEPSOtherGainsLosses',
        # 'annualProvisionForDoubtfulAccounts',
        # 'annualMinorityInterests',
        # 'trailingDilutedEPSOtherGainsLosses',
        # 'annualDepletionIncomeStatement',
        # 'annualDividendPerShare',
        # 'trailingOtherSpecialCharges',
        # 'annualBasicExtraordinary',
        # 'trailingNormalizedDilutedEPS',
        # 'annualReportedNormalizedBasicEPS',
        # 'trailingTaxLossCarryforwardBasicEPS',
        # 'trailingBasicExtraordinary',
        # 'trailingSpecialIncomeCharges',
        # 'annualDilutedExtraordinary',
        # 'trailingSecuritiesAmortization',
        # 'trailingBasicEPS',
        # 'trailingProvisionForDoubtfulAccounts',
        # 'trailingDilutedAverageShares',
        # 'trailingSalariesAndWages',
        # 'trailingDilutedContinuousOperations',
        # 'trailingGainOnSaleOfBusiness',
        # 'annualBasicAccountingChange',
        # 'trailingEarningsFromEquityInterest',
        # 'annualDilutedAccountingChange',
        # 'trailingAverageDilutionEarnings',
        # 'annualBasicContinuousOperations',
        # 'annualTaxLossCarryforwardBasicEPS',
        # 'annualContinuingAndDiscontinuedBasicEPS',
        # 'trailingDilutedAccountingChange',
        # 'trailingBasicAverageShares',
        # 'trailingDilutedExtraordinary',
        # 'annualDepreciationIncomeStatement',
        # 'trailingContinuingAndDiscontinuedDilutedEPS',
        # 'trailingBasicDiscontinuousOperations',
        # 'trailingDilutedDiscontinuousOperations',
        # 'trailingPreferredStockDividends',
        # 'annualOtherTaxes',
        # 'annualRentExpenseSupplemental',
        # 'trailingNetIncomeFromTaxLossCarryforward',
        # 'trailingTotalOtherFinanceCost',
        # 'trailingAmortization',
        # 'trailingAmortizationOfIntangiblesIncomeStatement',
        # 'trailingInsuranceAndClaims',
        # 'annualExciseTaxes',
        # 'trailingImpairmentOfCapitalAssets',
        # 'trailingRentExpenseSupplemental',
        # 'trailingNetIncomeExtraordinary',
        # 'annualSecuritiesAmortization',
        # 'annualTaxLossCarryforwardDilutedEPS',
        # 'annualNormalizedDilutedEPS',
        # 'trailingGainOnSaleOfPPE',
        # 'annualReportedNormalizedDilutedEPS',
        # 'trailingReportedNormalizedBasicEPS',
        # 'trailingMinorityInterests',
        # 'trailingTaxLossCarryforwardDilutedEPS',
        # 'trailingWriteOff',
        # 'trailingDepreciationIncomeStatement',
        # 'annualPreferredStockDividends',
        # 'annualNormalizedBasicEPS',
        # 'trailingDepreciationAmortizationDepletionIncomeStatement',
        # 'annualInsuranceAndClaims',
        # 'trailingRentAndLandingFees',
        # 'trailingNetIncomeDiscontinuousOperations',
        # 'annualBasicEPSOtherGainsLosses',
        # 'annualRentAndLandingFees',
        # 'annualNetIncomeDiscontinuousOperations',
        # 'trailingBasicContinuousOperations',
        # 'annualTotalOtherFinanceCost',
        # 'annualContinuingAndDiscontinuedDilutedEPS',
        # 'trailingDepreciationAndAmortizationInIncomeStatement',
        # 'annualDilutedContinuousOperations',
        # 'trailingOtherunderPreferredStockDividend',
        # 'annualDilutedEPSOtherGainsLosses',
        # 'trailingBasicAccountingChange',
        # 'trailingContinuingAndDiscontinuedBasicEPS',
        # 'trailingNormalizedBasicEPS',
        # 'trailingReportedNormalizedDilutedEPS',
        # 'trailingDepletionIncomeStatement',
        # 'trailingDividendPerShare',
        # 'trailingExciseTaxes',
        # 'trailingRestructuringAndMergernAcquisition',
        # 'annualGainOnSaleOfPPE',
        # 'trailingResearchAndDevelopment',
        # 'annualGainOnSaleOfBusiness',
        # 'annualAverageDilutionEarnings',
        # 'trailingOtherTaxes',
        # 'trailingDilutedEPS',
        # 'annualNetIncomeFromTaxLossCarryforward',
        # 'timestamp'
        #
        timeseries = timeseries_data["timeSeries"]

        # Extract annual_shares
        try:
            annual_diluted_shares = timeseries["annualDilutedAverageShares"]
        except:
            annual_diluted_shares = None
    else:
        summary = summary_data["incomeStatementHistoryQuarterly"][
            "incomeStatementHistory"
        ]

    if annual_diluted_shares is None:
        df = _convert_summary_to_pd(summary)
    else:
        df = pd.concat(
            [
                _convert_summary_to_pd(summary),
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
    cf_url = f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}"
    summary_data, _ = _parse_page_content_as_json(cf_url)

    if annual:
        summary = summary_data["cashflowStatementHistory"]["cashflowStatements"]
    else:
        summary = summary_data["cashflowStatementHistoryQuarterly"][
            "cashflowStatements"
        ]

    return _convert_summary_to_pd(summary)


def scraper_to_latest_stock_price(url: str) -> float:
    """Scrape yahoo finance for latest stock price.

    :param url: API endpoint as str.
    """
    # Scrape raw data for parsing.
    page_content = get_event_page(url)
    # Get closing price.
    price = page_content.find(
        "fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}
    ).text
    # Make sure there is no problem with commata.
    price = price.replace(",", "")

    return float(price)
