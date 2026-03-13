## import libraries:
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text



def load_raw_data():

	df = pd.read_csv("~/data/creditcard.csv")

	## create database engine using postgresql connection string:
	USERNAME = "postgres"
	PASSWORD = "*******"
	HOST = "localhost"
	PORT = "5432"
	DB_NAME = "fraud_capstone"

	engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

	##initial exploration
	print(df.head()) # View first 5 rows
	print(df.shape) # Number of rows and columns
	print(df.columns) # Return the names of the columns
	print(df.dtypes) # Data type of each column
	
	## load data into sql table :
	df.to_sql("credit_card_transactions", engine, schema='raw_schema', if_exists='replace', index=False)

	## print postgresql count
	with engine.connect() as conn:
		count = conn.execute(text("SELECT COUNT(*) FROM raw_schema.credit_card_transactions;")).scalar()
		print("Raw data loaded:", count)
