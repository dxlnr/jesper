"""Saving Information."""
import concurrent
from functools import partial
from typing import List

from jesper.utils.raw import save_stock_finance_info_to_csv


def save_financial_info_roic(
    stocks: List[str], path: str = "data/roic", max_threads: int = 10, 
) -> None:
    """Saves scraped pandas dataframes to .csv file in concurrent fashion.
    
    :param stocks: List of stocks tickers.
    :paran path: Path to directory where the resulting .csv files get saved. 
    :param max_threads: Number of maximal used threads.
    """
    threads = min(max_threads, len(stocks))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(partial(save_stock_finance_info_to_csv, path=path), stocks)
