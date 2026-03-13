import psycopg2

def get_connection():
    conn = psycopg2.connect (
        host="localhost",
        database="fraud_detection",
        user="postgres",
        password="******"
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
