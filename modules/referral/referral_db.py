from database import cursor, conn

def set_referrer(user_id, invited_by):
    cursor.execute("UPDATE users SET invited_by=? WHERE id=?", (invited_by, user_id))
    conn.commit()


def get_referrer(user_id):
    cursor.execute("SELECT invited_by FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def add_referral_profit(user_id, amount):
    referrer = get_referrer(user_id)

    if referrer:
        bonus = int(amount * 0.3)

        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE id=?",
            (bonus, referrer)
        )
        conn.commit()
