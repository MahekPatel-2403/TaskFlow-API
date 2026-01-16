import psycopg2
import os

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE") or os.getenv("DB_NAME"),
        user=os.getenv("PGUSER") or os.getenv("DB_USER"),
        password=os.getenv("PGPASSWORD") or os.getenv("DB_PASSWORD"),
        host=os.getenv("PGHOST") or os.getenv("DB_HOST"),
        port=os.getenv("PGPORT") or os.getenv("DB_PORT")
    )
    conn.autocommit = False
    return conn        
