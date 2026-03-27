from database import cursor, conn

def create_tables():

    # جدول المستخدمين
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        last_daily INTEGER DEFAULT 0,
        invited_by INTEGER,
        join_date TEXT
    )
    """)

    # جدول تنفيذ المهام (مرة يوميًا)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_done (
        user_id INTEGER,
        task_id INTEGER,
        last_time INTEGER,
        PRIMARY KEY (user_id, task_id)
    )
    """)

    # جدول الفاصل بين المهام (3 دقائق)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_last_task (
        user_id INTEGER PRIMARY KEY,
        last_time INTEGER
    )
    """)

    conn.commit()
    print("✅ Database Ready")
