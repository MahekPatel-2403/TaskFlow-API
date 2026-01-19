from app.utils.db import get_db_connection

def create_task(data, user_id):
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return None, "Title is required"

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO tasks (title, description, user_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (title, description, user_id)
        )

        task_id = cur.fetchone()[0]
        conn.commit()   

        return {
            "id": task_id,
            "title": title,
            "description": description
        }, None

    except Exception as e:
        conn.rollback()  
        print("DB ERROR:", e)
        return None, "Database error while creating task"

    finally:
        cur.close()
        conn.close()

def get_tasks_paginated(page=1, limit=5):
    conn = get_db_connection()
    cur = conn.cursor()

    offset = (page - 1) * limit

    cur.execute("""
    SELECT id, title, description, completed, created_at
    FROM tasks
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s;
""", (limit, offset))

    rows = cur.fetchall()

    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "user_id": r[3]
        })

    cur.close()
    conn.close()

    return tasks

