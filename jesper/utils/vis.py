import pandas as pd


def print_full(x: pd.DataFrame):
    """Prints the whole DataFrame to the screen."""
    pd.set_option("display.max_rows", len(x))
    print("\n", x, "\n")
    pd.reset_option("display.max_rows")
