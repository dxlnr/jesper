"""Main Entrypoint"""

from jesper.eval_sheet import eval_value_based_stocks
from jesper.scraper.stocks import tickers_sp500, tickers_nasdaq
from jesper.utils.raw import save_stocks_finance_info
from jesper.utils.style import color_low_safety_margin_green


def main():

    from jesper.scraper.roic import scrape_roic
    scrape_roic("AAPL")
    # Get list of ticker symbols of all NASDAQ stocks.
    # nasdaq = tickers_nasdaq()
    # Get list of ticker symbols of all s&p 500 stocks.
    # sp500 = tickers_sp500()
    # Get list of individual symbols.
    # single = ["PYPL", "CRM", "V", "MSFT", "GOOG"]
    # single = ["MSFT"]
    # # Collecting and saving financial information about various stocks.
    # save_stocks_finance_info(sp500)

    # # Calculate evaluation facilitating value based investing.
    # df = eval_value_based_stocks(single)
    # # df = eval_value_based_stocks(sp500, save_results_file="iv_sp500")
    # # Apply styling for highlighting outstanding values.
    # df['intrinsic value'] = df['intrinsic value'].astype(float).round(2)
    # df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # # Print final results.
    # print("\n", df, "\n")


if __name__ == "__main__":
    main()
