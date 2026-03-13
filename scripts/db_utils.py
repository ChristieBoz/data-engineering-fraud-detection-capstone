import psycopg2
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:newpassword@localhost:5432/fraud_capstone")

def get_connection():
    conn = psycopg2.connect (
        host="localhost",
        database="fraud_capstone",
        user="postgres",
        password="newpassword"
        )

    return conn

def run_sql_script(script_path):
    conn = get_connection()
    cursor = conn.cursor()
    
    with open(script_path, "r") as file:
        sql = file.read()

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
