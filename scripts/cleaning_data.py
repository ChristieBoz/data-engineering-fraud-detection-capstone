from scripts.db_utils import run_sql_script

def cleaning_data():
    print("Cleaning transactional data")
    run_sql_script("~/sql/load_staging.sql")

    cleaning_data.to_csv("~/results/metrics/cleaned_transactions.csv", index=False)