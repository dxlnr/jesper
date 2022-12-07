"""Scrape all the stock tickers."""
import io

import pandas as pd
import ftplib


def tickers_sp500(include_company_data=False):
    """Downloads list of tickers currently listed in the S&P 500."""
    sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    sp500["Symbol"] = sp500["Symbol"].str.replace(".", "-", regex=True)

    if include_company_data:
        return sp500

    sp_tickers = sp500.Symbol.tolist()
    sp_tickers = sorted(sp_tickers)

    return sp_tickers


def tickers_nasdaq(include_company_data = False):
    """Downloads list of tickers currently listed in the NASDAQ."""
    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")
    
    r = io.BytesIO()
    ftp.retrbinary('RETR nasdaqlisted.txt', r.write)
    
    if include_company_data:
        r.seek(0)
        data = pd.read_csv(r, sep = "|")
        return data
    
    info = r.getvalue().decode()
    splits = info.split("|")
    
    
    tickers = [x for x in splits if "\r\n" in x]
    tickers = [x.split("\r\n")[1] for x in tickers if "NASDAQ" not in x != "\r\n"]
    tickers = [ticker for ticker in tickers if "File" not in ticker]    
    
    ftp.close()    

    return tickers