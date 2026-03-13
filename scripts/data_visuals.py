import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def class_distribution():

    engine = create_engine(f"postgresql+psycopg2://postgres:******@localhost:5432/fraud_capstone")

    df = pd.read_sql("SELECT class, COUNT(*) as count FROM staging_schema.cleaned_transactions GROUP BY class;", engine)

    counts = df["class"].value_counts()

    counts.plot(kind="bar")
    plt.title("Fraud vs Non-Fraud Transactions")
    plt.xlabel("Class")
    plt.ylabel("Number of Transactions")

    plt.savefig("results/visuals/class_distribution.png")
    plt.close()

def amount_distribution():

    engine = create_engine(f"postgresql+psycopg2://postgres:******@localhost:5432/fraud_capstone")

    df = pd.read_sql("SELECT amount FROM staging_schema.cleaned_transactions;", engine)

    plt.figure(figsize=(10, 6))
    plt.hist(df["amount"], bins=50, color="blue", edgecolor="black")
    plt.title("Distribution of Transaction Amounts")
    plt.xlabel("Transaction Amount")
    plt.ylabel("Frequency")
    plt.xlim(0, 2000)  # Limit x-axis for better visualization

    plt.savefig("results/visuals/amount_distribution.png")
    plt.close()