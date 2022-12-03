"""Basic Scraping functions."""
import json
import re
from typing import Dict

import requests
from bs4 import BeautifulSoup


def get_event_page(url: str):
    """Download a webpage and return a beautiful soup doc."""
    # Web API headers.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    # Pull data from link.
    try:
        page_response = requests.get(url, headers=headers, timeout=1000)
    except:
        raise Exception("Failed to load page {}".format(url))
    # Structure raw data for parsing.
    page_content = BeautifulSoup(page_response.content, features="html.parser")

    return page_content


def _parse_page_content_as_json(
    url: str,
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    },
):
    try:
        html = requests.get(url=url, headers=headers).text
    except:
        raise Exception("Failed to load page {}".format(url))

    json_str = (
        html.split("root.App.main =")[1].split("(this)")[0].split(";\n}")[0].strip()
    )
    try:
        summary_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
            "QuoteSummaryStore"
        ]
        timeseries_data = json.loads(json_str)["context"]["dispatcher"]["stores"][
            "QuoteTimeSeriesStore"
        ]
    except:
        return "{}"
    else:
        # return summary data.
        new_summary_data = json.dumps(summary_data).replace("{}", "null")
        new_summary_data = re.sub(
            r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_summary_data
        )
        json_summary_data = json.loads(new_summary_data)

        # return summary data.
        new_time_data = json.dumps(timeseries_data).replace("{}", "null")
        new_time_data = re.sub(
            r"\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}", r"\1", new_time_data
        )
        json_time_data = json.loads(new_time_data)

        return json_summary_data, json_time_data
