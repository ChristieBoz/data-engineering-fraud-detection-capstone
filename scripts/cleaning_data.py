import pandas as pd
from scripts.db_utils import run_sql_script, engine

def cleaning_data():
    print("Cleaning transactional data")

    run_sql_script("sql/load_staging.sql")


    df = pd.read_sql(
        "SELECT * FROM staging_schema.cleaned_transactions",
        engine
    )

    df.to_csv("results/metrics/cleaned_transactions.csv", index=False)