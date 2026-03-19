import sqlite3


def vulnerable(user_id, user_name):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
    cursor.execute("SELECT * FROM users WHERE name = '{}'".format(user_name))
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
