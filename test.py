from jesper.sql.pd_to_sql import csv_to_postgresql
# from jesper.sql.env import get_env_data_as_dict
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


from jesper.sql.env import DBEnv
env = DBEnv()
env.merge_from_file("server/.env")

sql_str = env.get_uri_sqlalchemy()
print(sql_str)

engine = create_engine(env.get_uri_sqlalchemy(), echo=True)

aapl_df = pd.read_csv('data/AAPL.csv', index_col=0, na_values="(missing)")

# print(aapl_df.transpose())

aapl_df.to_sql(
    'data',
    engine,
    if_exists='replace',
    index=True,
    chunksize=500,
    # dtype={
    #     "job_id": Integer,
    #     "agency": Text,
    #     "business_title": Text,
    #     "job_category":  Text,
    #     "salary_range_from": Integer,
    #     "salary_range_to": Integer,
    #     "salary_frequency": String(50),
    #     "work_location": Text,
    #     "division/work_unit": Text,
    #     "job_description": Text,
    #     "posting_date": DateTime,
    #     "posting_updated": DateTime
    # }
)

table_df = pd.read_sql_table(
    "data",
    engine
)

print(table_df.transpose())
# from jesper.sql.db_tables import Stocks, Stock

# session = Session(engine)

# # declarative_base().metadata.create_all(engine)
# from sqlalchemy import Column, String  
# from sqlalchemy.ext.declarative import declarative_base 

# base = declarative_base()


# class Film(base):  
#     __tablename__ = 'films'

#     title = Column(String, primary_key=True)
#     director = Column(String)
#     year = Column(String)

# # Session = sessionmaker(engine)  
# # session = Session()
# base.metadata.create_all(engine)

# # Create 
# doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")  
# session.add(doctor_strange)  
# session.commit()

# # Create
# doctor_strange = Stocks()
# session.add(doctor_strange)
# session.commit()

# c = psycopg2.connect(database="jesper", user="postgres", password="", host="localhost", port="5423")

#
# postgres+psycopg2://myuser:mypassword@hackersdb.example.com:5432/mydatabase
#


# conn = psycopg2.connect(
#    database="jesper", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
# )

# cursor = conn.cursor()

# env = get_env_data_as_dict("server/.env")
# print(env)

# csv_to_postgresql("test", env)