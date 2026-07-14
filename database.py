import sqlite3


class Database:

    def __init__(self):

        self.db = sqlite3.connect(
            "data/database.db",
            check_same_thread=False
        )

        self.cursor = self.db.cursor()

        self.create_tables()

    def create_tables(self):

        # کاربران
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            start_param TEXT,
            is_banned INTEGER DEFAULT 0

        )
        """)

        self.db.commit()

    # ---------------- کاربران ---------------- #

    def add_user(self, user):

        self.cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            user_id,
            first_name,
            username
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """, (
            user.id,
            user.first_name,
            user.username
        ))

        self.db.commit()

    def get_users(self):

        self.cursor.execute("""
        SELECT user_id
        FROM users
        """)

        return self.cursor.fetchall()

    def users_count(self):

        self.cursor.execute("""
        SELECT COUNT(*)
        FROM users
        """)

        return self.cursor.fetchone()[0]

    # ---------------- بن ---------------- #

    def ban_user(self, user_id):

        self.cursor.execute("""
        UPDATE users
        SET is_banned = 1
        WHERE user_id = ?
        """, (user_id,))

        self.db.commit()

    def unban_user(self, user_id):

        self.cursor.execute("""
        UPDATE users
        SET is_banned = 0
        WHERE user_id = ?
        """, (user_id,))

        self.db.commit()

    def is_banned(self, user_id):

        self.cursor.execute("""
        SELECT is_banned
        FROM users
        WHERE user_id = ?
        """, (user_id,))

        row = self.cursor.fetchone()

        if row is None:
            return False

        return bool(row[0])

    # ---------------- Start Param ---------------- #

    def save_start_param(self, user_id, start_param):

        self.cursor.execute("""
        UPDATE users
        SET start_param = ?
        WHERE user_id = ?
        """, (
            start_param,
            user_id
        ))

        self.db.commit()

    def get_start_param(self, user_id):

        self.cursor.execute("""
        SELECT start_param
        FROM users
        WHERE user_id = ?
        """, (user_id,))

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None

    def clear_start_param(self, user_id):

        self.cursor.execute("""
        UPDATE users
        SET start_param = NULL
        WHERE user_id = ?
        """, (user_id,))

        self.db.commit()

    # ---------------- بستن دیتابیس ---------------- #

    def close(self):

        self.db.close()