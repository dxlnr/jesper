"""Styling Helper for Printing."""
from typing import List
import colorama
import math


def pd_color_low_safety_margin_green(val):
    """Takes a scalar and returns a string with the css property color adjusted."""
    color = "green" if 0 < val <= 0.3 else "black"
    return "color: %s" % color


def color_low_safety_margin_green(val):
    """Colorize specific value between 0 & 0.3."""
    color = colorama.Fore.GREEN if 0 < val <= 0.3 else colorama.Fore.WHITE
    return color + str("{:>.2%}".format(val)) + colorama.Style.RESET_ALL


def millify(n, names: List[str] = ["", "", "M", "B", "T"]):
    """Extracts the most significant part and returns it as str."""
    n = float(n)
    idx = max(
        0, min(len(names) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3)))
    )

    if idx <= 1:
        return "{:.0f}".format(n)
    else:
        return "{:.0f}{}".format(n / 10 ** (3 * idx), names[idx])


def readable_df(df):
    """Improves the readablility of the df reports."""
    # Extract most significant part of huge integers.
    for k in df.keys()[:4]:
        df[k] = df[k].apply(lambda x: millify(x))
    # Convert to percentage numbers.
    for k in df.keys()[4:]:
        df[k] = df[k].map('{:.2%}'.format)

    return df
