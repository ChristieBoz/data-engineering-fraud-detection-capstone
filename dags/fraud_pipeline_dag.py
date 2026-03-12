#define the work flow container
from airflow import DAG
#runs each python function as a task
from airflow.operators.python import PythonOperator
#runs the sql scripts
from airflow.providers.postgres.operators.postgres import PostgresOperator
# used to define when the DAG starts
from datetime import datetime

import os
import sys

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', os.path.expanduser('~/airflow'))
SCRIPTS_PATH = os.path.join(AIRFLOW_HOME, 'scripts')
if SCRIPTS_PATH not in sys.path:
    sys.path.append(SCRIPTS_PATH)


from pendulum import duration

#import the functions from the scripts
from load_raw_data import load_raw_data
from feature_engineering import feature_engineering
from baseline_modeling import baseline_modeling
from curated_modeling import curated_modeling
from comparison import comparison

#default dag settings  - owner and start date

default_args = {
	"owner": "owner_name",
	"start_date": datetime(2026, 3, 3),
	"retries": 0,
	"retry_delay": duration(seconds=2),
}

#define the pipeline
with DAG(
	dag_id="fraud_detection_pipeline", #dag name
	default_args=default_args,
	schedule_interval=None, #dag will only run when triggered manually - could be @daily or @hourly
	catchup=False # prevents airflow from trying to run past scheduled jobs
) as dag:

	# create schemas
	create_schemas_task = PostgresOperator(
		task_id="create_schemas",
		postgres_conn_id="postgres_default",
		sql="../sql/create_schemas.sql"
	)
	# create raw table
	create_raw_table_task = PostgresOperator(
		task_id="create_raw_table",
		postgres_conn_id="postgres_default",
		sql="../sql/create_raw_table.sql"
	)
	#create staging table
	create_staging_table_task = PostgresOperator(
		task_id="create_staging_table",
		postgres_conn_id="postgres_default",
		sql="../sql/create_staging_table.sql"
	)
	# load staging table - selects distinct rows(removes dupes) - filters invalid amounts and moves cleaned data from raw to staging
	load_staging_task = PostgresOperator(
		task_id="load_staging",
		postgres_conn_id="postgres_default",
		sql="../sql/load_staging.sql"
	)

	# create curated table
	create_curated_table_task = PostgresOperator(
		task_id="create_curated_table",
		postgres_conn_id="postgres_default",
		sql="../sql/create_curated_table.sql"
	)

	#loading the csv file into the dataframe and then into postgresql raw table
	load_raw_data_task = PythonOperator(
		task_id="load_raw_data",
		python_callable=load_raw_data #the functions that airflow will execute
	)

	# feature_engineering - reads staging data from postgres, created rolling features in pandas, writes results to curated table
	feature_engineering_task = PythonOperator(
		task_id="feature_engineering",
		python_callable=feature_engineering #the functions that airflow will execute
	)

	#baseline model training - uses staged data, trains logistic regression and random forest - exports to a new csv
	baseline_modeling_task = PythonOperator(
		task_id="baseline_modeling",
		python_callable=baseline_modeling #the functions that airflow will execute
	)
	# curated model training - uses curated data, trains logistic regression and random forest - exports to a new csv
	curated_modeling_task = PythonOperator(
		task_id="curated_modeling",
		python_callable=curated_modeling #the functions that airflow will execute
	)
	# compare models - loass both csvs, concats the results, created new csv. generates chart
	comparison_task = PythonOperator(
		task_id="comparison",
		python_callable=comparison #the functions that airflow will execute
	)

create_schemas_task >> create_raw_table_task >> load_raw_data_task >> create_staging_table_task >> load_staging_task >> create_curated_table_task >> feature_engineering_task >> baseline_modeling_task >> curated_modeling_task >> comparison_task

