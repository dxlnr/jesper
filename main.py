"""Main Entrypoint"""

from jesper.eval_sheet import eval_value_based_stocks
from jesper.scraper.stocks import tickers_sp500
from jesper.utils.style import color_low_safety_margin_green


def main():
    # Choose single stock.
    #
    # Apple Inc. (AAPL)
    stock = "AAPL"
    #
    # Alphabet Inc. (GOOG)
    # stock = "GOOG"
    #
    # Meta Platforms, Inc. (META)
    # stock = "META"
    #
    # Tesla, Inc. (TSLA)
    # stock = "TSLA"
    #
    # NVIDIA Corporation (NVDA)
    # stock = "NVDA"
    #
    # Jumia Technologies AG (JMIA)
    # stock = "JMIA"
    #
    # Sono Group N.V. (SEV)
    # stock = "SEV"
    from jesper.utils import get_project_root
    print(get_project_root())

    import pandas as pd
    from jesper.scraper.yahoo_finance import get_balance_sheet, get_income_statement, get_cash_flow
    from jesper.utils.raw import save_statements_to_csv
    stock = "AAPL"

    balance_sheet_df = get_balance_sheet(stock)
    income_df = get_income_statement(stock)
    cashflow_df = get_cash_flow(stock)
    # print(balance_sheet_df)
    # print(income_df)
    # print(cashflow_df)
    save_df = pd.concat([balance_sheet_df, income_df, cashflow_df])

    save_statements_to_csv(save_df, stock)
    """
    # test = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN']
    # Get list of ticker symbols of all s&p 500 stocks.
    sp500 = tickers_sp500()
    # from jesper.scraper.yahoo_finance import get_company_info
    # ci_df = get_company_info("AAPL")
    # print(ci_df)

    tsm = ['TSM']
    test = ['AAPL']
    import random
    tests = random.sample(sp500, 20)
    # Calculate evaluation facilitating value based investing.
    # df = eval_value_based_stocks(sp500[:75])
    df = eval_value_based_stocks(test)
    # Apply styling for highlighting outstanding values.
    df['intrinsic value'] = df['intrinsic value'].astype(float).round(2)
    df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # Print final results.
    print("\n", df, "\n")
    """

if __name__ == "__main__":
    main()
