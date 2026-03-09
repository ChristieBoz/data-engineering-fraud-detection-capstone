
!pip3 install sqlalchemy
!pip3 install pandas
!pip3 install psycopg2-binary


## import libraries:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2



## create database engine using postgresql connection string:
USERNAME = "postgres"
PASSWORD = "Banana456now!"
HOST = "localhost"
PORT = "5432"
DB_NAME = "fraud_capstone"

engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")


## test connection:
with engine.connect() as conn:
	results = conn.execute(text("SELECT version();"))
	print(results.fetchone())

## test query
with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    print(result.fetchall())


## load the csv into the dataframe - store jupyter notebook and csv in same folder:
df = pd.read_csv("creditcard.csv")


##initial exploration
#df.head() # View first 5 rows
#df.tail() # View last 5 rows
df.shape # Number of rows and columns
df.columns # Return the names of the columns
df.dtypes # Data type of each column
#df.info() # Index, datatype and memory information
#df.describe() # Summary statistics for numeric columns
#df.isnull().sum() # count the number of missing values per column


## load data into sql table :
df.to_sql("credit_card_transactions", engine, schema="raw_schema", if_exists='replace', index=False)


## print postgresql count
with engine.connect() as conn:
	count = conn.execute(text("SELECT COUNT(*) FROM raw_schema.credit_card_transactions;")).scalar()
	print("Rows now in PostgreSQL:", count)


# print fraud/legit count

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT class, COUNT(*) 
        FROM raw_schema.credit_card_transactions
        GROUP BY class
        ORDER BY class;
    """)).fetchall()

for fraud_class, total in result:
    print(f"Class {fraud_class}: {total}")


