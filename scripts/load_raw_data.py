def load_raw_data():
## import libraries:
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2

## create database engine using postgresql connection string:
USERNAME = "postgres"
PASSWORD = "password"
HOST = "localhost"
PORT = "5432"
DB_NAME = "fraud_capstone"

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")


df = pd.read_csv("/Users/student/Desktop/test/creditcard.csv")

##initial exploration
df.head() # View first 5 rows
df.shape # Number of rows and columns
df.columns # Return the names of the columns
df.dtypes # Data type of each column

## load data into sql table :
df.to_sql("credit_card_transactions", engine, schema='raw_schema', if_exists='append', index=False)


## print postgresql count
with engine.connect() as conn:
count = conn.execute(text("SELECT COUNT(*) FROM raw_schema.credit_card_transactions;")).scalar()
	print("Rows now in PostgreSQL:", count)
