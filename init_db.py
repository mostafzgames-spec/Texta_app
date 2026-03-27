# تنفيذ المهام (مرة يوميًا)
cursor.execute("""
CREATE TABLE IF NOT EXISTS task_done (
    user_id INTEGER,
    task_id INTEGER,
    last_time INTEGER,
    PRIMARY KEY (user_id, task_id)
)
""")

# فاصل بين المهام (3 دقائق)
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_last_task (
    user_id INTEGER PRIMARY KEY,
    last_time INTEGER
)
""")
