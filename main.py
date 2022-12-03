"""Main Entrypoint"""

import pandas as pd

from jesper.scraper.yahoo_finance import scraper_to_latest_stock_price
from jesper.valuation import intrinsic_value
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

    # # Calculate Intrincic Value.
    # df = intrinsic_value(stock)
    # print(f"\t{stock}\n")
    # print(df)
    #
    # link = f"https://finance.yahoo.com/quote/{stock}?p={stock}"
    # print(scraper_to_latest_stock_price(link))


    # # Get list of ticker symbols of all s&p 500 stocks.
    # sp500 = tickers_sp500()
    # # print(sp500)
    # test = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN']
    # test_ex = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS']

    # Calculate evaluation facilitating value based investing.
    df = eval_value_based_stocks(["AMZN", "AAPL", "AAL", "NVDA"])
    # Apply styling for highlighting outstanding values.
    df.round({'intrinsic value': 2})
    df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # Print final results.
    print("\n", df, "\n")
    
    # from jesper.scraper.yahoo_finance import get_balance_sheet, get_income_statement, get_cash_flow
    # stock = "AMZN"
    # # stock = "META"
    # # stock = "NVDA"
    # bs_df = get_balance_sheet(stock)
    # in_df = get_income_statement(stock)
    # cf_df = get_cash_flow(stock)
    # print(bs_df)
    # print(in_df)
    # print(cf_df)

    # from jesper.valuation import annual_report_readings
    # from jesper.utils.style import readable_df
    # df = annual_report_readings(stock)
    # print(f"\n\t{stock}\n".expandtabs(4))
    # print(readable_df(df))


if __name__ == "__main__":
    main()
