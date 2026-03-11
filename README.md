# Data Engineering Fraud Detection Capstone
WGU Capstone Project - Credit Card Fraud Detection 
PostgreSQL - Apache Airflow - Python

## Project Overview
This project implemented a full ETL pipeline for credit card fraud detection using the Credit Card Fraud Detection found on Kaggle.com. The goal is to show that if engineered behavioral features are added to a multi-layered ETL pipeline can enchance the performace of fraud detection modeling. 
This pipeline uses PostgreSQL for data storage, Apache Airflow for pipeline orchestration, Python for feature engineering and machine learning, and scikit-learn for model training and evaluation.

## Architechture

Kaggle Dataset > Raw data layer > Staging data layer > Feature Engineering > Curated data layer > Machine Learning models > Model comparision

### Schema Layers

Raw Layer: 
Stores the original transaction dataset without any modifications
PostgreSQL table: raw_schema.credit_card_transactions

Staging Layer: 
Contains the cleaned and validated transactions
  Tranformations: duplicate removal and validation of transactions amount
PostgreSQL table: staging_schema.cleaned_transactions

Curated Layer: 
Contains engineered behavioral features used for ml model training
PostgreSQL table: curated_schema.feature_engineered_transactions
Engineered Features: 
* rolling_avg_amount_10 
* rolling_std_amount_10 
* rolling_sum_amount_10 
* amount_zscore 
* high_value_flag 
* amount_velocity

### Airflow Orchestration

create_schemas_task >> create_raw_table_task >> load_raw_data_task >> create_staging_table_task >> load_staging_task >> create_curated_table_task >> feature_engineering_task >> baseline_modeling_task >> curated_modeling_task >> comparison_task

### Model Training and Metrics

Two models were trained on each dataset. Logistic Regression and Random Forest. They were run on "Baseline" and "Curated" datasets. The baseline is the cleaned dataset from the Staging Layer and the curated is the feature engineered data from the Curated Layer

Baseline = staging_schema.cleaned_transactions
Curated = curated_schema.feature_engineered_transactions

Metrics used
* Precision
* Recall
* F1 Score
* ROC_AUC
* Importance

Results are saved to curated_results.csv

### Repository Structure
architecture/
* pipeline_architecture.png

dags/
* fraud_pipeline_dag.py

scripts/
* baseline_modeling.py
* comparison.py
* curated_modeling.py
* feature_engineering.py
* load_raw_data.py

sql/
* create_curated_table.sql
* create_database.sql
* create_raw_table.sql
* create_schemas.sql
* create_staging_table.sql
* load_staging.sql

README.md

requirements.txt





## Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher (running and accessible)
- The following Python packages (install with `pip3 install -r requirements.txt`)

## Installation

1. **Install Python 3.8+**  
   Download from [python.org](https://www.python.org/downloads/).

2. **Install PostgreSQL 12+**  
   Download from [postgresql.org](https://www.postgresql.org/download/).

3. **Install Python dependencies**
   pip3 install -r requirements.txt

