from database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        referrer_id BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        link TEXT,
        reward INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_tasks (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        task_id INTEGER,
        last_done TIMESTAMP,
        UNIQUE(user_id, task_id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
