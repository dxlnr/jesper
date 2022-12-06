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

    # import os
    # from jesper.utils import get_project_root
    # import pandas as pd
    # fpath = os.path.join(get_project_root(), "data/fundamentalData", f"{stock}.csv")
    # pre_df = pd.read_csv(fpath, index_col=0, na_values='(missing)')
    #
    # print(pre_df)
    #
    # for col in pre_df.columns:
    #     print(col)
    #     print(type(col))

    # from jesper.utils.raw import save_stocks_finance_info
    # # Get list of ticker symbols of all s&p 500 stocks.
    # sp500 = tickers_sp500()
    # test = ['AAPL']
    #
    # save_stocks_finance_info(sp500[50:])

    from jesper.scraper.yahoo_finance import get_timeseries_financial_statements
    # df = get_timeseries_financial_statements('AAPL', 'financials')
    # print(df)

    for stock in tickers_sp500():
        print(f"{stock}:")
        print(get_timeseries_financial_statements(stock, 'financials'))

    # print(get_timeseries_financial_statements('AAPL', 'financials'))
    # print(get_timeseries_financial_statements('CE', 'financials'))
    # print(get_timeseries_financial_statements('CE', 'balance-sheet'))
    # print(get_timeseries_financial_statements('CE', 'cash-flow'))


    # save_stocks_finance_info(test)

    # tsm = ['TSM', 'AMD']
    # test = ['AAPL']

    # import random
    # tests = random.sample(sp500, 20)
    # # Calculate evaluation facilitating value based investing.
    # # df = eval_value_based_stocks(sp500[:75])
    # df = eval_value_based_stocks(tsm)
    # # Apply styling for highlighting outstanding values.
    # df['intrinsic value'] = df['intrinsic value'].astype(float).round(2)
    # df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # # Print final results.
    # print("\n", df, "\n")


if __name__ == "__main__":
    main()
