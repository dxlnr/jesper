"""Main Entrypoint"""
from tabulate import tabulate

from jesper.eval_sheet import eval_value_based_stocks
from jesper.savings import save_financial_info_roic
from jesper.scraper.stocks import tickers_dow, tickers_nasdaq, tickers_sp500
from jesper.sql import JesperSQL
from jesper.sql.env import DBEnv
from jesper.utils.style import color_low_safety_margin_green


def main():
    ##########################################################################
    # Scraping & Saving Data
    ##########################################################################
    # Get list of ticker symbols of all NASDAQ stocks.
    nasdaq = tickers_nasdaq()
    # Get list of ticker symbols of all s&p 500 stocks.
    sp500 = tickers_sp500()
    #
    # Collecting and saving financial information
    # about various stocks from roic.ai
    save_financial_info_roic(sp500, path="data/roic/sp500")

    ##########################################################################
    # Stock Evaluation
    ##########################################################################

    # Calculate evaluation facilitating value based investing.
    single = ["AAPL", "META"]
    df = eval_value_based_stocks(single, path_to_csv="data")
    # df = eval_value_based_stocks(single, path_to_csv="data/roic/nyse")
    # df = eval_value_based_stocks(
    #     sp500[:100], path_to_csv="data/roic/sp500", save_results_file="iv_sp500_0_100"
    # )
    # Apply styling for highlighting outstanding values.
    df["intrinsic value"] = df["intrinsic value"].astype(float).round(2)
    df["safety margin"] = df["safety margin"].apply(color_low_safety_margin_green)
    # Print final results.
    print("\n", tabulate(df, showindex=True, headers=df.columns), "\n")

    ##########################################################################
    # SQL Database Actions
    ##########################################################################
    env = DBEnv()
    env.merge_from_file("server/.env")

    j_sql = JesperSQL(env)

    # Writing to SQL Database.
    # nvda_df = pd.read_csv('data/NVDA.csv', index_col=0, na_values="(missing)")
    # aapl_df = pd.read_csv('data/AAPL.csv', index_col=0, na_values="(missing)")
    # meta_df = pd.read_csv('data/META.csv', index_col=0, na_values="(missing)")

    # for s_df in [aapl_df, nvda_df, meta_df]:
    #     j_sql.write(s_df)

    # Reading from SQL Database.
    df = j_sql.read("AAPL")
    print(df)


if __name__ == "__main__":
    main()
