#define the work flow container
from airflow import DAG
#runs each python function as a task
from airflow.operators.python import PythonOperator
#runs the sql scripts
from airflow.providers.postgres.operators.postgres import PostgresOperators
# used to define when the DAG starts
from datetime import datetime

import sys
sys.path.append("/Users/christinaboswell/Desktop/CAPSTONE")

#import the functions from the scripts
from scripts.load_raw_data.py import load_raw_data
from scripts.feature_engineering import feature_engineering
from scripts.baseline_modeling import baseline_modeling
from scripts.curated_modeling import curated_modeling
from scripts.comparison import comparison

#default dag settings  - owner and start date

default_args = {
	"owner": "christina",
  "start_date": datetime(2026, 3, 3),
  "retries": 1
}

#define the pipeline

with DAG(
	dag_is="fraud_detection_pipeline", #dag name
	default_args=default_args,
	schedule_interval=None, #dag will only run when triggered manually - could be @daily or @hourly
	catchup=False # prevents airflow from trying to run past scheduled jobs
) as dag:

# create schemas
create_schemas = PostgresOperator(
	task_id="create_schemas",
	postgres_conn_id="postgres_default",
	sql="create_schemas.sql"
)
# create raw table
create_raw_table = PostgresOperators(
	task_id="create_raw_table"
	postgres_conn_id="postgres_default",
	sql="create_raw_table.sql"
)
#create staging table
create_staging_table = PostgresOperators(
	task_id="create_staging_table"
	postgres_conn_id="postgres_default",
	sql=" create_staging_table.sql"
)
# load staging table - selects distinct rows(removes dupes) - filters invalid amounts and moves cleaned data from raw to staging
load_staging = PostgresOperators(
	task_id="load_staging"
	postgres_conn_id="postgres_default",
	sql="load_staging.sql"
)

# create curated table
create_curated_table = PostgresOperators(
	task_id="create_curated_table"
	postgres_conn_id="postgres_default",
	sql="create_curated_table.sql"
)

#loading the csv file into the dataframe and then into postgresql raw table
load_raw_data = PythonOperator(
task_id="load_raw_data",
python_callable=load_raw_data #the functions that airflow will execute
)

# feature_engineering - reads staging data from postgres, created rolling features in pandas, writes results to curated table
load_data = PythonOperator(
task_id="feature_engineering",
python_callable=feature_engineering #the functions that airflow will execute
)

#baseline model training - uses staged data, trains logistic regression and random forest - exports to a new csv
load_data = PythonOperator(
task_id="baseline_modeling",
python_callable=baseline_modeling #the functions that airflow will execute
)
# curated model training - uses curated data, trains logistic regression and random forest - exports to a new csv
load_data = PythonOperator(
task_id="curated_modeling",
python_callable=curated_modeling #the functions that airflow will execute
)
# compare models - loass both csvs, concats the results, created new csv. generates chart
load_data = PythonOperator(
task_id="comparison",
python_callable=comparison #the functions that airflow will execute
)

create_schemas >> create_raw_table >> load_raw_data_task >> create_staging_table >> load_staging >> create_curated_table >> feature_engineering_task >> baseline_modeling_task >> curated_modeling_task >> comparison_task
