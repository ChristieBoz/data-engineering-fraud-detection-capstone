# Data Engineering Fraud Detection Capstone
WGU Capstone Project - Credit Card Fraud Detection  
**Technologies:** PostgreSQL · Python · scikit-learn

## Project Overview
This project implements a full ETL pipeline for credit card fraud detection using the [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle. The goal is to demonstrate that engineered behavioral features, when added to a multi-layered ETL pipeline, can enhance the performance of fraud detection models.

The pipeline uses:
- **PostgreSQL** for data storage
- **Python** for feature engineering and machine learning
- **scikit-learn** for model training and evaluation

## Architecture

Kaggle Dataset &#8594; Raw Data Layer &#8594; Staging Data Layer &#8594; Feature Engineering &#8594; Curated Data Layer &#8594; Machine Learning Models &#8594; Model Comparison 

### Schema Layers

- **Raw Layer:**  
  Stores the original transaction dataset without modifications  
  Table: `raw_schema.credit_card_transactions`

- **Staging Layer:**  
  Contains cleaned and validated transactions  
  Transformations: duplicate removal and validation of transaction amount  
  Table: `staging_schema.cleaned_transactions`

- **Curated Layer:**  
  Contains engineered behavioral features for ML model training  
  Table: `curated_schema.feature_engineered_transactions`  
  Engineered Features:  
    - `rolling_avg_amount_10`  
    - `rolling_std_amount_10`  
    - `rolling_sum_amount_10`  
    - `amount_zscore`  
    - `high_value_flag`  
    - `amount_velocity`

### Airflow Orchestration

create_schemas_task >> create_raw_table_task >> load_raw_data_task >> create_staging_table_task >> load_staging_task >> create_curated_table_task >> feature_engineering_task >> baseline_modeling_task >> curated_modeling_task >> comparison_task

### Model Training and Metrics

Two models are trained on each dataset: **Logistic Regression** and **Random Forest**.  
- **Baseline:** Cleaned dataset from the Staging Layer (`staging_schema.cleaned_transactions`)
- **Curated:** Feature-engineered data from the Curated Layer (`curated_schema.feature_engineered_transactions`)

**Metrics used:**
- Precision
- Recall
- F1 Score
- ROC_AUC
- Feature Importance

Results are saved to `curated_results.csv`.

### Repository Structure

architecture/ pipeline_architecture.png

run_pipeline.py

screenshots/ 

scripts/ baseline_modeling.py comparison.py curated_modeling.py feature_engineering.py load_raw_data.py

sql/ create_curated_table.sql create_database.sql create_raw_table.sql create_schemas.sql create_staging_table.sql load_staging.sql

README.md 

requirements.txt

## Execution

### Requirements
- Python 3.8 or higher
- PostgreSQL 12 or higher (running and accessible)
- The Python packages listed in `requirements.txt` (install with `pip install -r requirements.txt`)

### Installation

1. **Install Python 3.8+**  
   [Download from python.org](https://www.python.org/downloads/)

2. **Install PostgreSQL 12+**  
   [Download from postgresql.org](https://www.postgresql.org/download/)

   
4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt

  
# Results
The project evaluates whether engineered behavioral features improve fraud detection performance relative to baseline transactional features.
Results are summarized in 'curated_results.csv'


