"""From Pandas to SQL Database"""
import os

import pandas as pd
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from jesper.sql.db_tables import base, Stock
from jesper.sql.env import DBEnv


class JesperSQL():
    tables: list = [
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

    def __init__(self, env: DBEnv) -> None:
        # Keep all the DB connection in one place.
        self.env = env
        # Construct an Engine object, the starting point for any SQLAlchemy application.
        #
        # The engine will request a connection from the underlying Pool 
        # once Engine.connect() is called, 
        # or a method which depends on it such as Engine.execute() is invoked.
        self.engine = create_engine(self.env.get_uri_sqlalchemy(), echo=True)
        # Establish a Session. The Session establishes all conversations with the database 
        # and represents a “holding zone” for all the objects which you’ve loaded 
        # or associated with it during its lifespan.
        self.session = Session(self.engine)
        # Construct all metadata defined in the tables sections.
        # MetaData is a container object that keeps together many different features of a database
        # (or multiple databases) being described.
        base.metadata.create_all(self.engine)

    def _single_data_pd_to_sql(self, df: pd.DataFrame) -> None:
        """Reads a single pandas DataFrame containing fundamental data of a
        particular stock. It then iterates over the data and writes the every row to the
        corret table in the sql schema & adds the symbol as primary key.
        
        :param df: pd.DataFrame containing the data.
        """
        for t in self.tables:
            sqldf = df.loc[[t]]
            sqldf = sqldf.rename({t: str(df.loc["symbol"].iat[0])})

            sqldf.to_sql(
                t,
                self.engine,
                if_exists='append',
                index=True,
                chunksize=500,
            )
            # Adds stock ticker as primary key.
            self.engine.execute(f'ALTER TABLE {t} ADD PRIMARY KEY (index);')

    def write(self, df: pd.DataFrame) -> None:
        """Writes a specific stock to DB."""
        try:
            ticker = str(df.loc["symbol"].iat[0])
            reported_currency = str(df.loc["reportedCurrency"].iat[0])
            cik = str(df.loc["cik"].iat[0])
        except ValueError as err:
            raise ValueError(f"Parameter for stock not found. {err}.")
        
        # Instantiate the stocks table.
        stock = Stock(ticker=ticker, cik=cik, reported_currency=reported_currency)
        # Writes it to db.
        self.session.add(stock)
        self.session.commit()



# def pd_to_sql(df: pd.DataFrame) -> None:
#     symbol = df.loc["symbol"].iat[0]
#     rdf = df.loc[["revenue"]]
#     rdf = rdf.rename({"revenue": str(symbol)})

#     df.to_sql(
#         'revenue',
#         engine,
#         if_exists='append',
#         # if_exists='append',
#         index=True,
#         chunksize=500,
#         # dtype={
#         #     "job_id": Integer,
#         #     "agency": Text,
#         #     "business_title": Text,
#         #     "job_category":  Text,
#         #     "salary_range_from": Integer,
#         #     "salary_range_to": Integer,
#         #     "salary_frequency": String(50),
#         #     "work_location": Text,
#         #     "division/work_unit": Text,
#         #     "job_description": Text,
#         #     "posting_date": DateTime,
#         #     "posting_updated": DateTime
#         # }
#         # dtype={
#         #     'index': 'PRIMARY KEY',
#         # }
#     )

#     engine.execute('ALTER TABLE revenue ADD PRIMARY KEY (index);')


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
