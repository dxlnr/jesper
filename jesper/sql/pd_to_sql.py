"""From Pandas to SQL Database"""
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from jesper.sql.db_tables import Stock, base
from jesper.sql.env import DBEnv


class JesperSQL:
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

    def _table_exists(self, table_str: str) -> bool:
        """Checks if specific table exists."""
        return sqlalchemy.inspect(self.engine).has_table(table_str)

    def _clean_c_headers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Takes a pandas DataFrame & returns it with cleaned up headers."""
        df.columns = [self._clean_str(x) for x in df.columns]
        return df

    def _clean_str(self, x: str) -> str:
        """Cleans a str for riskfree SQL usage."""
        return (
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
        )

    def _single_data_pd_to_sql(self, df: pd.DataFrame) -> None:
        """Reads a single pandas DataFrame containing fundamental data of a
        particular stock. It then iterates over the data and writes the every row to the
        corret table in the sql schema & adds the symbol as primary key.
        
        :param df: pd.DataFrame containing the data.
        """
        for t in self.tables:
            sqldf = df.loc[[t]]
            sqldf = sqldf.rename({t: str(df.loc["symbol"].iat[0])})
            sqldf.insert(0, 'param', str(t))

            # SQL clean up str.
            t = self._clean_str(t)
            if not self._table_exists(t):

                sqldf.to_sql(
                    t, self.engine, if_exists="append", index=True, chunksize=500,
                )
                # Adds stock ticker as primary key for data table.
                self.engine.execute(f"ALTER TABLE {t} ADD PRIMARY KEY (index);")
                self.engine.execute(
                    f"ALTER TABLE {t} ADD CONSTRAINT fk_stocks FOREIGN KEY(index) REFERENCES stocks (ticker);"
                )
            else:
                try:
                    sqldf.to_sql(
                        t, self.engine, if_exists="append", index=True, chunksize=500,
                    )
                except:
                    print(f"{str(df.loc['symbol'].iat[0])} for {t} alread exists.")

    def write(self, df: pd.DataFrame) -> None:
        """Writes a specific stock to DB.

        :param df: pd.DataFrame containig all fundamental data of stock.
        """
        try:
            ticker = str(df.loc["symbol"].iat[0])
            reported_currency = str(df.loc["reportedCurrency"].iat[0])
            cik = str(df.loc["cik"].iat[0])
        except ValueError as err:
            raise ValueError(f"Parameter for stock not found. {err}.")

        # Instantiate the stocks table.
        stock = Stock(ticker=ticker, cik=cik, reported_currency=reported_currency)

        # Writes it to sql db.
        try:
            self.session.add(stock)
            self.session.commit()
        except:
            print(f"{ticker} already exists in DB.")

        # Filling up the data tables.
        self._single_data_pd_to_sql(df)

    def read(self, ticker: str) -> pd.DataFrame:
        """Reads a specific stock from DB.

        :parma ticker: Stock ticker symbol determining the stock.
        :returns: pd.DataFrame containig all fundamental data of stock.
        """
        for idx, t in enumerate(self.tables):
            query = f"SELECT * FROM {self._clean_str(t)} WHERE index = '{ticker}';"
            if idx == 0:
                df = pd.read_sql(query, self.engine, index_col="param")
                df = df.rename({ticker: t})
            else:
                t_df = pd.read_sql(query, self.engine, index_col="param")
                t_df = t_df.rename({ticker: t})
                df = pd.concat([df, t_df])

        df = df.drop(columns=['index'])
        return df
