from database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # 👤 جدول المستخدمين
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        balance INTEGER DEFAULT 0
    )
    """)

    # 📢 جدول المهام
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT,
        description TEXT,
        link TEXT,
        reward INTEGER
    )
    """)

    # 📅 جدول تتبع المهام اليومية
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_tasks (
        user_id BIGINT,
        task_id INTEGER,
        date DATE,
        PRIMARY KEY (user_id, task_id, date)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Tables created successfully")

# تشغيل الملف مباشرة
if __name__ == "__main__":
    create_tables()
