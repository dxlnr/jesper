from jesper.sql.pd_to_sql import csv_to_postgresql
from jesper.sql.env import get_env_data_as_dict
import psycopg2

# c = psycopg2.connect(database="jesper", user="postgres", password="", host="localhost", port="5423")

conn = psycopg2.connect(
   database="jesper", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
)

cursor = conn.cursor()

env = get_env_data_as_dict("server/.env")
print(env)

csv_to_postgresql("test", env)