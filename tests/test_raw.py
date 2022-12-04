"""Automated Testing for Read & Write Functions."""
import pandas as pd
from pandas.testing import assert_frame_equal

from jesper.utils.raw import _fill_df


def test_fill_df():
    """."""
    # The previous DataFrame
    pre_d = {
        "2021": [302083, 50672, 64849, None],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
        "2018": [248028, 90488, 45174, 781],
    }
    pre_df = pd.DataFrame(
        data=pre_d,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    # The current DataFrame.
    d = {
        "2022": [329870, 48205, 70349, 900],
        "2021": [302083, 50672, 64849, 822],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
    }
    df = pd.DataFrame(
        data=d,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    print("PRE DF: \n", pre_df)

    # Get the merged DataFrame from the tested function.
    new_df = _fill_df(df, pre_df)
    print("")
    print("NEW DF: \n", new_df)

    # Construct the aimed for DataFrame.
    goal_d = {
        "2022": [329870, 48205, 70349, 900],
        "2021": [302083, 50672, 64849, 822],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
        "2018": [248028, 90488, 45174, 781],
    }
    goal_df = pd.DataFrame(
        data=goal_d,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    assert_frame_equal(new_df, goal_df)
