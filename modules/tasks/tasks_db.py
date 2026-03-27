from database import cursor, conn
import time

# 🔹 منع تكرار نفس المهمة في نفس اليوم
def can_do_task(user_id, task_id):
    cursor.execute(
        "SELECT last_time FROM task_done WHERE user_id=? AND task_id=?",
        (user_id, task_id)
    )
    result = cursor.fetchone()

    if not result:
        return True

    last_time = result[0]
    now = int(time.time())

    return now - last_time > 86400  # 24 ساعة


def save_task(user_id, task_id):
    now = int(time.time())

    cursor.execute(
        "INSERT OR REPLACE INTO task_done (user_id, task_id, last_time) VALUES (?, ?, ?)",
        (user_id, task_id, now)
    )
    conn.commit()


# 🔹 فاصل 3 دقائق بين أي مهمتين
def can_do_new_task(user_id):
    cursor.execute(
        "SELECT last_time FROM user_last_task WHERE user_id=?",
        (user_id,)
    )
    result = cursor.fetchone()

    if not result:
        return True

    now = int(time.time())
    return now - result[0] > 180  # 3 دقائق


def update_last_task_time(user_id):
    now = int(time.time())

    cursor.execute(
        "INSERT OR REPLACE INTO user_last_task (user_id, last_time) VALUES (?, ?)",
        (user_id, now)
    )
    conn.commit()
