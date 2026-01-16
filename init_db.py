from app.utils.db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    user_id INTEGER REFERENCES users(id)
    );
""")

conn.commit()
cur.close()
conn.close()

print("PostgreSQL tables created")