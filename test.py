from jesper.sql.pd_to_sql import csv_to_postgresql
from jesper.sql.db_tables import Stock, Base
import pandas as pd
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


from jesper.sql.env import DBEnv
env = DBEnv()
env.merge_from_file("server/.env")

sql_str = env.get_uri_sqlalchemy()
print(sql_str)

engine = create_engine(env.get_uri_sqlalchemy(), echo=True)

session = Session(engine)
Base.metadata.create_all(engine)
# base = declarative_base()

# stock = Stock(ticker="AAPL", fundamental_data=tmp.to_sql(
#     'fundamental_data',
#     engine,
#     if_exists='replace',
#     index=True,
#     chunksize=500)
# )

# from sqlalchemy import Column, String  
# class Stock(base):  
#     __tablename__ = 'stocks'

#     ticker = Column(String(128), primary_key=True, unique=True, nullable=False)


nvda_df = pd.read_csv('data/NVDA.csv', index_col=0, na_values="(missing)")

# df = pd.DataFrame(columns=list(nvda_df.columns))
print(nvda_df)

# for i in range(len(list(nvda_df.columns))):
#     df.at[i, "revenue"] = nvda_df.loc["revenue"].iat[i]

# df = pd.concat([df, nvda_df.loc["revenue"].transpose()])
symbol = nvda_df.loc["symbol"].iat[0]
print(symbol)
df = nvda_df.loc[["revenue"]]
df = df.rename({"revenue": str(symbol)})

# df.rename(columns=df.iloc[0])
# df = nvda_df.loc["revenue"].set_index("revenue").T
# df = nvda_df.iloc[0]
print(df)
# print(nvda_df.loc["revenue"])
# print(list(nvda_df.transpose().columns))
# [print(x) for x in nvda_df.transpose()]

# nvda_df = nvda_df.transpose()

df.to_sql(
    'revenue',
    engine,
    if_exists='append',
    # if_exists='append',
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
    # dtype={
    #     'index': 'PRIMARY KEY',
    # }
)

engine.execute('ALTER TABLE revenue ADD PRIMARY KEY (index);')

# engine.execute('ALTER TABLE nvda ADD PRIMARY KEY (symbol) ;')

# engine.execute("ALTER TABLE stocks ADD COLUMN data INT NOT NULL ;")

# engine.execute("ALTER TABLE nvda ADD CONSTRAINT data_id UNIQUE USING INDEX data_stocks_id_idx;")
# engine.execute("CONSTRAINT y_x_fk_c REFERENCES nvda")
# engine.execute("alter table stocks add constraint fk_stocks_data foreign key (ticker, nvda) references nvda ;")

# # stock = Stock(ticker="AAPL")
# another_stock = Stock(ticker="NVDA")
# session.add(another_stock)
# session.commit()

# table_df = pd.read_sql_table(
#     "data",
#     engine,
#     index_col="index",
# )

# print(table_df.transpose())
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