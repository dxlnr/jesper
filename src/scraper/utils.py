import pandas as pd


def clean(x, y):
    """."""
    df = pd.DataFrame(x.iloc[0, 0])
    df = df.loc[:, df.columns.str.contains(y)]
    df = pd.json_normalize(df[y])
    df = pd.DataFrame(df.raw)
    df.columns = [y]
    return df


def has_digits(in_str: str) -> bool:
    """Returns Bool if str contains digits."""
    return any(char.isdigit() for char in in_str)


def convert_to_float(df: pd.DataFrame):
    """Takes scraped dataframe and converts the str numbers to floats."""
    for idx, key in enumerate(df.columns):
        if idx == 0:
            continue

        df[key] = [
            float(str(i).replace(",", "")) if has_digits(i) else i for i in df[key]
        ]
    return df
