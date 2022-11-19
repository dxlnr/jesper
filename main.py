from src.scraper.yahoo_finance import scraper_to_statement
from src.scraper.utils import convert_to_float, extract_ttm_value
from src.valuation import return_table


def main():
    is_link = "https://finance.yahoo.com/quote/AAPL/financials?p=AAPL"
    bs_link = "https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL"
    cf_link = "https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL"

    # Run scraping and return data frame.
    income_df = scraper_to_statement(is_link)
    balance_sheet_df = scraper_to_statement(bs_link)
    cashflow_df = scraper_to_statement(cf_link)

    print("\tAAPL")
    print("\t")
    print("Income Report: ")
    print(income_df)
    print("\n")
    print("Balance Sheet: ")
    print(balance_sheet_df)
    print("\n")
    print("Cashflow Report: ")
    print(cashflow_df)

    # Instantiate resulting table.
    df = return_table()

    # # Pulling in the desired fields ebit, depreciation & capex
    df.at[0, 'incomeBeforeTax'] = extract_ttm_value(income_df, 'EBIT')
    df.at[0, 'depreciation'] = extract_ttm_value(income_df, 'Reconciled Depreciation')
    df.at[0, 'capitalExpenditures'] = extract_ttm_value(cashflow_df, 'Capital Expenditure')

    # Calculating Average Capital Expenditure.
    cp_exp_row = cashflow_df[cashflow_df["Breakdown"] == "Capital Expenditure"]
    mean_capex = cp_exp_row.iloc[:, 2:].mean(axis=1).astype(float)
    df.at[0, 'Average Capex'] = mean_capex.iloc[0]

    # Calculating Owners Earnings
    earnings = df['incomeBeforeTax'] + df['depreciation'] - df['Average Capex']
    df.at[0, 'Owners Earnings'] = earnings.iloc[0]

    # Show results.
    print("\n")
    print(df)


if __name__ == "__main__":
    main()
