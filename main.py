"""Main Entrypoint"""

from jesper.eval_sheet import eval_value_based_stocks
from jesper.savings import save_financial_info_roic
from jesper.scraper.stocks import tickers_sp500, tickers_nasdaq, tickers_dow
from jesper.utils.raw import save_stocks_finance_info
from jesper.utils.style import color_low_safety_margin_green
from jesper.utils.vis import print_full


def main():
    # Get list of ticker symbols of all NASDAQ stocks.
    # nasdaq = tickers_nasdaq()
    # Get list of ticker symbols of all s&p 500 stocks.
    sp500 = tickers_sp500()

    # df = _convert_data_to_df(data["props"]["pageProps"]["data"]["data"]["outlook"])
    # # from jesper.scraper.yahoo_finance import get_financial_statements
    # df = scrape_roic("CPT")
    # print("\n", df, "\n")

    # Collecting and saving financial information
    # about various stocks from roic.ai
    #
    save_financial_info_roic(sp500, path="data/roic/sp500")

    # # Calculate evaluation facilitating value based investing.
    # single = ["TSM", "TCEHY"]
    # # df = eval_value_based_stocks(single, path_to_csv="data/roic/sp500")
    # df = eval_value_based_stocks(
    #     sp500[100:125], path_to_csv="data/roic/sp500", save_results_file="iv_sp500_100_125"
    # )
    # # Apply styling for highlighting outstanding values.
    # df["intrinsic value"] = df["intrinsic value"].astype(float).round(2)
    # df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # # Print final results.
    # # print("\n", df, "\n")
    # print_full(df)


if __name__ == "__main__":
    main()
