# Data Engineering Fraud Detection Capstone
WGU Capstone Project - Credit Card Fraud Detection  
**Technologies:** PostgreSQL · Apache Airflow · Python · scikit-learn

## Project Overview
This project implements a full ETL pipeline for credit card fraud detection using the [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle. The goal is to demonstrate that engineered behavioral features, when added to a multi-layered ETL pipeline, can enhance the performance of fraud detection models.

The pipeline uses:
- **PostgreSQL** for data storage
- **Apache Airflow** for pipeline orchestration
- **Python** for feature engineering and machine learning
- **scikit-learn** for model training and evaluation

## Architecture

Kaggle Dataset → Raw Data Layer → Staging Data Layer → Feature Engineering → Curated Data Layer → Machine Learning Models → Model Comparison -->

### Schema Layers

Raw Layer: 
Stores the original transaction dataset without any modifications
PostgreSQL table: raw_schema.credit_card_transactions

Staging Layer: 
Contains the cleaned and validated transactions
  Transformations: duplicate removal and validation of transaction amount
PostgreSQL table: 'staging_schema.cleaned_transactions'

Curated Layer: 
Contains engineered behavioral features used for ML model training
PostgreSQL table: 'curated_schema.feature_engineered_transactions'
Engineered Features: 
* 'rolling_avg_amount_10'
* 'rolling_std_amount_10'
* 'rolling_sum_amount_10' 
* 'amount_zscore' 
* 'high_value_flag'
* 'amount_velocity'

### Airflow Orchestration

'create_schemas_task >> create_raw_table_task >> load_raw_data_task >> create_staging_table_task >> load_staging_task >> create_curated_table_task >> feature_engineering_task >> baseline_modeling_task >> curated_modeling_task >> comparison_task'

### Model Training and Metrics

Two models were trained on each dataset. Logistic Regression and Random Forest. They were run on "Baseline" and "Curated" datasets. The baseline is the cleaned dataset from the Staging Layer and the curated is the feature engineered data from the Curated Layer.

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
* 'pipeline_architecture.png'

dags/
* 'fraud_pipeline_dag.py'

scripts/
* 'baseline_modeling.py'
* 'comparison.py'
* 'curated_modeling.py'
* 'feature_engineering.py'
* 'load_raw_data.py'

sql/
* 'create_curated_table.sql'
* 'create_database.sql'
* 'create_raw_table.sql'
* 'create_schemas.sql'
* 'create_staging_table.sql'
* 'load_staging.sql'

README.md

'requirements.txt'



## Execution
### Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher (running and accessible)
- The following Python packages (install with `pip3 install -r requirements.txt`)

### Installation

1. **Install Python 3.8+**  
   Download from [python.org](https://www.python.org/downloads/).

2. **Install PostgreSQL 12+**  
   Download from [postgresql.org](https://www.postgresql.org/download/).

3. **Install Python dependencies**
   pip3 install -r requirements.txt


# Results
The project evaluates whether engineered behavioral features improve fraud detection performance relative to baseline transactional features.


