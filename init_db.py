from database import get_connection

conn = get_connection()
cur = conn.cursor()

# جدول المستخدمين
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE,
    points INTEGER DEFAULT 0
);
""")

# جدول المهام
cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    link TEXT,
    reward INTEGER
);
""")

# جدول تنفيذ المهام
cur.execute("""
CREATE TABLE IF NOT EXISTS user_tasks (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    task_id INTEGER,
    date DATE
);
""")

conn.commit()
cur.close()
conn.close()

print("✅ DB READY")
