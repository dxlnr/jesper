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

    # test = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN']
    # Get list of ticker symbols of all s&p 500 stocks.
    sp500 = tickers_sp500()
    # Calculate evaluation facilitating value based investing.
    df = eval_value_based_stocks(sp500[:10])
    # Apply styling for highlighting outstanding values.
    df = df.round({"intrinsic value": 2})
    df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # Print final results.
    print("\n", df, "\n")


if __name__ == "__main__":
    main()
