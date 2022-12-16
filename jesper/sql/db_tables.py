from sqlalchemy.orm import relationship
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Stocks(Base):
    __tablename__ = "stocks_table"
    id = Column(Integer, primary_key=True, autoincrement="auto")

    tickers = relationship("Stock", back_populates="stocks")

    def __init__(self, **kwargs):
        super(Stocks, self).__init__(**kwargs)


class Stock(Base):
    __tablename__ = "stock_table"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    ticker = Column(String(128), unique=True, nullable=False)

    stocks_id = Column(Integer, ForeignKey('stocks_table.id'), nullable=False)
    stocks = relationship("Stocks", back_populates='tickers')