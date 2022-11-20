import pandas as pd


def load_train_data(path: str = "./data/317_v4_train.parquet"):
    r"""."""
    train_data = pd.read_parquet(path)
    print(train_data)
