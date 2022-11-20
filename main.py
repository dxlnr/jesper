from src.scraper.yahoo_finance import scraper_to_latest_stock_price
from src.valuation import intrinsic_value


def main():
    # Calculate Intrincic Value.
    df = intrinsic_value("AAPL")
    print("\tAAPL\n")
    print(df)


    link = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
    print(scraper_to_latest_stock_price(link))


if __name__ == "__main__":
    main()
