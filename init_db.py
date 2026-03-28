from database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # جدول المستخدمين
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        referrer_id BIGINT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # جدول المهام
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        link TEXT,
        reward INTEGER
    );
    """)

    # تنفيذ المهام (منع التكرار)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_tasks (
        user_id BIGINT,
        task_id INTEGER,
        last_done TIMESTAMP,
        PRIMARY KEY (user_id, task_id)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
