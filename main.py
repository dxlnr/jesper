from src.scraper.yahoo_finance import scraper_to_statement


def main():
    is_link = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
    bs_link = 'https://finance.yahoo.com/quote/AAPL/balance-sheet?p=AAPL'
    cf_link = 'https://finance.yahoo.com/quote/AAPL/cash-flow?p=AAPL'

    df = scraper_to_statement(is_link)
    print(df)
    # close_price, after_hours_price = stock_prices(is_link)
    # print("\n")
    # print(close_price)
    # print(after_hours_price)

if __name__ == "__main__":
    main()
