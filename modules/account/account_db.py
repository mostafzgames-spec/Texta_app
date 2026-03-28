from database import get_connection

def create_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
        conn.commit()

    cur.close()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()

    cur.close()
    conn.close()
    return user
