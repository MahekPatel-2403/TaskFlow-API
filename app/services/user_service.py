from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.db import get_db_connection


def create_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return None, "Username and password required"

    hashed = generate_password_hash(password)

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
            (username, hashed)
        )

        user_id = cur.fetchone()[0]
        conn.commit()

        return {"id": user_id, "username": username}, None

    except Exception as e:
        conn.rollback()

        if "unique" in str(e).lower():
            return None, "User already exists"

        print("DB ERROR:", e)
        return None, "Database error while creating user"

    finally:
        cur.close()
        conn.close()


def authenticate_user(username, password):
    """
    Used during login
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT id, username, password FROM users WHERE username = %s",
            (username,)
        )

        row = cur.fetchone()

        if row and check_password_hash(row[2], password):
            return {"id": row[0], "username": row[1]}

        return None

    finally:
        cur.close()
        conn.close()
