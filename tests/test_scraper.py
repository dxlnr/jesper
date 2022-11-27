import pandas as pd

from jesper.scraper.yahoo_finance import extract_latest_value


def test_extract_latest_value():
    # DataFrame Layout
    #
    #           Breakdown         ttm  12/31/2021  12/31/2020  12/31/2019  12/31/2018
    # 0     Total Revenue  45210000.0  29882000.0  17337000.0  45768000.0  44541000.0
    # 1   Cost of Revenue  38665000.0  29855000.0  24933000.0  35379000.0  34490000.0
    #
    d1 = {
        "Breakdown": "Reconciled Depreciation",
        "ttm": 11104000.0,
        "12/31/2021": 11104000.0,
        "12/31/2020": 11284000.0,
        "12/31/2019": 11056000.0,
        "12/31/2028": 12547000.0,
    }
    df1 = pd.DataFrame(data=d1, index=[0])

    print(df1)

    d2 = {
        "Breakdown": "Reconciled Depreciation",
        "ttm": "-",
        "12/31/2021": 2335000.0,
        "12/31/2020": 2370000.0,
        "12/31/2019": 2318000.0,
        "12/31/2028": 2159000.0,
    }
    df2 = pd.DataFrame(data=d2, index=[0])

    assert extract_latest_value(df1, "Reconciled Depreciation") == 11104000.0
    assert extract_latest_value(df2, "Reconciled Depreciation") == 2335000.0
