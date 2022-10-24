"""Main entrypoint."""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.data.raw import load_train_data


def main():
    # load_train_data('../data/317_v4_train.parquet')

    print('Reading minimal training data')
    # read the feature metadata and get a feature set (or all the features)
    with open("data/numerai/features.json", "r") as f:
        feature_metadata = json.load(f)

        features = feature_metadata["feature_sets"]["medium"]

        print(features)


if __name__ == "__main__":
    main()
