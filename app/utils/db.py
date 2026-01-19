import os
import psycopg2

def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(database_url)
    return conn
