from sqlalchemy import MetaData, Column, Integer, Float, String, DateTime, Date, ForeignKey, BigInteger, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Stock(declarative_base(metadata=MetaData())):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    ticker = Column(String(128), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super(Stock, self).__init__(**kwargs)
