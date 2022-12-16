"""From Pandas to SQL Database"""
import os

import pandas as pd
import psycopg


def clean_c_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Takes a pandas DataFrame & returns it with cleaned up headers."""
    df.columns = [
        x.lower()
        .replace(" ", "_")
        .replace("?", "")
        .replace("-", "_")
        .replace(r"/", "_")
        .replace("\\", "_")
        .replace("%", "")
        .replace(r")", "")
        .replace(r"(", "")
        .replace("$", "")
        for x in df.columns
    ]
    return df


def adjust_dtype(df: pd.DataFrame):
    replacements = {
        "object": "varchar",
        "float64": "float",
        "int64": "int",
        "datetime64": "timestamp",
        "timedelta64[ns]": "varchar",
    }
    col_str = ", ".join("{} {}")


def csv_to_postgresql(csv_path: str, env: dict):
    """."""
    assert not all(
        k in env.items()
        for k in ("PSQL_PORT", "PSQL_HOST", "PSQL_DB_NAME", "PSQL_USER", "PSQL_PW")
    ), "keys are missing in .env \['PSQL_PORT', 'PSQL_HOST', 'PSQL_DB_NAME', 'PSQL_USER', 'PSQL_PW'\]."

    for k, v in env.items():
        print(type(v))

    try:
        with psycopg.connect(
            dbname=env["PSQL_DB_NAME"],
            user=env["PSQL_USER"],
            password=env["PSQL_PW"],
            host=env["PSQL_HOST"],
            port=env["PSQL_PORT"],
        ) as conn:
            cursor = conn.cursor()

            cursor.execute("drop table if exists")
            print("success.")
    except (Exception, psycopg.DatabaseError) as err:
        raise err
