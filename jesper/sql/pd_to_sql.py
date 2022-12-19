"""From Pandas to SQL Database"""
import os

import pandas as pd
import psycopg

TABLES_LIST = [
    "revenue",
    "costOfRevenue",
    "grossProfit",
    "grossProfitRatio",
    "researchAndDevelopmentExpenses",
    "generalAndAdministrativeExpenses",
    "sellingAndMarketingExpenses",
    "sellingGeneralAndAdministrativeExpenses",
    "otherExpenses",
    "operatingExpenses",
    "costAndExpenses",
    "interestIncome",
    "interestExpense",
    "depreciationAndAmortization",
    "ebitda",
    "ebitdaratio",
    "operatingIncome",
    "operatingIncomeRatio",
    "totalOtherIncomeExpensesNet",
    "incomeBeforeTax",
    "incomeBeforeTaxRatio",
    "incomeTaxExpense",
    "netIncome",
    "netIncomeRatio",
    "eps",
    "epsdiluted",
    "weightedAverageShsOut",
    "weightedAverageShsOutDil",
    "cashAndCashEquivalents",
    "shortTermInvestments",
    "cashAndShortTermInvestments",
    "netReceivables",
    "inventory",
    "otherCurrentAssets",
    "totalCurrentAssets",
    "propertyPlantEquipmentNet",
    "goodwill",
    "intangibleAssets",
    "goodwillAndIntangibleAssets",
    "longTermInvestments",
    "taxAssets",
    "otherNonCurrentAssets",
    "totalNonCurrentAssets",
    "otherAssets",
    "totalAssets",
    "accountPayables",
    "shortTermDebt",
    "taxPayables",
    "deferredRevenue",
    "otherCurrentLiabilities",
    "totalCurrentLiabilities",
    "longTermDebt",
    "deferredRevenueNonCurrent",
    "deferredTaxLiabilitiesNonCurrent",
    "otherNonCurrentLiabilities",
    "totalNonCurrentLiabilities",
    "otherLiabilities",
    "capitalLeaseObligations",
    "totalLiabilities",
    "preferredStock",
    "commonStock",
    "retainedEarnings",
    "accumulatedOtherComprehensiveIncomeLoss",
    "othertotalStockholdersEquity",
    "totalStockholdersEquity",
    "totalLiabilitiesAndStockholdersEquity",
    "minorityInterest",
    "totalEquity",
    "totalLiabilitiesAndTotalEquity",
    "totalInvestments",
    "totalDebt",
    "netDebt",
    "deferredIncomeTax",
    "stockBasedCompensation",
    "changeInWorkingCapital",
    "accountsReceivables",
    "accountsPayables",
    "otherWorkingCapital",
    "otherNonCashItems",
    "netCashProvidedByOperatingActivities",
    "investmentsInPropertyPlantAndEquipment",
    "acquisitionsNet",
    "purchasesOfInvestments",
    "salesMaturitiesOfInvestments",
    "otherInvestingActivites",
    "netCashUsedForInvestingActivites",
    "debtRepayment",
    "commonStockIssued",
    "commonStockRepurchased",
    "dividendsPaid",
    "otherFinancingActivites",
    "netCashUsedProvidedByFinancingActivities",
    "effectOfForexChangesOnCash",
    "netChangeInCash",
    "cashAtEndOfPeriod",
    "cashAtBeginningOfPeriod",
    "operatingCashFlow",
    "capitalExpenditure",
    "freeCashFlow",
]


def pd_to_sql(df: pd.DataFrame) -> None:
    symbol = df.loc["symbol"].iat[0]
    rdf = df.loc[["revenue"]]
    rdf = rdf.rename({"revenue": str(symbol)})

    df.to_sql(
        'revenue',
        engine,
        if_exists='append',
        # if_exists='append',
        index=True,
        chunksize=500,
        # dtype={
        #     "job_id": Integer,
        #     "agency": Text,
        #     "business_title": Text,
        #     "job_category":  Text,
        #     "salary_range_from": Integer,
        #     "salary_range_to": Integer,
        #     "salary_frequency": String(50),
        #     "work_location": Text,
        #     "division/work_unit": Text,
        #     "job_description": Text,
        #     "posting_date": DateTime,
        #     "posting_updated": DateTime
        # }
        # dtype={
        #     'index': 'PRIMARY KEY',
        # }
    )

    engine.execute('ALTER TABLE revenue ADD PRIMARY KEY (index);')


def clean_c_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Takes a pandas DataFrame & returns it with cleaned up headers."""
    df.columns = [
        x.lower()
        .replace(" ", "_")
        .replace("?", "")
        .replace("-", "_")
        .replace(r"/", "_")
        .replace("\\", "_")
        .replace("%", "")
        .replace(r")", "")
        .replace(r"(", "")
        .replace("$", "")
        for x in df.columns
    ]
    return df


def adjust_dtype(df: pd.DataFrame):
    replacements = {
        "object": "varchar",
        "float64": "float",
        "int64": "int",
        "datetime64": "timestamp",
        "timedelta64[ns]": "varchar",
    }
    col_str = ", ".join("{} {}")


def csv_to_postgresql(csv_path: str, env: dict):
    """."""
    assert not all(
        k in env.items()
        for k in ("PSQL_PORT", "PSQL_HOST", "PSQL_DB_NAME", "PSQL_USER", "PSQL_PW")
    ), "keys are missing in .env \['PSQL_PORT', 'PSQL_HOST', 'PSQL_DB_NAME', 'PSQL_USER', 'PSQL_PW'\]."

    for k, v in env.items():
        print(type(v))

    try:
        with psycopg.connect(
            dbname=env["PSQL_DB_NAME"],
            user=env["PSQL_USER"],
            password=env["PSQL_PW"],
            host=env["PSQL_HOST"],
            port=env["PSQL_PORT"],
        ) as conn:
            cursor = conn.cursor()

            cursor.execute("drop table if exists")
            print("success.")
    except (Exception, psycopg.DatabaseError) as err:
        raise err
