## import libraries:
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2


def load_raw_data():

	import os

	AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', os.path.expanduser('~/airflow'))
	csv_path = os.path.join(AIRFLOW_HOME, 'data', 'creditcard.csv')


	## create database engine using postgresql connection string:
	USERNAME = "postgres"
	PASSWORD = "*******"
	HOST = "localhost"
	PORT = "5432"
	DB_NAME = "fraud_capstone"

	engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

	df = pd.read_csv(csv_path)

	##initial exploration
	print(df.head()) # View first 5 rows
	print(df.shape) # Number of rows and columns
	print(df.columns) # Return the names of the columns
	print(df.dtypes) # Data type of each column
	
	## load data into sql table :
	df.to_sql("credit_card_transactions", engine, schema='raw_schema', if_exists='append', index=False)

	## print postgresql count
	with engine.connect() as conn:
		count = conn.execute(text("SELECT COUNT(*) FROM raw_schema.credit_card_transactions;")).scalar()
		print("Rows now in PostgreSQL:", count)
