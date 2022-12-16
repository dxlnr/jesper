"""Helpers for dealing with .env"""
from dataclasses import dataclass


@dataclass
class DBEnv:
    PSQL_PORT: str = "5423"
    PSQL_HOST: str = "127.0.0.1"
    PSQL_DB_NAME: str = "postgres"
    PSQL_USER: str = "postgres"
    PSQL_PW: str = "postgres"


def get_env_data_as_dict(path: str = ".env") -> dict:
    """Sets env vars from .env file in root."""
    with open(path, "r") as f:
        return dict(
            tuple(line.replace("\n", "").split("="))
            for line in f.readlines()
            if not line.startswith("#")
        )
