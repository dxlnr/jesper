from jesper.scraper.yahoo_finance import scraper_to_latest_stock_price
from jesper.valuation import intrinsic_value
from jesper.eval_sheet import eval_value_based_stocks


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
    #
    # import pandas as pd
    # from jesper.scraper.stocks import tickers_sp500
    # df1 = tickers_sp500()
    # print(type(df1))
    # print(df1)

    # Calculate evaluation facilitating value based investing
    df = eval_value_based_stocks(["AAPL"])
    print(df)

if __name__ == "__main__":
    main()
