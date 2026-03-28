from database import get_connection

def get_tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, reward FROM tasks")
    data = cur.fetchall()

    cur.close()
    conn.close()
    return data

def get_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cur.fetchone()

    cur.close()
    conn.close()
    return task
