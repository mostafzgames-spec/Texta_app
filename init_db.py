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

    conn.commit()
    print("✅ تم إنشاء الجداول بنجاح")

if __name__ == "__main__":
    create_tables()
