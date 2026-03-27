import sqlite3
import datetime
import pytz

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# المنطقة الزمنية (مصر)
egypt = pytz.timezone("Africa/Cairo")


def add_user(user_id, invited_by=None):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    if not cursor.fetchone():

        now = datetime.datetime.now(egypt).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO users (id, balance, last_daily, invited_by, join_date) VALUES (?, 0, 0, ?, ?)",
            (user_id, invited_by, now)
        )
        conn.commit()


def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


def add_balance(user_id, amount):
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE id=?",
        (amount, user_id)
    )
    conn.commit()


def get_last_daily(user_id):
    cursor.execute("SELECT last_daily FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


def update_daily(user_id, time):
    cursor.execute(
        "UPDATE users SET last_daily=? WHERE id=?",
        (time, user_id)
    )
    conn.commit()


def get_join_date(user_id):
    cursor.execute("SELECT join_date FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else "غير متوفر"
