from jesper.sql.db_tables import Stock, base
import pandas as pd
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from jesper.sql import JesperSQL
from jesper.sql.env import DBEnv
env = DBEnv()
env.merge_from_file("server/.env")

# sql_str = env.get_uri_sqlalchemy()
# print(sql_str)

# engine = create_engine(env.get_uri_sqlalchemy(), echo=True)

# session = Session(engine)
# base.metadata.create_all(engine)

j_sql = JesperSQL(env)

nvda_df = pd.read_csv('data/NVDA.csv', index_col=0, na_values="(missing)")
print(nvda_df)

j_sql.write(nvda_df)
