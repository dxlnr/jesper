from src.scraper.yahoo_finance import scraper_to_statement
from src.scraper.utils import convert_to_float


def main():
    is_link = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
    bs_link = 'https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL'
    cf_link = 'https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL'

    # Run scraping and return data frame.
    income_df = scraper_to_statement(is_link)
    balance_sheet_df = scraper_to_statement(bs_link)
    cashflow_df = scraper_to_statement(cf_link)

    print("AAPL")
    print("----")
    print(income_df)
    print("\n")
    print(balance_sheet_df)
    print("\n")
    print(cashflow_df)

    # close_price, after_hours_price = stock_prices(is_link)
    # print("\n")
    # print(close_price)
    # print(after_hours_price)

    # from src.scraper.utils import clean
    # print("\n")
    # ebit = clean(incomestatement,'incomeBeforeTax')
    # depreciation = clean(cashflow, 'depreciation')
    # capex = clean(cashflow,'capitalExpenditures')
    # df = pd.concat([ebit, depreciation, capex], axis=1)
    #
    print("\n")
    test = cashflow_df[cashflow_df['Breakdown'] == 'Capital Expenditure']
    mean_capex = test.iloc[:, 2:].mean(axis=1)
    # test.drop('Breakdown', axis=1).drop('ttm', axis=1).apply(lambda x: float(x).mean(), axis=1)
    print(test)
    print(mean_capex)
    # mean_capex = cashflow_df['Capital Expenditure'].mean()
    # print(mean_capex)

if __name__ == "__main__":
    main()
