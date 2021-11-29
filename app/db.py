from os import getenv
import databases
import sqlalchemy

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_PORT = getenv("POSTGRES_PORT")

DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@f_db:{POSTGRES_PORT}/{POSTGRES_DB}'
print("TEST")
print(DB_URL)
db = databases.Database(DB_URL)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DB_URL)