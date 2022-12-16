from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Date,
    ForeignKey,
    BigInteger,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Stocks(declarative_base(metadata=MetaData())):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, autoincrement="auto")

    edge_devices = relationship('Stock', back_populates='stocks', lazy=True)

    def __init__(self, **kwargs):
        super(Stocks, self).__init__(**kwargs)


class Stock(declarative_base(metadata=MetaData())):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    ticker = Column(String(128), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Stock, self).__init__(**kwargs)
