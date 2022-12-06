"""Automated Testing for Read & Write Functions."""
import pandas as pd
from pandas.testing import assert_frame_equal

from jesper.utils.raw import _fill_df


def test_fill_df():
    """."""
    # The previous DataFrame.
    base_d = {
        "2021": [302083, 50672, 64849, None],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
        "2018": [248028, 90488, 45174, 781],
    }
    base_df = pd.DataFrame(
        data=base_d,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    # The DataFrames that will overwrite the baseline df.
    d1 = {
        "2022": [329870, 48205, 70349, 900],
        "2021": [302083, 50672, 64849, 822],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
    }
    df1 = pd.DataFrame(
        data=d1,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    d2 = {
        "2022": [329870, 48205, 70349, 900, 352755],
        "2021": [302083, 50672, 64849, 822, 351002],
        "2020": [287912, 63090, 57365, None, 323888],
        "2019": [258549, 65339, 50779, None, 338516],
    }
    df2 = pd.DataFrame(
        data=d2,
        index=[
            "totalLiab",
            "totalStockholderEquity",
            "commonStock",
            "issuanceOfStock",
            "totalAssets",
        ],
    )

    d3 = {
        "2022": [None, 48205, 70349, 900],
        "2021": [None, 50672, 64849, 822],
        "2020": [None, 63090, 57365, None],
        "2019": [None, 65339, 50779, None],
    }
    df3 = pd.DataFrame(
        data=d3,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    # Get the merged DataFrame from the tested function.
    new_df1 = _fill_df(df1, base_df)
    new_df2 = _fill_df(df2, base_df)
    new_df3 = _fill_df(df3, base_df)

    # Construct the aimed for DataFrames.
    goal_d1 = {
        "2022": [329870, 48205, 70349, 900],
        "2021": [302083, 50672, 64849, 822],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
        "2018": [248028, 90488, 45174, 781],
    }
    goal_df1 = pd.DataFrame(
        data=goal_d1,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    goal_d2 = {
        "2022": [329870, 48205, 70349, 900, 352755],
        "2021": [302083, 50672, 64849, 822, 351002],
        "2020": [287912, 63090, 57365, None, 323888],
        "2019": [258549, 65339, 50779, None, 338516],
        "2018": [248028, 90488, 45174, 781, None],
    }
    goal_df2 = pd.DataFrame(
        data=goal_d2,
        index=[
            "totalLiab",
            "totalStockholderEquity",
            "commonStock",
            "issuanceOfStock",
            "totalAssets",
        ],
    )

    goal_d3 = {
        "2022": [None, 48205, 70349, 900],
        "2021": [302083, 50672, 64849, 822],
        "2020": [287912, 63090, 57365, None],
        "2019": [258549, 65339, 50779, None],
        "2018": [248028, 90488, 45174, 781],
    }
    goal_df3 = pd.DataFrame(
        data=goal_d3,
        index=["totalLiab", "totalStockholderEquity", "commonStock", "issuanceOfStock"],
    )

    assert_frame_equal(new_df1.astype(float), goal_df1.astype(float))
    assert_frame_equal(new_df2.astype(float), goal_df2.astype(float))
    assert_frame_equal(new_df3.astype(float), goal_df3.astype(float))
