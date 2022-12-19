"""SQL Tables MetaData."""
from sqlalchemy import MetaData, Column, String
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base(metadata=MetaData())


class Stock(base):
    __tablename__ = "stocks"
    # Stock ticker symbol defines the primary key, e.g. "AAPL".
    ticker = Column(String(128), primary_key=True, unique=True, nullable=False)

    # Additional information
    cik = Column(String(128), unique=False, nullable=False)
    reported_currency = Column(String(128), unique=False, nullable=False)


    def __init__(self, **kwargs):
        super(Stock, self).__init__(**kwargs)