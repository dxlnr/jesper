"""SQL Tables MetaData."""
from sqlalchemy import Column, ForeignKey, MetaData, String
from sqlalchemy.ext.declarative import declarative_base

# from sqlalchemy.orm import relationship

base = declarative_base(metadata=MetaData())


class Stock(base):
    __tablename__ = "stocks"
    # Stock ticker symbol defines the primary key, e.g. "AAPL".
    ticker = Column(String(128), primary_key=True, unique=True, nullable=False)

    # Additional information
    cik = Column(String(128), unique=False, nullable=False)
    reported_currency = Column(String(128), unique=False, nullable=False)

    # # Data relationship table (one-to-one)
    # data = relationship("Data", back_populates="stock", lazy=True)

    def __init__(self, **kwargs):
        super(Stock, self).__init__(**kwargs)


# class Data(base):
#     __tablename__ = "data"
#     # Stock ticker symbol defines the primary key, e.g. "AAPL".
#     ticker = Column(
#         String(128),
#         ForeignKey("stocks.ticker"),
#         primary_key=True,
#         unique=True,
#         nullable=False,
#     )

#     # Relates back to Stock (one-to-one).
#     stock = relationship("Stock", back_populates="data", lazy=True)
