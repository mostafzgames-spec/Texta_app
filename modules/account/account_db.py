from database import cursor

def get_user_data(user_id):
    cursor.execute("SELECT id, join_date FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()
