"""Saving Information."""
import concurrent
from functools import partial
from typing import List

from jesper.utils.raw import save_stock_finance_info_to_csv


def save_financial_info_roic(
    stocks: List[str], max_threads: int = 10, path: str = "data/roic"
) -> None:
    """."""
    threads = min(max_threads, len(stocks))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(partial(save_stock_finance_info_to_csv, path=path), stocks)
